# CyberScope

Een persoonlijke nieuwsapp over cybersecurity, in begrijpelijk Nederlands. CyberScope vertelt niet alleen **wat** er gebeurt, maar legt uit **hoe het technisch werkt**: na elk stuk moet de lezer iets nieuws begrijpen.

Per ontwikkeling beantwoordt CyberScope, waar het kan:

1. Wat is er gebeurd?
2. Wat is de technologie, en wat gaat er technisch fout?
3. Hoe kan een aanvaller dit misbruiken?
4. Wat is de impact, en hoe zie en voorkom je het (SIEM, vulnerability management, threat intelligence)?
5. Wat betekent dit voor je werk, en welke vragen stel je een klant?
6. Wat moet je onthouden?

CyberScope is gebouwd op de code van de [Data & AI Radar](https://github.com/tomasr91/data-ai-radar): zelfde opzet, opmaak en werking, zonder het tabblad Leren, met een eigen profiel, eigen bronnen en een artikelopbouw voor securityonderwerpen.

## Structuur

```
README.md                    ← dit bestand
context/
  profile.md                 ← voor wie, kennisniveau, uitlegstijl, leerpad
  werkcontext.md             ← werkomgeving van de lezer, klantvragen, grenzen
  interests.yml              ← onderwerpen, prioriteiten, verdeling, regio-voorrang, uitsluitingen
  verdieping.yml             ← ideeënlijst voor verdiepingen (leerpad in vier fasen)
  sources.yml                ← nieuwsbronnen en hun betrouwbaarheid
  editorial-guide.md         ← schrijfstijl, artikelopbouw, betrouwbaarheid, veiligheid
  app.yml                    ← wie via GitHub-issues feedback en keuzes mag insturen
taken/                       ← werkinstructies voor de vier nachttaken (begin bij REGELS.md)
pipeline/                    ← ophalen → normaliseren → ontdubbelen → verrijken → scoren
scripts/                     ← controles, site bouwen, issues verwerken
data/                        ← feed, archief, uitleg per artikel, verdiepingen (schrijft de pipeline/Claude)
app/                         ← de mobiele app (index.html) en PWA-bestanden
tests/                       ← unit tests en end-to-end tests (fixtures: vaste testconfiguratie)
.github/workflows/radar.yml  ← elke nacht ophalen, feed bouwen, app publiceren
```

## Zo werkt het elke nacht

1. **01:37 – GitHub Actions** (`.github/workflows/radar.yml`) haalt de feeds op, bouwt `data/feed.json` en zet de beste onverwerkte artikelen op de werklijst `data/to_enrich.json`. De app op GitHub Pages wordt bijgewerkt.
2. **Daarna – vier geplande Claude-taken** (02:22 uitleggen, 03:22 verdiepen, 04:22 overzicht, 05:37 inhalen), elk met een eigen instructie in `taken/`. Claude leest elk artikel volledig, zoekt bij technische onderwerpen de primaire bron op en schrijft de uitleg in `data/enrichment/`.
3. **Na elke push** van Claude draait de workflow opnieuw; de nieuwe uitleg staat dan in de app.

Alleen artikelen die Claude heeft uitgelegd komen in de app. Een fout uitlegbestand komt er nooit in: de pipeline negeert het en meldt het onder Status.

## Wat CyberScope toevoegt aan de Data & AI Radar

- **Artikelopbouw voor security** (`context/editorial-guide.md` §2): korte stukken voor gewoon nieuws, uitgebreide stukken met vaste onderdelen (technologie · wat gaat fout · misbruik · impact · hoe zie je dit · hoe voorkom je dit) als er iets te leren valt. Plus klantvragen, "Bevestigd", "Nog onbekend of onzeker" en "Onthoud".
- **Urgentie bij kwetsbaarheden**: labels *actief misbruikt*, *aanvalscode openbaar*, *patch beschikbaar*, *nog geen patch*.
- **Regio-voorrang**: Nederland, dan Benelux, Europa, Noord-Amerika, de rest van de wereld (`scoring.region_bonus` in `interests.yml`).
- **Leveranciersneutraal**; nieuws over leveranciers alleen bij groot nieuws (`security_market`, prioriteit 1).
- **Uitleg, geen handleiding**: geen werkende aanvalscode (redactiegids §4).
- Eigen opslag (`cyberscope:*`) en caches in de browser, zodat CyberScope en de Data & AI Radar elkaar niet raken (ze delen het adres `tomasr91.github.io`).
- Eigen accentkleur (cyaan) en icoon.

## Eenmalig instellen

1. **Settings → Pages → Source: GitHub Actions.**
2. **Settings → Actions → General → Workflow permissions: Read and write.**
3. **Actions → Radar bijwerken → Run workflow** voor de eerste run. Daarna staat de app op `https://tomasr91.github.io/cyber-radar/`.
4. **De lezer feedback laten geven:** duimpjes, keuzes voor verdiepingen en wijzigingen in interesses gaan als GitHub-issue naar deze repository. Alleen issues van de eigenaar en van de namen in `context/app.yml` (`issue_authors`) tellen. Heeft de lezer een GitHub-account, zet die naam daar.
5. **Geplande taken** (Claude): vier taken, elk met deze opdracht (met `<TAAK>` = UITLEGGEN, VERDIEPEN, OVERZICHT of INHALEN):

> Voeg de GitHub-repository `tomasr91/cyber-radar` toe met push-toegang en clone hem. Lees `taken/REGELS.md` en voer daarna `taken/<TAAK>.md` uit. Wijzig alleen de bestanden die in REGELS.md staan.

**Let op:** de repository is openbaar. Alles in `context/` (ook het profiel) en alle issues zijn voor iedereen te lezen. Zet er geen klantnamen of interne informatie in.

## Lokaal gebruiken

```bash
pip install -r requirements.txt
python scripts/validate_context.py          # context controleren
python -m pipeline.build --provider feeds   # live ophalen (netwerk nodig)
cp data/feed.json app/feed.json
python -m http.server -d app 8000           # bekijk op http://localhost:8000
```

**Testen:** `python -m unittest discover -s tests -t .`, `python tests/e2e_app.py` en `python tests/e2e_cyber.py` (vereist `pip install playwright`).

## Handmatig wijzigen

- **Onderwerp toevoegen of zwaarder maken:** `context/interests.yml` (`topics`, `priority` 1–5). Uitzetten met `enabled: false`.
- **Bron toevoegen:** `context/sources.yml`, met `region` (nl, benelux, eu, na, world). Nog niet gecontroleerd? `status: to_verify` en `enabled: false`.
- **Verdieping toevoegen:** `context/verdieping.yml`.
- Daarna altijd: `python scripts/validate_context.py`.

### Relevantiescore

`score = 55% onderwerp + 20% inhoudelijke kwaliteit + 15% actualiteit + 10% bron`, plus regio-voorrang, de duimpjes van de lezer en Claudes inschatting "past bij jou". Onder `min_relevance_score` komt niets in de feed. Details staan bovenaan `pipeline/score.py`.

## Wat nog ontbreekt

Zie de `[aanvullen]`- en `[aanname]`-labels in `context/`. De belangrijkste:

- **Profiel:** hoeveel tijd per dag er is om te lezen.
- **Werkcontext:** belangrijkste sectoren en landen van de klanten.
- **Bronnen:** de feedadressen worden bij de eerste run gecontroleerd (Status in de app). Nog toe te voegen: Eye Security, Northwave en het Belgische CCB, als ze een feed hebben (`Actions → Feeds zoeken`).
