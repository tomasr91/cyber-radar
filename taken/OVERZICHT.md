# Taak 3: overzicht (04:22)

Lees eerst `taken/REGELS.md`. Deze taak doet alles wat over de feed als geheel gaat.

## Stappen

1. **Context lezen.** `context/profile.md`, `context/werkcontext.md`, `context/editorial-guide.md`, `context/interests.yml`, `data/feedback.json`. `git pull` zodat je de uitleg van vannacht hebt.
2. **Trends.** Werk `data/trends.json` bij volgens **Trends** hieronder (een lege lijst mag). Opslaan, commit `Trends`.
3. **Interesses.** Draai `python scripts/interest_requests.py` en verwerk elke `VERWERKEN`-regel volgens **Mijn interesses** hieronder (wachtrij `data/interest_requests.json` daarna leeg: `{"requests": []}`). Bij `NIET NU`, `GEEN VERZOEKEN` of `ONBEKEND`: niets aan `context/interests.yml` veranderen. Opslaan, commit `Interesses aangepast` (met `Closes #n` voor losse issues).
4. **Begrippen aanvullen.** Hooguit 15 bestaande uitleg- of verdiepingsbestanden zonder `terms`, volgens **Begrippen** hieronder. Opslaan, commit `Begrippen aangevuld`.
5. **Alleen op zondag** (datum in Europe/Amsterdam):
   - `data/weekly.json` volgens **Jouw week** hieronder.
   - hooguit 3 voorstellen in `data/interest_suggestions.json` volgens **Mijn interesses** (voorstellen doen).
   - Opslaan, commit `Jouw week`.
6. **Afronden.** Taakverslag `data/runs/<datum>-overzicht.json` en opslaan.

## Trends

Een trend is een ontwikkeling of techniek waar nu meerdere bronnen tegelijk over schrijven, bijvoorbeeld "aanvallers misbruiken VPN-servers van één leverancier op grote schaal" of "phishing die MFA omzeilt via gestolen sessies". Geen breed onderwerp als "ransomware" of "phishing".

- Kijk naar de uitgelegde artikelen in `data/feed.json` van de **laatste 21 dagen**.
- Een trend heeft **minstens 3 artikelen uit minstens 2 bronnen**. Hooguit **3 trends**; liever geen trend dan een geforceerde.
- `title`: hooguit 80 tekens, zegt wat er speelt. `summary`: 2 of 3 korte zinnen: wat is de gemeenschappelijke lijn, en waarom komt het nu op. Alleen wat in de artikelen staat.
- Een trend van gisteren die nog klopt, houd je met hetzelfde `id` en vul je aan.

```json
{
  "format_version": 1,
  "generated_at": "2026-10-30T06:20:00Z",
  "trends": [
    {"id": "misbruik-vpn-servers", "title": "...", "summary": "...", "article_ids": ["<id>", "<id>", "<id>"], "topics": ["edge_devices"]}
  ]
}
```

## Mijn interesses

De lezer ziet in de app (tandwiel > Mijn interesses) de onderwerpen uit `context/interests.yml`, jouw voorstellen en een logboek. Wat de lezer wil veranderen komt als issue "Interesses: ..." binnen; `scripts/interest_requests.py` zet het om in een lijst. Je mag hiervoor **alleen** `context/interests.yml`, `data/interest_suggestions.json` en `data/interest_log.json` aanpassen; nooit het profiel, de bronnen of andere contextbestanden.

**Verzoeken verwerken (stap 3)**
- `onderwerp <id>: belangrijker` → `priority` één omhoog (hooguit 5). `minder` → één omlaag (minstens 1). `weg` → `enabled: false` (het onderwerp blijft staan, zodat het terug kan). `leren` → `learning: true` (leeronderwerp: geel lampje op de kaarten, uitleg bij de basis beginnen); `niet_leren` → haal `learning` weg. `volgen` → `follow: true` (altijd volgen: feedback duwt het niet omlaag, minstens één artikel per week als er iets verscheen); `niet_volgen` → haal `follow` weg.
- `voorstel <id>: JA` → voer het voorstel uit. Bij `nieuw`: voeg een onderwerp toe onder `topics` met een `id` in snake_case, `name`, `description` (2 of 3 zinnen), een bestaande `feed_group`, `enabled: true`, `priority: 3` (tenzij het voorstel iets anders zegt), 5 tot 15 specifieke `keywords` (geen losse woorden die ook in andere teksten staan) en `related_topics`; zet het `id` ook bij het passende gebied in `interest_areas`. Bij `belangrijker`/`minder`/`weg`: zoals hierboven.
- `voorstel <id>: NEE` → niets veranderen.
- Haal elk beantwoord voorstel (ja of nee) uit `data/interest_suggestions.json`.
- `in eigen woorden`: vertaal het naar concrete aanpassingen in `interests.yml` (prioriteit, zoekwoorden, omschrijving, `excluded_topics`). Is het onduidelijk of valt het buiten `interests.yml` (bijv. een nieuwe bron), verander dan niets en schrijf dat in het logboek.
- Zet `updated:` bovenin `interests.yml` op de datum van vandaag.
- Draai `python scripts/validate_context.py`. Bij een fout: herstel het, of zet `interests.yml` terug en meld het.
- Schrijf per wijziging één regel bovenaan `data/interest_log.json` (nieuwste eerst), in gewoon Nederlands:
  `{"changes": [{"at": "2026-11-04T03:40:00Z", "text": "Ransomware: van 'belangrijk' naar 'kern' (jouw verzoek)."}, ...]}`
  Ook een afgewezen voorstel krijgt een regel ("Voorstel 'OT-beveiliging' niet overgenomen (jouw nee)."), zodat je het niet snel opnieuw voorstelt.
- Zet `Closes #<n>` voor elk verwerkt issue in de commitboodschap.

**Voorstellen doen (stap 5, alleen op zondag)**
- Hooguit 3, en vervang de vorige (onbeantwoorde) voorstellen. Liever geen voorstel dan een zwak voorstel; een lege lijst mag.
- Soorten (`kind`): `nieuw` (een onderwerp dat er nog niet is), `belangrijker`, `minder` of `weg` (een bestaand onderwerp, met `topic`).
- Baseer je op: de duimpjes, redenen en gelezen artikelen van de lezer (`data/feedback.json`, laatste 4 weken); onderwerpen die vaak in het nieuws of in de werklijst zitten maar niet goed in `interests.yml` passen; overgeslagen artikelen; de leerdoelen in `context/profile.md`.
- `why`: één zin met het concrete bewijs ("kwam deze maand in 5 artikelen terug; 2 daarvan gaf je een 👍"). Verzin geen cijfers.
- Stel niets voor wat de lezer in de laatste 8 weken heeft afgewezen (zie `data/interest_log.json`).

```json
{
  "generated_at": "2026-11-08T04:40:00Z",
  "suggestions": [
    {"id": "ot-beveiliging", "kind": "nieuw", "name": "Beveiliging van industriële systemen (OT)", "description": "...", "why": "..."},
    {"id": "ransomware-belangrijker", "kind": "belangrijker", "topic": "ransomware", "why": "..."}
  ]
}
```

## Begrippen: `terms`

Volg **Begrippen** in `taken/UITLEGGEN.md`.

**Aanvullen (elke run, na de werklijst):** uitlegbestanden van artikelen die nu in de app staan (`articles` in `data/feed.json`) maar nog geen `terms` hebben: voeg ze toe, hooguit 15 per run, nieuwste eerst. Verander verder niets aan die bestanden. Hetzelfde voor verdiepingen zonder `terms`. Noem het aantal in de melding.

## Jouw week (alleen op zondag)

Een kort overzicht dat de lezer zondagochtend leest om de week af te sluiten. De app zet er zelf de quizscores, herhaalvragen en wat er gelezen is bij; jij schrijft alleen de inhoud.

- Kijk naar de uitgelegde artikelen in `data/feed.json` die de afgelopen 7 dagen in de app kwamen (`processed_at`), en naar de verdiepingen van die week.
- Kies de **3 belangrijkste ontwikkelingen** van de week: wat moet de lezer weten voor gesprekken met klanten, en wat was technisch het leerzaamst. Liever iets dat in meerdere artikelen terugkomt dan één losse melding. Minder dan 3 mag in een rustige week.
- `title`: hooguit 90 tekens, de ontwikkeling zelf. `why`: 2 korte zinnen, wat het is en wat het voor de lezer betekent. Alleen wat in de artikelen staat.
- `article_ids`: 1 tot 3 artikelen waar het in staat.
- `intro`: één zin over de week als geheel.
- `focus` (optioneel): één concreet ding voor deze week, bijv. een vraag om met een klant te bespreken of een verdieping om te lezen. Geen klantnamen.
- Begrijpelijk Nederlands, zoals in de redactiegids.

```json
{
  "week": "2026-W45",
  "generated_at": "2026-11-08T03:40:00Z",
  "intro": "...",
  "highlights": [
    {"title": "...", "why": "...", "article_ids": ["<id>", "<id>"]}
  ],
  "focus": "..."
}
```

`week` is de ISO-week van de zondag zelf (`date +%G-W%V`).
