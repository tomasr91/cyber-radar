# Gemeenschappelijke regels voor de nachttaken van CyberScope

CyberScope draait 's nachts in vier korte taken. Elke taak heeft een eigen bestand in `taken/`:

| Tijd (Nederland) | Taak | Bestand |
|---|---|---|
| 02:22 | Uitleggen: nieuwe artikelen | `taken/UITLEGGEN.md` |
| 03:22 | Verdiepen: verdieping(en) en 5 keuzes voor morgen | `taken/VERDIEPEN.md` |
| 04:22 | Overzicht: trends, interesses, begrippen aanvullen, zondag Jouw week | `taken/OVERZICHT.md` |
| 05:37 | Inhalen: alleen wat vannacht nog ontbreekt | `taken/INHALEN.md` |

Lees dit bestand en daarna alleen het bestand van jouw taak.

## Voor wie

CyberScope is voor **de lezer**: een Senior Customer Success Manager bij een cybersecurityleverancier, met basiskennis van cybersecurity, die wil begrijpen hoe het technisch werkt. Lees `context/profile.md` en `context/werkcontext.md` als je taak over inhoud gaat. In de app spreek je de lezer aan met "je".

## Altijd

- **Verzin niets.** Alleen wat in de bron, een officieel advies of de data staat. Weet je iets niet, laat het weg of zeg dat het onbekend is.
- **Geen technische claim zonder betrouwbare onderbouwing.** Controleer hoe iets technisch werkt bij een primaire bron (advies van de leverancier, CISA, NCSC, NVD, het onderzoek zelf).
- **Feiten, vermoedens en mogelijkheden** houd je altijd uit elkaar. Doe nooit alsof een aanvalsmethode is gebruikt als dat niet bevestigd is.
- **Uitleg, geen handleiding.** Geen werkende exploitcode, aanvalsscripts of uitvoerbare aanvalsstappen (redactiegids §4).
- **Geen klantnamen of interne informatie** van de werkgever. De repository is openbaar.
- **Geen sleutels of geheimen** in bestanden.
- Schrijf in begrijpelijk Nederlands, zoals in `context/editorial-guide.md`.
- Alles wat de lezer kiest, hoort pas de volgende ochtend in de app. Scripts die zeggen `NIET NU` volg je altijd.

## Welke bestanden je mag aanpassen

Alleen: `data/enrichment/`, `data/deepdives/`, `data/deepdive_options.json`, `data/trends.json`, `data/weekly.json`, `data/interest_suggestions.json`, `data/interest_log.json`, `data/interest_requests.json`, `data/runs/`, `data/run-request`, en (alleen bij verzoeken van de lezer in Overzicht) `context/interests.yml`. Nooit `app/`, `pipeline/`, `scripts/`, `.github/` of andere contextbestanden.

## Starten

1. `git pull` op `main`, daarna `pip install -r requirements.txt`.
2. Noteer de starttijd (UTC) voor het taakverslag.

## Tussendoor opslaan

Sla op na elk afgerond onderdeel, niet pas aan het eind. Zo blijft werk bewaard als de taak halverwege stopt:

1. `python scripts/validate_enrichment.py` moet `0 fout` geven. Los fouten eerst op.
2. `git add` alleen de bestanden van dat onderdeel, commit met een korte Nederlandse boodschap.
3. `git pull --rebase` en `git push`. Lukt de push niet, probeer het nog één keer na `git pull --rebase`.

## Taakverslag (altijd, ook als er niets te doen was)

Schrijf aan het eind `data/runs/<datum>-<taak>.json`, met de datum in Nederlandse tijd (`TZ=Europe/Amsterdam date +%F`) en `<taak>` = `uitleggen`, `verdiepen`, `overzicht` of `inhalen`:

```json
{"task": "uitleggen", "started_at": "2026-11-04T01:22:40Z", "finished_at": "2026-11-04T02:08:10Z",
 "status": "ok", "summary": "8 artikelen uitgelegd, 6 overgeslagen",
 "counts": {"uitgelegd": 8, "overgeslagen": 6}, "problems": []}
```

- `status`: `ok` (alles gedaan), `deels` (een deel lukte niet) of `mislukt`.
- `summary`: één zin in gewoon Nederlands; de app toont die op de pagina Status.
- `problems`: korte zinnen over wat niet lukte.
Sla het verslag op zoals hierboven (valideren, committen, pushen).

## Afsluiten

Geef een korte samenvatting in het Nederlands van wat je deed.
