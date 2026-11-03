"""End-to-end test van wat CyberScope toevoegt: een uitgebreid artikel met vaste onderdelen,
klantvragen, 'Onthoud', labels voor misbruik en patch, en regio-voorrang. Bouwt een feed met de
echte CyberScope-context en een verzonnen testartikel (duidelijk als test herkenbaar).

Draaien: python tests/e2e_cyber.py [map-voor-screenshots]
"""
import functools
import http.server
import json
import shutil
import sys
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SHOTS = Path(sys.argv[1]) if len(sys.argv) > 1 else None
sys.path.insert(0, str(ROOT))
from pipeline import build as build_mod, config as cfg, enrich  # noqa: E402
from pipeline.normalize import normalize  # noqa: E402
from pipeline.providers import ProviderResult  # noqa: E402

results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print(("OK   " if cond else "FOUT ") + name + (f"  ({detail})" if detail and not cond else ""))


NOW = datetime(2026, 11, 3, 20, 0, tzinfo=timezone.utc)
ITEMS = [
    {"source_id": "security_nl", "title": "Testbericht: kwetsbaarheid in voorbeeldsoftware", "url": "https://example.org/test-1",
     "published_raw": "Tue, 03 Nov 2026 08:00:00 GMT", "fetched_at": "2026-11-03T09:00:00Z", "excerpt": "test"},
    {"source_id": "bleepingcomputer", "title": "Test: ransomware incident", "url": "https://example.org/test-2",
     "published_raw": "Tue, 03 Nov 2026 07:00:00 GMT", "fetched_at": "2026-11-03T09:00:00Z", "excerpt": "test"},
]
LONG = {
    "format_version": 2, "headline": "Test: lek in voorbeeldwebserver laat aanvallers binnen",
    "summary": "Testartikel voor de app. Een fout in een verzonnen webserver laat aanvallers opdrachten uitvoeren.",
    "story": ["Dit is een verzonnen testartikel. Een leverancier meldt een lek in Voorbeeldserver."],
    "sections": [
        {"heading": "Wat is de technologie?", "paragraphs": ["Een webserver ontvangt verzoeken van browsers en stuurt pagina's terug."]},
        {"heading": "Wat gaat er technisch fout?", "paragraphs": ["De server controleert invoer niet goed. Daardoor kan een aanvaller een webshell plaatsen."]},
        {"heading": "Hoe zie je dit?", "paragraphs": ["In het log van de webserver staan vreemde verzoeken."]},
    ],
    "key_facts": ["Testfeit: versie 1.0 tot en met 1.4 is kwetsbaar."], "limitations": ["Testonbekend: wie de aanvallers zijn."],
    "personal_relevance": "Testrelevantie voor klantgesprekken.",
    "customer_questions": ["Weten jullie welke servers Voorbeeldserver draaien?", "Zien jullie vreemde verzoeken in de logs?"],
    "takeaway": "Testles: invoer die niet gecontroleerd wordt, is een open deur.",
    "region": "nl", "exploitation": "actief_misbruikt", "patch_status": "patch_beschikbaar",
    "topics": ["vulnerabilities_cve", "web_software_security"], "quality": {"depth": 0.8, "practicality": 0.8, "novelty": 0.8},
    "soort": "kwetsbaarheid",
    "showcase": {"caption": "Testlogregel.", "language": "log", "code": "203.0.113.10 - - \"GET /upload.php HTTP/1.1\" 200", "note": "Nagebouwd."},
    "terms": [{"term": "webshell", "explanation": "Testuitleg: een achterdeur op een webserver."}],
    "processed_by": "test", "processed_at": "2026-11-03T10:00:00Z",
}
SHORT = {
    "format_version": 2, "headline": "Test: kort incidentbericht", "summary": "Kort testbericht.",
    "story": ["Een verzonnen organisatie meldt een incident.", "Wat er gebeurde is nog onbekend."],
    "key_facts": ["Testfeit."], "limitations": [], "personal_relevance": "Test.", "takeaway": "Testles kort.",
    "region": "world", "topics": ["ransomware"], "quality": {"depth": 0.5, "practicality": 0.6, "novelty": 0.6},
    "soort": "incident", "processed_by": "test", "processed_at": "2026-11-03T10:00:00Z",
}

tmp = Path(tempfile.mkdtemp())
cfg.DATA = tmp
enrich.CACHE = tmp / "enrichment"
enrich.CACHE.mkdir(parents=True)
for item, data in zip(ITEMS, [LONG, SHORT]):
    aid = normalize(item)["id"]
    (enrich.CACHE / f"{aid}.json").write_text(json.dumps({**data, "article_id": aid, "url": item["url"]}), encoding="utf-8")
conf = cfg.load()
provider = lambda c: ProviderResult(items=ITEMS, source_results=[], mode="live", note="test")  # noqa: E731
feed = build_mod.build("feeds", tmp / "feed.json", 0, now=NOW, conf=conf, provider_fn=provider)
by = {a["headline"]: a for a in feed["articles"]}
check("pipeline: beide testartikelen in de feed", len(feed["articles"]) == 2, str([a.get("decision") for a in feed["articles"]]))
long_a = by.get(LONG["headline"], {})
check("pipeline: regio Nederland geeft extra punten", long_a.get("score_parts", {}).get("region") == 0.06)
check("pipeline: nieuwe velden komen in de feed", all(k in long_a for k in ["customer_questions", "takeaway", "exploitation"]))
check("pipeline: begrip uit een onderdeel in de woordenlijst", any(g["term"] == "webshell" for g in feed["glossary"]))

site = Path(tempfile.mkdtemp())
page_html = (ROOT / "app" / "index.html").read_text(encoding="utf-8")
(site / "index.html").write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + page_html, encoding="utf-8")
(site / "feed.json").write_text(json.dumps(feed), encoding="utf-8")
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(site))
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{srv.server_address[1]}/index.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 412, "height": 915}, device_scale_factor=2, is_mobile=True, has_touch=True, locale="nl-NL")
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.route("**/fonts.g*/**", lambda r: r.abort())
    page.route("https://api.github.com/**", lambda r: r.fulfill(status=200, content_type="application/json", body="[]"))
    page.goto(url)
    page.wait_for_selector(".card")
    check("titel CyberScope", page.title() == "CyberScope" and "CyberScope" in page.locator("h1").first.inner_text())
    check("tabbladen zonder Leren", page.locator("#seg-view button").all_inner_texts() == ["Actueel", "Verdieping"])
    check("kaart toont 'actief misbruikt'", page.locator(".card .pill.actief_misbruikt").count() == 1)
    accent = page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--accent').trim()")
    check("eigen accentkleur (cyaan)", accent.lower() == "#4cc3e8", accent)
    if SHOTS:
        page.screenshot(path=str(SHOTS / "cyber-1-feed.png"))
    page.goto(url + "#a-" + long_a["id"])
    page.wait_for_selector("#reader:not([hidden])")
    txt = page.locator("#reader").inner_text()
    heads = page.locator("#reader .art-sec h2").all_inner_texts()
    check("uitgebreid artikel: vaste koppen", heads == ["Wat is er gebeurd?", "Wat is de technologie?", "Wat gaat er technisch fout?", "Hoe zie je dit?"], str(heads))
    check("label misbruik, geen patchlabel", "actief misbruikt" in txt and "patch beschikbaar" not in txt)
    check("klantvragen", page.locator("#reader .qs li").count() == 2 and "vragen die je een klant kunt stellen" in txt.lower())
    check("bevestigd en onbekend apart", "Bevestigd" in txt and "Nog onbekend of onzeker" in txt and "Testonbekend" in txt)
    check("onthoud-blok", page.locator("#reader .takeaway").count() == 1 and "Testles" in page.locator("#reader .takeaway").inner_text())
    check("begrip in een onderdeel onderstreept", page.locator("#reader .art-sec .term, #reader .art-sec [data-term]").count() >= 1
          or "webshell" in (page.locator("#reader .art-sec").nth(2).inner_html()))
    check("zo ziet het eruit (logregel)", page.locator("#reader pre.code[data-lang='log']").count() == 1)
    if SHOTS:
        page.screenshot(path=str(SHOTS / "cyber-2-artikel.png"))
        page.locator("#reader .takeaway").scroll_into_view_if_needed()
        page.screenshot(path=str(SHOTS / "cyber-3-artikel-einde.png"))
    page.click("#score-btn")
    check("scoredialoog toont regio", "Regio" in page.locator("#score-dlg").inner_text() and "Nederland" in page.locator("#score-dlg").inner_text())
    check("geen JavaScript-fouten", not errors, "; ".join(errors))
    browser.close()
srv.shutdown()
shutil.rmtree(tmp, ignore_errors=True)

failed = [r for r in results if not r[1]]
print(f"\n{len(results) - len(failed)} van {len(results)} controles geslaagd")
sys.exit(1 if failed else 0)
