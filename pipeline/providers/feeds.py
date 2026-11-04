"""Live ophalen van RSS-, Atom- en GitHub-releasefeeds.

Eén bron die faalt blokkeert de rest niet: elke bron krijgt een eigen status.
Bronnen zonder feed (fetch_method html of manual) worden in V1 niet
automatisch opgehaald; dat staat als 'not_supported' of 'skipped' in de status.
"""
import html
import html.entities
import re
import urllib.error
from urllib.parse import urljoin
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

from . import ProviderResult

TIMEOUT = 20
UA = "CyberScope/0.1 (+persoonlijke nieuwsfeed; github.com/tomasr91/cyber-radar)"
ATOM = "{http://www.w3.org/2005/Atom}"
MAX_ITEMS_PER_SOURCE = 30


def _now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def _text(el, tag):
    found = el.find(tag)
    return (found.text or "").strip() if found is not None and found.text else ""


XML_ENTITIES = {"amp", "lt", "gt", "quot", "apos"}


def _repair(xml_bytes: bytes) -> bytes:
    """Maakt veelvoorkomende fouten in feeds onschadelijk: stuurtekens weg, HTML-entiteiten
    (&nbsp;, &rsquo;) als tekens, en een losse '&' als &amp;."""
    text = xml_bytes.decode("utf-8", "replace")
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)

    def entity(m):
        name = m.group(1)
        if name in XML_ENTITIES:
            return m.group(0)
        ch = html.entities.html5.get(name + ";")
        return html.escape(ch) if ch else "&amp;" + name + ";"
    text = re.sub(r"&([A-Za-z][A-Za-z0-9]*);", entity, text)
    text = re.sub(r"&(?!(?:[A-Za-z][A-Za-z0-9]*|#[0-9]+|#x[0-9A-Fa-f]+);)", "&amp;", text)
    text = re.sub(r"^\s*<\?xml[^>]*\?>", "", text)   # declaratie met encoding mag niet in een str
    return text.encode("utf-8")


def parse_feed(xml_bytes: bytes, source_id: str, fetched_at: str) -> list:
    """Leest RSS 2.0 en Atom. Gooit ValueError bij ongeldige XML."""
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        # Sommige feeds bevatten losse '&', HTML-entiteiten of stuurtekens.
        # Eén herstelpoging; lukt dat niet, dan blijft de bron 'failed' met de oorspronkelijke fout.
        try:
            root = ET.fromstring(_repair(xml_bytes))
        except ET.ParseError:
            raise ValueError(f"geen geldige XML ({e})") from e
    items = []
    if root.tag == "rss" or root.find("channel") is not None:
        for it in root.iter("item"):
            items.append({
                "source_id": source_id,
                "title": _text(it, "title"),
                "url": _text(it, "link"),
                "published_raw": _text(it, "pubDate") or _text(it, "{http://purl.org/dc/elements/1.1/}date") or None,
                "fetched_at": fetched_at,
                "excerpt": _text(it, "description"),
            })
    elif root.tag == f"{ATOM}feed":
        for e in root.iter(f"{ATOM}entry"):
            link = ""
            for ln in e.findall(f"{ATOM}link"):
                if ln.get("rel", "alternate") == "alternate":
                    link = ln.get("href", "")
                    break
            items.append({
                "source_id": source_id,
                "title": _text(e, f"{ATOM}title"),
                "url": link,
                "published_raw": _text(e, f"{ATOM}published") or _text(e, f"{ATOM}updated") or None,
                "fetched_at": fetched_at,
                "excerpt": _text(e, f"{ATOM}summary") or _text(e, f"{ATOM}content"),
            })
    else:
        raise ValueError(f"onbekend feedformaat (root <{root.tag}>)")
    items = [i for i in items if i["title"] and i["url"]]
    if not items:
        raise ValueError("feed bevat geen bruikbare items")
    return items[:MAX_ITEMS_PER_SOURCE]


def feed_url_for(source: dict):
    """Welke URL wordt opgehaald, of None als de methode niet wordt ondersteund."""
    method = source["fetch_method"]
    if method in ("rss", "atom"):
        return source.get("feed_url")
    if method == "github_releases":
        # GitHub publiceert releases als Atom op <repo>/releases.atom.
        repo = source["url"].rstrip("/").removesuffix("/releases")
        return f"{repo}/releases.atom"
    return None


def collect(config, getter=http_get) -> ProviderResult:
    items, results = [], []
    for src in config.source_list:
        if not src.get("enabled"):
            continue
        checked_at = _now()
        url = feed_url_for(src)
        if url is None:
            status = "skipped" if src["fetch_method"] == "manual" else "not_supported"
            msg = ("Handmatige bron; wordt niet automatisch opgehaald." if status == "skipped"
                   else "Geen feed bekend; pagina's verwerken zit niet in versie 1.")
            results.append({"source_id": src["id"], "status": status, "items": 0, "message": msg, "checked_at": checked_at})
            continue
        try:
            got = parse_feed(getter(url), src["id"], checked_at)
            for it in got:   # sommige feeds (o.a. DIVD) geven relatieve links: maak ze volledig
                it["url"] = urljoin(src.get("url") or url, it["url"])
            items.extend(got)
            results.append({"source_id": src["id"], "status": "ok", "items": len(got), "message": f"{len(got)} items via {url}", "checked_at": checked_at})
        except urllib.error.HTTPError as e:
            results.append({"source_id": src["id"], "status": "failed", "items": 0, "message": f"HTTP {e.code} bij {url}", "checked_at": checked_at})
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            reason = getattr(e, "reason", e)
            results.append({"source_id": src["id"], "status": "failed", "items": 0, "message": f"Niet bereikbaar: {reason}", "checked_at": checked_at})
        except ValueError as e:
            results.append({"source_id": src["id"], "status": "failed", "items": 0, "message": f"Feed onleesbaar: {e}", "checked_at": checked_at})

    attempted = [r for r in results if r["status"] in ("ok", "failed")]
    ok = [r for r in attempted if r["status"] == "ok"]
    if attempted and len(ok) == len(attempted):
        mode, note = "live", "Alle feeds zijn opgehaald."
    elif ok:
        mode, note = "partial", f"{len(ok)} van {len(attempted)} feeds opgehaald; zie bronstatus."
    else:
        mode, note = "failed", "Geen enkele feed kon worden opgehaald."
    return ProviderResult(items=items, source_results=results, mode=mode, note=note)
