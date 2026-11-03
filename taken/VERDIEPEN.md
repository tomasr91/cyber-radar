# Taak 2: verdiepingen en keuzes voor morgen (03:22)

Lees eerst `taken/REGELS.md`. Deze taak schrijft de verdieping die de lezer gisteren koos (en eigen voorstellen) en zet 5 nieuwe keuzes klaar.

## Stappen

1. **Context lezen.** `context/profile.md` (vooral §2 en het leerpad in §6), `context/werkcontext.md`, `context/editorial-guide.md`, `context/verdieping.yml`, de onderwerpen en `interest_areas` in `context/interests.yml`, en `data/feedback.json`.
2. **Wat schrijven?** Draai `python scripts/next_deepdive.py`:
   - `NIET NU`: geen verdieping en **geen** nieuwe keuzes. Schrijf alleen het taakverslag ("niet in de nacht gestart") en stop.
   - `SCHRIJVEN: <id> (issue #n)`: schrijf die verdieping volgens **Verdiepingen** hieronder. Er kunnen er meerdere zijn: de gewone keuze en hooguit 2 eigen voorstellen (zie **Eigen onderwerp**). Schrijf ze allemaal.
   - `AL GESCHREVEN`: niets schrijven; sluit het issue met `Closes #n` in een commit.
   - `ONBEKENDE KEUZE`: niets schrijven; zet het in het taakverslag.
   - `LATER`: komt een volgende nacht; niets doen.
   - `GEEN KEUZE` of `ONBEKEND`: vandaag geen verdieping.
3. **Na elke verdieping opslaan** (REGELS: tussendoor opslaan). Commit `Verdieping: <id>` met `Closes #<n>` op een eigen regel.
4. **Nieuwe keuzes.** Maak 5 nieuwe keuzes in `data/deepdive_options.json` volgens **Dagelijkse keuzes** hieronder. Opslaan, commit `Keuzes voor morgen`.
5. **Afronden.** Taakverslag `data/runs/<datum>-verdiepen.json` (in `counts`: `verdiepingen` en `keuzes`) en opslaan.

## Verdiepingen

Een verdieping is een langer stuk over één onderwerp uit het leerpad: hoe iets technisch werkt. De lezer heeft basiskennis, dus **begin bij de basis**: wat is het, waarom bestaat het, een vergelijking uit het dagelijks leven, en dan pas de details. Leg eerst uit hoe iets normaal werkt, dan wat er mis kan gaan. De `question` en `why` van de gekozen keuze bepalen waar het stuk over gaat.

### Eigen onderwerp (`eigen-...`)

De lezer kan in de app zelf iets op "Jouw lijst" zetten en daar een verdieping van laten maken. Het script meldt dan `SCHRIJVEN: eigen-<slug>` met `"own": true`, de `title` (het onderwerp in de woorden van de lezer), soms een `question` (een notitie) en `seen_in` (waar het gelezen werd).

- Schrijf over precies dat onderwerp; de notitie zegt waar de lezer benieuwd naar is. Ontbreekt die, beantwoord dan: wat is het, hoe werkt het technisch, hoe ziet een securityteam het, en wat betekent het voor klanten.
- Zoek het op in actuele, betrouwbare bronnen; verzin niets. Bestaat het onderwerp niet of kun je er niets betrouwbaars over vinden, schrijf dan niets en meld het.
- `id` en `plan_id` zijn de `eigen-...`-sleutel uit het script; ook de bestandsnaam.

### Dagelijkse keuzes

Elke run zet je 5 nieuwe keuzes klaar. De lezer kiest er in de app één; die schrijf je de volgende nacht.

- **Waar komen ze vandaan?** Combineer:
  - het nieuws van de afgelopen dagen (`data/feed.json` en de werklijst): wat roept een "hoe werkt dat eigenlijk?"-vraag op (bijv. na een artikel over een webshell: "Wat is een webshell en hoe vind je hem?");
  - het leerpad (`context/profile.md` §6) en de ideeënlijst in `context/verdieping.yml`;
  - de interessegebieden en hun richtverdeling in `context/interests.yml` (`interest_areas`).
- **Trends:** is er een trend in `data/trends.json`, maak dan van minstens één trend een keuze (`why` noemt de trend).
- **Basis eerst:** staan er in `context/verdieping.yml` open onderwerpen uit fase 1 of 2 (`level: beginner`, nog geen verdieping over geschreven), neem er dan elke dag minstens één als keuze op, met hetzelfde `id`. Zo bouwt de lezer stap voor stap de basis op.
- **Spreiding:** de 5 keuzes komen uit minstens 3 verschillende interessegebieden. Zet het gebied in `area`.
- **Vers:** niet iets waar al een verdieping over is (`data/deepdives/`), en niet dezelfde 5 als gisteren. Een keuze die gisteren niet is gekozen mag terugkomen, maar hooguit 2 per dag.
- **Afwisseling:** bijvoorbeeld één basisbegrip, één aanvalstechniek, één onderwerp uit het nieuws, één onderwerp over detectie of vulnerability management.
- **Per keuze:**
  - `id`: korte sleutel, kleine letters en koppeltekens (bijv. `wat-is-een-webshell`). Wordt later de bestandsnaam.
  - `title`: hooguit 80 tekens, Nederlands, zegt waar het over gaat.
  - `question`: de vraag die de verdieping beantwoordt.
  - `why`: één zin waarom dit nu interessant is (bijv. een artikel van deze week).
  - `topics`: 1 tot 3 id's uit `interests.yml`. `area`: id uit `interest_areas`.
- **Bestand:** verplaats de keuzes van gisteren naar `history` (bewaar hooguit de laatste 60) en zet de nieuwe in `options`:

```json
{
  "format_version": 1,
  "generated_at": "2026-11-04T02:30:00Z",
  "options": [
    {"id": "wat-is-een-webshell", "title": "...", "question": "...", "why": "...", "topics": ["attack_techniques"], "area": "techniek"}
  ],
  "history": []
}
```

### Actualiteit en betrouwbaarheid

- Schrijf alleen wat **nu** klopt. Gebruik bij voorkeur bronnen van de laatste twaalf maanden; een oudere bron alleen voor een basisidee dat nog steeds klopt, en dan naast een recente bron.
- Lees 2 tot 5 goede bronnen volledig: officiële bronnen (NCSC, CISA, MITRE ATT&CK, OWASP), technisch onderzoek (zie `context/sources.yml`) of erkende vakmensen. Geen marketing.
- Verzin niets. Elk feit, getal en elke naam komt uit een bron die je hebt gelezen.
- Gebruik een actueel voorbeeld uit het nieuws als dat er is, en maak duidelijk wat daarvan bevestigd is.
- Zet de gelezen bronnen in `further_reading`, met per bron in één zin waarom hij het lezen waard is. Alleen links die je zelf hebt geopend.
- Schrijf in `currency_check` kort hoe je de actualiteit gecontroleerd hebt: op welke datum en uit welke periode de bronnen komen.

### Uitleg, geen handleiding

Een verdieping legt uit hoe een aanval werkt, wat je ervan ziet en hoe je je beschermt. Geen werkende aanvalscode, geen uitvoerbare stappen, geen instructies om detectie te omzeilen (redactiegids §4).

### Opbouw

- Schrijf volgens de redactiegids (§1: begrijpelijk Nederlands, korte zinnen, begrip uitleggen vóór je het gebruikt, één vergelijking per nieuw begrip).
- 5 tot 7 onderdelen (`sections`), elk met een korte kop en 2 tot 4 alinea's. Samen 6 tot 10 minuten lezen. Een logische lijn is: wat is het en waarom bestaat het · hoe werkt het normaal · wat gaat er mis en hoe misbruikt een aanvaller dat · een echt voorbeeld · hoe ziet een securityteam het (SIEM, logs, EDR) · hoe voorkom je het (vulnerability management, maatregelen) · wat betekent het voor klanten.
- `takeaway`: de belangrijkste les in één of twee zinnen.
- `limitations`: 2 tot 4 korte zinnen over wat het stuk niet behandelt, waar experts het oneens zijn, of wat onzeker is.
- `experiment` (optioneel): iets kleins dat de lezer zelf kan doen zonder risico, bijv. "Open in je browser de ontwikkelaarstools en bekijk de HTTP-verzoeken als je een website opent." Nooit iets uitproberen op systemen van anderen.
- `showcase`: volgens **Zien** in `taken/UITLEGGEN.md`, als het onderwerp zich ervoor leent.
- `terms`: volgens **Begrippen** in `taken/UITLEGGEN.md` (hooguit 8).
- `quiz`: **3 controlevragen** over de kern van het stuk, zodat de lezer merkt of het is blijven hangen. Per vraag 3 of 4 antwoorden, precies één goed (`answer` is de index, vanaf 0), en een `explanation` van 1 of 2 zinnen. Vraag naar begrip (waarom, wat gebeurt er, wat zie je), niet naar losse namen of getallen. De foute antwoorden zijn geloofwaardig, maar volgens het stuk echt fout. Zet het goede antwoord niet steeds op dezelfde plek.

### Formaat van `data/deepdives/<id>.json`

Gebruik de `id` van de gekozen keuze als bestandsnaam, `id` en `plan_id`.

```json
{
  "format_version": 1,
  "id": "<id van de gekozen keuze>",
  "plan_id": "<id van de gekozen keuze>",
  "request_issue": 12,
  "headline": "Nederlandse kop, hooguit ongeveer 70 tekens",
  "summary": "Twee of drie zinnen voor de kaart en de opening.",
  "sections": [{"heading": "Korte kop", "paragraphs": ["Alinea.", "Alinea."]}],
  "takeaway": "De les in één of twee zinnen.",
  "limitations": ["Korte zin"],
  "further_reading": [{"label": "Titel (auteur of organisatie, maand jaar)", "url": "https://...", "note": "Waarom lezen."}],
  "quiz": [{"question": "Vraag?", "options": ["A", "B", "C"], "answer": 1, "explanation": "Waarom B klopt."}],
  "currency_check": "Gecontroleerd op <datum>: ...",
  "topics": ["<1 tot 4 id's uit interests.yml>"],
  "terms": [{"term": "Zoals in de tekst", "explanation": "Eén of twee korte zinnen."}],
  "written_at": "2026-11-04T02:30:00Z",
  "processed_by": "Claude (geplande taak)",
  "prompt_version": "verdieping-v2"
}
```

## Feedback van de lezer

Gebruik `data/feedback.json` zoals beschreven in `taken/UITLEGGEN.md` (**Feedback van de lezer**). Onderwerpen met `nieuw_voor_mij` of `meer_hiervan` neem je vaker mee in de keuzes.
