"""Tests voor wat CyberScope toevoegt aan de pipeline van de Data & AI Radar:
de echte context, de extra velden in een uitleg, de regio-voorrang en wie issues mag insturen.
Draaien: python -m unittest discover -s tests -t ."""
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from pipeline import config as cfg
from pipeline import enrich
from pipeline.normalize import normalize
from pipeline.score import score_article

ROOT = Path(__file__).resolve().parent.parent
CONTEXT = ROOT / "context"
NOW = datetime(2026, 11, 3, 20, 0, tzinfo=timezone.utc)


def _load_real():
    import yaml
    read = lambda n: yaml.safe_load((CONTEXT / n).read_text(encoding="utf-8"))  # noqa: E731
    return cfg.Config(interests=read("interests.yml"), sources=read("sources.yml"))


def article(**kw):
    base = {"format_version": 2, "headline": "Kop", "summary": "s", "personal_relevance": "r", "takeaway": "t",
            "story": ["Wat er gebeurde.", "Meer uitleg."], "key_facts": ["CVE-2026-0001 in versie 1.2."],
            "limitations": [], "topics": ["vulnerabilities_cve"],
            "quality": {"depth": 0.7, "practicality": 0.7, "novelty": 0.7}}
    base.update(kw)
    return base


class TestRealContext(unittest.TestCase):
    def test_context_validates(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_context.py")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_areas_follow_profile(self):
        conf = _load_real()
        shares = {a["id"]: a["target_share"] for a in conf.interests["interest_areas"]}
        self.assertEqual(shares, {"kwetsbaarheden": 0.30, "techniek": 0.30, "incidenten": 0.25, "praktijk": 0.15})
        self.assertEqual(conf.topics["security_market"]["priority"], 1, "leveranciersnieuws alleen bij groot nieuws")

    def test_regions_ordered_nl_first(self):
        b = _load_real().scoring["region_bonus"]
        self.assertTrue(b["nl"] > b["benelux"] > b["eu"] > b["na"] >= b["world"])

    def test_no_leren_tab(self):
        html = (ROOT / "app" / "index.html").read_text(encoding="utf-8")
        self.assertNotIn('data-v="leren"', html)
        self.assertNotIn("cca-academy", html)
        self.assertFalse((ROOT / "app" / "leren").exists())

    def test_own_storage_and_cache_prefix(self):
        """Zelfde origin (tomasr91.github.io) als de Data & AI Radar: eigen sleutels en caches."""
        html = (ROOT / "app" / "index.html").read_text(encoding="utf-8")
        self.assertNotIn('"radar:', html)
        self.assertNotIn("'radar:", html)
        sw = (ROOT / "app" / "pwa" / "sw.js").read_text(encoding="utf-8")
        self.assertIn("cyberscope-", sw)
        self.assertNotIn('startsWith("radar-")', sw)


class TestEnrichmentFields(unittest.TestCase):
    def setUp(self):
        self.topics = set(_load_real().topics)

    def test_short_article_valid(self):
        self.assertEqual(enrich.validate(article(), self.topics), [])

    def test_takeaway_required(self):
        a = article(); del a["takeaway"]
        self.assertTrue(any("takeaway" in p for p in enrich.validate(a, self.topics)))

    def test_long_article_with_sections_and_questions(self):
        a = article(sections=[{"heading": "Wat is de technologie?", "paragraphs": ["Een webserver stuurt pagina's."]},
                              {"heading": "Hoe zie je dit?", "paragraphs": ["In het log van de webserver."]}],
                    customer_questions=["Weten jullie welke servers deze software draaien?"],
                    region="nl", exploitation="actief_misbruikt", patch_status="patch_beschikbaar",
                    terms=[{"term": "webserver", "explanation": "Een computer die webpagina's verstuurt."}])
        self.assertEqual(enrich.validate(a, self.topics), [], "begrip uit sections mag onderstreept worden")

    def test_invalid_values_rejected(self):
        for kw in [{"region": "mars"}, {"exploitation": "misschien"}, {"patch_status": "ja"},
                   {"sections": [{"heading": "", "paragraphs": []}]}, {"customer_questions": []}]:
            self.assertTrue(enrich.validate(article(**kw), self.topics), kw)

    def test_showcase_log_language(self):
        sc = {"caption": "Een logregel.", "language": "log", "code": "203.0.113.10 - - GET /", "note": "Nagebouwd."}
        self.assertEqual(enrich.validate(article(showcase=sc), self.topics), [])


class TestRegionBonus(unittest.TestCase):
    def test_dutch_news_scores_higher(self):
        conf = _load_real()
        raw = {"source_id": "bleepingcomputer", "title": "Ransomware attack", "url": "https://example.org/x",
               "published_raw": "Tue, 03 Nov 2026 10:00:00 GMT", "fetched_at": "2026-11-03T12:00:00Z", "excerpt": ""}
        scores = {}
        for region in ["nl", "world"]:
            a = normalize(raw)
            a.update(processing_status="enriched", topics=["ransomware"], region=region,
                     quality={"depth": 0.6, "practicality": 0.6, "novelty": 0.6})
            score_article(a, conf, NOW)
            scores[region] = a["relevance_score"]
        self.assertEqual(scores["nl"] - scores["world"], 6)

    def test_source_region_used_when_article_has_none(self):
        conf = _load_real()
        a = normalize({"source_id": "security_nl", "title": "Datalek bij bedrijf", "url": "https://example.org/y",
                       "published_raw": "Tue, 03 Nov 2026 10:00:00 GMT", "fetched_at": "2026-11-03T12:00:00Z", "excerpt": ""})
        a.update(processing_status="enriched", topics=["incidents_breaches"], quality={"depth": 0.5, "practicality": 0.5, "novelty": 0.5})
        score_article(a, conf, NOW)
        self.assertEqual(a["score_parts"].get("region"), 0.06)


class TestFeedRepair(unittest.TestCase):
    def test_broken_feed_is_repaired(self):
        from pipeline.providers import feeds
        bad = (b'<?xml version="1.0" encoding="utf-8"?><rss><channel><item><title>Fish &amp; chips &nbsp;&rsquo; R&D \x0b</title>'
               b'<link>https://example.org/a?x=1&y=2</link><pubDate>Tue, 03 Nov 2026 08:00:00 GMT</pubDate></item></channel></rss>')
        items = feeds.parse_feed(bad, "s", "2026-11-03T09:00:00Z")
        self.assertEqual(items[0]["url"], "https://example.org/a?x=1&y=2")
        self.assertIn("R&D", items[0]["title"])

    def test_hopeless_feed_still_fails(self):
        from pipeline.providers import feeds
        with self.assertRaises(ValueError):
            feeds.parse_feed(b"<html><body>geen feed", "s", "x")


class TestIssueAuthors(unittest.TestCase):
    def test_owner_plus_listed_names(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "app.yml").write_text("issue_authors: [LezerX]\n", encoding="utf-8")
            self.assertEqual(cfg.issue_authors("tomasr91", Path(d)), {"tomasr91", "lezerx"})
            self.assertEqual(cfg.issue_authors("tomasr91", Path(d) / "leeg"), {"tomasr91"})

    def test_scripts_accept_listed_reader(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        import next_deepdive
        issues = [{"number": 1, "title": "Verdieping: sql-injection", "user": {"login": "someone-else"}},
                  {"number": 2, "title": "Verdieping: http-en-https", "user": {"login": "tomasr91"}}]
        self.assertEqual(next_deepdive.choices(issues, "tomasr91"), [(2, "http-en-https")])


if __name__ == "__main__":
    unittest.main()
