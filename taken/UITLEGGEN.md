# Taak 1: artikelen uitleggen (02:22)

Lees eerst `taken/REGELS.md`. Deze taak schrijft per nieuw artikel de uitleg die de app toont (Actueel). Dit is het hart van CyberScope: niet alleen vertellen wat er gebeurde, maar uitleggen hoe het technisch werkt.

## Stappen

1. **Vers ophalen afdwingen.** Kijk naar `generated_at` in `data/feed.json`. Is die niet van vandaag (UTC), schrijf dan de datum van vandaag (`date -u +%F`) in `data/run-request`, commit alleen dat bestand ("Ophalen aangevraagd <datum>") en push. Wacht daarna tot `data/feed.json` van vandaag is: elke 30 seconden `git pull`, hooguit 10 minuten. Lukt het niet, ga door met de werklijst die er is en zet dat in het taakverslag.
2. **Context lezen.** `context/profile.md`, `context/werkcontext.md`, `context/editorial-guide.md` en de onderwerp-id's in `context/interests.yml`. De redactiegids is leidend. Lees ook `data/feedback.json` (zie **Feedback van de lezer**) en `data/taste.json` (zie **Past bij de lezer**).
3. **Werklijst.** Open `data/to_enrich.json`. Is `items` leeg: schrijf het taakverslag ("niets te verwerken") en stop.
4. **Kiezen.** Lees de hele werklijst eerst door. Zitten er meerdere artikelen over dezelfde ontwikkeling in (bijv. dezelfde CVE of hetzelfde incident bij drie nieuwssites)? Leg dan **één** uit, het liefst de bron met de meeste technische inhoud of een Nederlandse bron, en sla de andere over met reden "zelfde ontwikkeling als <id>". Gebruik voor alle artikelen over dezelfde ontwikkeling dezelfde `development_key`.
5. **Per artikel** (in volgorde, **maximaal 15**):
   1. Open de `url` en lees het **volledige artikel**. Nooit alleen op titel of `excerpt`.
   2. Niet te lezen (betaalmuur, fout, geen inhoud)? Schrijf `data/enrichment/skipped/<id>.json` met `{"article_id", "url", "reason", "checked_at"}` en ga door. Begin `reason` dan met "Niet te lezen": zo'n artikel komt na een week nog één keer terug op de werklijst.
   3. Valt het onder **Niet uitleggen**? Ook een `skipped`-bestand, met de regel als `reason`.
   4. Gaat het over een kwetsbaarheid of een technische aanval? **Zoek de primaire bron op** (advies van de leverancier, CISA, NCSC, NVD, het onderzoek zelf) en lees die ook. Technische details komen uit de primaire bron; zet die in `official_docs`.
   5. Kies de lengte (redactiegids §2): **kort** bij nieuws met weinig technische diepgang, **uitgebreid** (met `sections`) als er iets te leren valt. Richtlijn: ongeveer de helft van de artikelen uitgebreid.
   6. Schrijf `data/enrichment/<id>.json` volgens **Formaat** hieronder, met begrippen (`terms`) en waar het past een `showcase`.
   7. **Na elke 5 artikelen opslaan** (zie REGELS: tussendoor opslaan), commit `Uitleg: <aantal> artikelen`.
6. **Aanvullen.** Staan er artikelen in `data/to_tag.json`: zet in hun `data/enrichment/<id>.json` alleen de ontbrekende velden `soort` en/of `fit` (de rest niet aanraken). Hooguit 20, opslaan met commit `Soort en fit: <aantal> artikelen`.
7. **Afronden.** Laatste artikelen opslaan, taakverslag `data/runs/<datum>-uitleggen.json` schrijven en opslaan.

## Wat maakt een goede uitleg?

De lezer heeft basiskennis en wil de techniek leren. Na het lezen moet de lezer **iets nieuws begrijpen**. Controleer per artikel:

- Is de **normale werking** uitgelegd voordat de fout aan bod komt? ("Een webserver ontvangt verzoeken van browsers en stuurt pagina's terug…")
- Is elk nieuw begrip uitgelegd **vóór** het gebruikt wordt (in de tekst of als `term`)?
- Staat er **waarom** het gevaarlijk is, niet alleen dát?
- Is de koppeling gelegd met **SIEM** (wat zie je in de logs?), **vulnerability management** (hoe vind je kwetsbare systemen, hoe urgent is het?) en **threat intelligence** (wordt het misbruikt, door wie?), waar dat past?
- Zijn **feiten, vermoedens en mogelijkheden** gescheiden?
- Zijn er **klantvragen** die een Customer Success Manager echt zou stellen?

### Uitgebreid: vaste onderdelen
`story` = "Wat is er gebeurd?" (1 of 2 alinea's). Daarna `sections` met deze koppen, in deze volgorde. Laat een onderdeel weg als de bronnen er niets over zeggen.

1. `Wat is de technologie?`
2. `Wat gaat er technisch fout?`
3. `Hoe kan een aanvaller dit misbruiken?`
4. `Wat is de mogelijke impact?`
5. `Hoe zie je dit?`
6. `Hoe voorkom je dit?`

Per onderdeel 1 tot 3 korte alinea's. "Hoe kan een aanvaller dit misbruiken?" blijft op begripsniveau: wat heeft de aanvaller nodig, wat gebeurt er, wat zijn de beperkingen. **Geen werkende aanvalscode of uitvoerbare stappen.**

### Kwetsbaarheden
- Zet altijd `exploitation` en `patch_status` (redactiegids §2). `actief_misbruikt` alleen als een betrouwbare bron het bevestigt (CISA KEV, NCSC, de leverancier, een onderzoeksteam dat het zelf zag); noem die bron in `key_facts`.
- Controleer actief misbruik zelf in de CISA KEV-lijst (https://www.cisa.gov/known-exploited-vulnerabilities-catalog) en, als die er is, de EPSS-score (https://www.first.org/epss/). De CISA-feeds zelf haalt de pipeline niet op (CISA weigert GitHub Actions).
- Leg uit waarom het wel of niet urgent is, verder dan de CVSS-score: misbruik, bereikbaar vanaf internet, inlog nodig of niet, wat de aanvaller daarna kan.
- Komt er openbare aanvalscode (bijv. een module voor een pentestframework zoals Metasploit)? Noem het en leg uit wat dat betekent voor het risico: misbruik wordt dan voor veel meer mensen eenvoudig.

### Incidenten
- Wat is **bevestigd** (en door wie), wat wordt **vermoed**, wat is **onbekend**? Onbekend hoort in `limitations`.
- Is de aanvalsmethode niet bekend: zeg dat. Je mag uitleggen hoe zulke aanvallen meestal verlopen, maar herkenbaar als algemene uitleg ("zulke aanvallen beginnen vaak met…").
- Claims van ransomwaregroepen zonder bevestiging: noem ze alleen als claim, met bron.
- Gaat het over een Nederlandse organisatie? Dat heeft voorrang (regio `nl`).

## Zien: `showcase`

De lezer leert het best als hij het ziet. Voeg waar het past een klein voorbeeld toe (bij artikelen én verdiepingen):

**`showcase` – "Zo ziet het eruit"**: bijvoorbeeld
- een regel uit een webserverlog of Windows-eventlog die laat zien hoe een aanval eruitziet (`log`);
- een HTTP-verzoek dat de normale werking of de aanval laat zien (`http`);
- een eenvoudige detectieregel (`sigma` of `kql`), regel voor regel uitgelegd in de caption;
- een kwetsbare en een veilige versie van een paar regels code (`sql`, `python`), alleen in leerboekvorm.

Regels:
- **Gebaseerd op de bron.** Staat er een voorbeeld in de bron of het advies, gebruik dat (ingekort). Bouw je iets na, zeg dat in `note` ("nagebouwd voorbeeld; de echte logregels staan in het advies").
- **Nooit werkende exploitcode of aanvalsscripts**, geen echte IP-adressen, domeinen of hashes van aanvallers. Gebruik voorbeeldadressen (`203.0.113.10`, `example.com`).
- Hooguit ongeveer 20 regels. Een `result`-tabel (hooguit 12 rijen) mag, bijv. wat een SIEM-zoekopdracht oplevert, met verzonnen data.

```json
"showcase": {"caption": "Zo ziet een poging tot SQL injection eruit in het log van een webserver. Let op het stukje na id=.", "language": "log",
             "code": "203.0.113.10 - - [03/Nov/2026:10:12:01 +0100] \"GET /product.php?id=1%27%20OR%20%271%27=%271 HTTP/1.1\" 200 5120",
             "note": "Nagebouwd voorbeeld met een voorbeeldadres."}
```

## Begrippen: `terms`

De lezer heeft basiskennis en komt veel nieuwe termen tegen. Geef bij elke uitleg (hooguit 6) en elke verdieping (hooguit 8) de begrippen die hij misschien nog niet kent. De app onderstreept ze in de tekst; tikken geeft de uitleg. Alle begrippen samen staan in het menu onder Begrippen. Zo bouwt de lezer een eigen woordenlijst op.

- **Welke:** vaktermen en afkortingen met een eigen betekenis (bijv. webshell, deserialisatie, laterale beweging, EDR, IOC, CVSS, EPSS, KEV, proof of concept, adversary-in-the-middle, sessietoken). **Niet** wat de lezer al kent (`profile.md` §2): cybersecurity, SIEM, vulnerability management, threat intelligence, kwetsbaarheid, hack, wachtwoord.
- **Letterlijk:** `term` staat precies zo in de tekst waarin de app onderstreept: in `story` of in de alinea's van `sections`. Anders keurt de controle het af.
- **Uitleg:** één of twee korte zinnen (hooguit 240 tekens), begrijpelijk Nederlands: wat het is en waarvoor het dient. Een vergelijking mag.
- **Zelfde uitleg:** staat het begrip al in `glossary` in `data/feed.json`, neem die uitleg over, tenzij hij niet klopt. Zo blijft de woordenlijst consistent.

```json
"terms": [{"term": "webshell", "explanation": "Een klein programma dat een aanvaller op een gehackte webserver zet. Het werkt als een achterdeur: via de browser kan hij daarna opdrachten geven aan de server."}]
```

## Niet uitleggen (overslaan met reden)

Let op de **ondergrens per gebied** (`min_articles` bij `interest_areas` in `interests.yml`): de werklijst zet artikelen uit gebieden die te weinig in de app hebben vooraan. Sla die niet over omdat ze minder spectaculair zijn; alleen om de regels hieronder.

CyberScope is **compact**. Sla deze artikelen over:

- **Dubbel nieuws**: een ontwikkeling die je al uitlegde (in deze run of eerder; zoek op `development_key` en CVE-nummer in `data/enrichment/`), tenzij er echt nieuwe informatie is.
- **Kleine kwetsbaarheden** in weinig gebruikte software, zonder misbruik en zonder iets bijzonders om van te leren.
- **NCSC- en CISA-adviezen** die alleen een lijst updates noemen, zonder kwetsbaarheid met hoge kans of hoge schade in veelgebruikte software.
- **Incidentnieuws zonder inhoud**: alleen "bedrijf X getroffen, onderzoek loopt", tenzij het een groot Nederlands of Benelux-incident is.
- **Onbevestigde claims** van ransomwaregroepen of hackers.
- **Marketing**: productaankondigingen, klantverhalen en "5 tips"-stukken van leveranciers, rapporten die vooral een download willen.
- **Leveranciersnieuws** (overnames, cijfers, personeel), tenzij het groot nieuws is: zet dan `exceptional: true`.
- Alles uit `excluded_topics`.

Twijfel je? Vraag je af: "Begrijpt de lezer na dit stuk iets nieuws over hoe cybersecurity werkt, of moet hij dit weten voor een klantgesprek?" Zo nee, overslaan.

## Feedback van de lezer

`data/feedback.json` bevat onder `reads` de artikelen die de lezer helemaal las (een licht positief signaal), en onder `votes` de duimpjes per artikel (`v`: 1 of -1) met soms een reden. De pipeline stuurt de score er al op bij. Gebruik het daarnaast zelf:

- Een duim omhoog is een sterk signaal. Gelezen is maar een benadering.
- Lees vóór het uitleggen de stemmen van de laatste 30 dagen. Kijk naar het soort artikel, niet alleen het onderwerp.

Redenen bij 👎:
- `te_basic`: leg minder basis uit bij dat soort onderwerp en ga sneller de diepte in.
- `te_vaag` (te vaag of te technisch): maak het concreter, met een voorbeeld, en leg meer stappen uit. Of sla het over als de bron zelf vaag is.
- `niet_mijn_stack` (niet relevant voor mijn werk) of `geen_interesse`: sla vergelijkbare artikelen vaker over.
- `oud_nieuws`: let beter op of iets echt nieuw is.

Redenen bij 👍:
- `praktisch` (handig voor klantgesprekken): maak de klantvragen en "wat betekent dit voor je werk" vaker concreet.
- `goed_uitgelegd`: lees de uitleg van dat artikel (`data/enrichment/<id>.json`) en houd die opbouw en dat niveau aan.
- `nieuw_voor_mij`: kies vaker artikelen die een nieuw concept of nieuwe techniek uitleggen; neem het onderwerp mee bij de verdiepingskeuzes.
- `mijn_stack` (past bij mijn werk): leg vaker de link naar SIEM, vulnerability management en threat intelligence.
- `meer_hiervan`: geef zulke artikelen voorrang en neem het onderwerp mee bij de verdiepingskeuzes.

## Past bij de lezer

`data/taste.json` bevat de laatste 20 duimpjes (met reden) en 10 gelezen artikelen, elk met titel, onderwerpen, bron en soort. Geef elk artikel dat je uitlegt een `fit`:

- `score` 0 tot 1: 0,5 = geen idee of neutraal, 0,8+ = lijkt sterk op de duimen omhoog, 0,2- = lijkt op de duimen omlaag. Telt hooguit 10 punten mee.
- `why`: één korte zin met de vergelijking, bijv. "Uitgebreide uitleg van een webkwetsbaarheid, zoals je PHP-artikel."
- Weinig duimen? Blijf dicht bij 0,5.

## Overige regels

- `key_facts` bevat **alleen feiten uit de bronnen**: CVE-nummers, getroffen versies, datums, cijfers, wie wat bevestigde. Elk feit dat in het verhaal staat, staat ook hier.
- `limitations` = **Nog onbekend of onzeker**: wat de bronnen (nog) niet zeggen, waar ze elkaar tegenspreken, en belangen van de bron.
- `personal_relevance`: één of twee zinnen over wat dit betekent voor het werk van een Customer Success Manager bij een securityleverancier.
- `customer_questions`: 2 tot 5 vragen die de lezer een klant kan stellen, bijv. "Weten jullie welke systemen deze software draaien?", "Hoe zien jullie of iemand dit al geprobeerd heeft?". Concreet bij dit onderwerp, geen verkoopvragen.
- `takeaway`: de belangrijkste technische les in één of twee zinnen. Niet het nieuws herhalen, maar wat de lezer moet onthouden over hoe het werkt.
- `region`: waar het nieuws over gaat: `nl`, `benelux`, `eu`, `na` of `world` (een wereldwijde kwetsbaarheid = `world`).
- `official_docs`: alleen links die je zelf hebt geopend (advies, CVE-pagina, onderzoek). Nooit zelf een URL opbouwen.
- `topics`: alleen id's uit `interests.yml`, de best passende eerst. Kies er 1 tot 4.
- `quality` (0 tot 1), wees streng:
  - `depth`: 0,2 = nieuwsbericht zonder technische details · 0,5 = enige uitleg · 0,8+ = technische oorzaak, aanvalsstappen of detectie concreet beschreven
  - `practicality`: hoe bruikbaar voor begrip en klantgesprekken
  - `novelty`: 0,2 = herhaling · 0,8+ = echt nieuw
- `development_key`: een korte sleutel voor de ontwikkeling, bij voorkeur met het CVE-nummer (bijv. `cve-2026-12345-fortios`) of de organisatie en maand (bijv. `hack-gemeente-x-nov-2026`).
- `date_note`: vul in als de datum twijfelachtig is.
- `article_type`: `nieuws` (standaard) of `opinie` (dan `author` verplicht).
- `soort`: `incident`, `kwetsbaarheid`, `onderzoek` (technische analyse van onderzoekers), `advies` (officieel advies of waarschuwing), `achtergrond` (uitleg van een concept) of `mening`.
- `exceptional: true` alleen bij groot, bevestigd nieuws (bijv. een grote overname in de securitymarkt, of een nieuwe wet die veel organisaties direct raakt).
- `availability_status` hoeft niet (dat is voor productnieuws); laat het weg.

## Formaat van `data/enrichment/<id>.json`

```json
{
  "format_version": 2,
  "article_id": "<id uit de werklijst>",
  "url": "<url uit de werklijst>",
  "headline": "Nederlandse kop, hooguit ongeveer 70 tekens",
  "summary": "Eén of twee zinnen voor de kaart in de lijst.",
  "story": ["Wat is er gebeurd? Alinea 1.", "Alinea 2."],
  "sections": [
    {"heading": "Wat is de technologie?", "paragraphs": ["..."]},
    {"heading": "Wat gaat er technisch fout?", "paragraphs": ["..."]},
    {"heading": "Hoe kan een aanvaller dit misbruiken?", "paragraphs": ["..."]},
    {"heading": "Wat is de mogelijke impact?", "paragraphs": ["..."]},
    {"heading": "Hoe zie je dit?", "paragraphs": ["..."]},
    {"heading": "Hoe voorkom je dit?", "paragraphs": ["..."]}
  ],
  "key_facts": ["Feit uit de bron met CVE-nummer, versie of datum.", "..."],
  "limitations": ["Wat nog onbekend is."],
  "personal_relevance": "Eén of twee zinnen: wat betekent dit voor je werk?",
  "customer_questions": ["Vraag aan een klant?", "..."],
  "takeaway": "De technische les in één of twee zinnen.",
  "region": "nl | benelux | eu | na | world",
  "exploitation": "actief_misbruikt | poc_openbaar | geen_misbruik_bekend | onbekend",
  "patch_status": "patch_beschikbaar | workaround | geen_patch | onbekend",
  "official_docs": [{"label": "Naam", "url": "https://..."}],
  "topics": ["vulnerabilities_cve", "web_software_security"],
  "quality": {"depth": 0.7, "practicality": 0.8, "novelty": 0.6},
  "development_key": "korte-sleutel",
  "date_note": "",
  "exceptional": false,
  "article_type": "nieuws",
  "soort": "incident | kwetsbaarheid | onderzoek | advies | achtergrond | mening",
  "fit": {"score": 0.5, "why": "Eén korte zin."},
  "showcase": {"caption": "...", "language": "log", "code": "...", "note": "..."},
  "terms": [{"term": "Zoals in de tekst", "explanation": "Eén of twee korte zinnen."}],
  "processed_by": "Claude (geplande taak)",
  "processed_at": "2026-11-04T01:40:00Z",
  "prompt_version": "cyber-taak-v1"
}
```

Korte artikelen hebben geen `sections`. `exploitation` en `patch_status` alleen bij kwetsbaarheden. `showcase` en `terms` alleen als ze iets toevoegen.
