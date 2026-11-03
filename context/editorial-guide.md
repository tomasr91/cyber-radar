---
id: editorial-guide
type: context
schema_version: 1
updated: 2026-11-03
---

# Redactiegids

Dit bestand bepaalt **hoe** CyberScope nieuws verwerkt en presenteert. **Wat** relevant is, staat in `interests.yml`; **voor wie**, in `profile.md` en `werkcontext.md`.

**Kern:** CyberScope vertelt niet alleen wat er gebeurt, maar legt uit hoe het technisch werkt. Na elk stuk moet de lezer iets nieuws begrijpen.

## 1. Schrijfstijl

- Begrijpelijk Nederlands ("Jip en Janneke-taal"), zonder dat de inhoud oppervlakkig wordt. Maak het niet eenvoudiger dan het is.
- **Korte zinnen**: gemiddeld 12 tot 15 woorden, nooit meer dan 25. Eén gedachte per zin.
- **Korte alinea's** van 2 tot 4 zinnen.
- **Actief en concreet**: wie doet wat. "De aanvaller stuurt een verzoek naar de webserver", niet "Er wordt een verzoek verstuurd".
- **Leg een begrip uit vóór je het gebruikt.** Eén keer, op de plek waar het voor het eerst voorkomt, het liefst met een vergelijking uit het dagelijks leven ("een webshell is een achterdeur die de aanvaller in de website achterlaat").
- Bouw op: **eerst eenvoudig, dan de techniek, dan een concreet voorbeeld, dan de betekenis voor organisaties.**
- Leg uit **waarom** iets gevaarlijk is, niet alleen dát het gevaarlijk is.
- Gebruik Nederlandse woorden waar die gangbaar zijn. Zet de Engelse vakterm bij het eerste gebruik tussen haakjes, bijv. "rechten verhogen (privilege escalation)". Gangbare Engelse termen (phishing, ransomware, malware) mag je gewoon gebruiken.
- Productnamen en CVE-nummers blijven zoals ze zijn.
- Geen marketingtaal, geen angstzaaierij ("apocalyptisch", "iedereen loopt gevaar"), geen overdreven claims.

**Zien:** waar het past krijgt een stuk een klein voorbeeld ("Zo ziet het eruit"): een logregel, een HTTP-verzoek, een detectieregel. Zie `taken/UITLEGGEN.md`.

## 2. Opbouw van een artikel

Er zijn twee lengtes. Kies wat het onderwerp vraagt: **kort waar het kan, uitgebreid waar het iets te leren valt.**

### Kort (nieuws met weinig technische diepgang)
- **Kop** (`headline`), **samenvatting** (`summary`), **verhaal** (`story`, 2 tot 4 alinea's): wat is er gebeurd, hoe werkt het, wat betekent het.
- **Onthoud** (`takeaway`): één of twee zinnen.

### Uitgebreid (een technisch onderwerp met leerwaarde)
Het verhaal (`story`) beantwoordt **Wat is er gebeurd?** (1 tot 2 alinea's). Daarna volgen de vaste onderdelen (`sections`), elk met precies deze kop. Laat een onderdeel weg als de bron er niets over zegt; verzin het niet.

1. **Wat is de technologie?** Welke software of infrastructuur is betrokken, en wat doet die normaal? Leg eerst de normale werking uit.
2. **Wat gaat er technisch fout?** De fout of de aanvalsmethode. Waarom is die fout gevaarlijk?
3. **Hoe kan een aanvaller dit misbruiken?** Stap voor stap, op begripsniveau: wat heeft de aanvaller nodig, welke toegang, welke techniek, wat gebeurt er als het lukt, wat zijn de beperkingen.
4. **Wat is de mogelijke impact?** Maak onderscheid tussen bevestigde impact, mogelijke impact en impact die afhangt van de situatie.
5. **Hoe zie je dit?** Welke signalen een securityteam kan zien: logs, SIEM, EDR, netwerkverkeer, threat intelligence.
6. **Hoe voorkom je dit?** Patchen, configuratie, toegang beperken, segmentatie, monitoring, detectieregels: alleen wat bij dit onderwerp past, met de reden erbij.

Daarna, bij beide lengtes:
- **Wat betekent dit voor je werk?** (`personal_relevance`): één of twee zinnen, plus **vragen die je een klant kunt stellen** (`customer_questions`, 2 tot 5).
- **Bevestigd** (`key_facts`): 3 tot 6 korte feiten uit de bron, met CVE-nummers, versies, datums en cijfers.
- **Nog onbekend of onzeker** (`limitations`): wat (nog) niet bekend is, of waar bronnen elkaar tegenspreken.
- **Onthoud** (`takeaway`): de belangrijkste technische les in één of twee zinnen.
- **Bron**: naam, publicatiedatum en link toont de app automatisch.

### Kwetsbaarheden: altijd de urgentie
Bij een kwetsbaarheid vul je twee velden die de app als label toont:
- `exploitation`: `actief_misbruikt` (bevestigd door bijv. CISA KEV, NCSC of de leverancier), `poc_openbaar` (aanvalscode is openbaar, misbruik nog niet bevestigd), `geen_misbruik_bekend` of `onbekend`.
- `patch_status`: `patch_beschikbaar`, `workaround` (alleen een tijdelijke maatregel), `geen_patch` of `onbekend`.

Leg uit **waarom** iets wel of niet urgent is, verder dan de CVSS-score: wordt het actief misbruikt, is het systeem bereikbaar vanaf internet, is er geen inlog nodig, wat kan de aanvaller daarna, hoe groot is de kans op misbruik (EPSS)?

### Incidenten: feiten, vermoedens, mogelijkheden
- Zeg wat **bevestigd** is (door de getroffen organisatie, een officiële instantie of onderzoekers die het zelf zagen).
- Zeg wat **vermoed** wordt, en door wie.
- Een aanvalsmethode die **mogelijk** is gebruikt, noem je alleen als mogelijkheid ("zo'n aanval verloopt vaak via…"). **Doe nooit alsof een methode is gebruikt als dat niet bevestigd is.**
- Is de oorzaak onbekend, zeg dat dan duidelijk. Het verhaal mag dan uitleggen hoe zulke incidenten meestal ontstaan, als dat herkenbaar als algemene uitleg is.

### Opiniestukken (`article_type: "opinie"`)
Een onderbouwde mening van een **erkende vakpersoon** (bekende onderzoeker, CISO, auteur, iemand van een officiële instantie) is welkom. Schrijf de mening altijd toe ("volgens …"). Noem belangen in `limitations`.

### Verdiepingen
Naast het nieuws (tabblad *Actueel*) schrijft CyberScope verdiepingen (tabblad *Verdieping*): langere stukken over een onderwerp uit het leerpad (`verdieping.yml`). Dezelfde stijl, met ruimte voor uitleg. Details in `taken/VERDIEPEN.md`.

### Dagelijks overzicht
- Compact: liever 3 goed uitgelegde stukken dan 10 korte berichten.
- Is er weinig relevant nieuws, dan een kortere feed. Niet aanvullen met minder relevante items.

## 3. Betrouwbaarheid

- **Verzin niets**: geen feiten, CVE-nummers, versies, aanvallersnamen, citaten of bronnen die niet in de bron staan.
- **Geen technische claim zonder betrouwbare onderbouwing.** Een nieuwssite (`trust_level: medium`) is genoeg voor *wat er gebeurde*, niet voor *hoe het technisch werkt*: zoek daarvoor de primaire bron op (advies van de leverancier, CISA, NCSC, NVD, het onderzoek zelf) en zet die in `official_docs`.
- **Herkomst blijft herleidbaar**: alles wat als feit in het verhaal staat, staat ook in `key_facts`. Interpretaties formuleer je herkenbaar als zodanig ("dat betekent dat…", "waarschijnlijk…").
- **Actueel**: gebruik de originele publicatiedatum. Gaat een artikel over iets ouds, meld dat of laat het weg.
- **Onzekerheid**: zeg het als bronnen elkaar tegenspreken of als iets nog onderzocht wordt.
- **Altijd** een link naar de oorspronkelijke bron.

## 4. Veiligheid: uitleg, geen handleiding

- Leg uit **hoe een aanval werkt, wat je ziet en hoe je je beschermt**. Geen werkende exploitcode, geen aanvalsscripts, geen stap-voor-stapinstructies die iemand direct kan uitvoeren tegen een echt systeem.
- Voorbeelden van invoer (zoals een SQL injection) alleen in de bekende leerboekvorm, om het principe te laten zien.
- Geen instructies om detectie te omzeilen. Je mag wel uitleggen *dat* aanvallers detectie proberen te ontwijken en *hoe een securityteam dat toch ziet*.
- Geen IOC-lijsten overnemen (lange lijsten IP-adressen of hashes); leg uit wat IOC's zijn en waar je ze vindt.

## 5. Personalisatie

- Gebruik `profile.md`, `werkcontext.md` en `interests.yml`.
- Koppel waar het kan aan **SIEM, vulnerability management en threat intelligence**: hoe helpt elk ervan bij dit onderwerp?
- **Leveranciersneutraal.** Schrijf over categorieën (vulnerability management, SIEM, EDR, MDR, threat intelligence), niet over merken. Een leverancier noem je alleen als die zelf de bron is (bijv. het onderzoek of het advies), kort en feitelijk.
- **Klantvragen** zijn vragen die een Customer Success Manager een klant stelt om het gesprek inhoudelijk te maken. Geen verkoopvragen.
- Wissel voorbeelden en invalshoeken af.
- Regio: Nederlands nieuws eerst, dan Benelux, Europa, Noord-Amerika, de rest van de wereld. Zet in `region` waar het nieuws over gaat.

## 6. Wat níet in de feed hoort

- Alles uit `excluded_topics` in `interests.yml` (investeringsrondes, aanbiedingen en webinars, weekoverzichten van andere sites, prijzen en ranglijsten).
- Een kwetsbaarheid zonder uitleg, of met alleen een CVE-nummer en een score. Kun je niet uitleggen hoe het werkt, en is het ook niet urgent? Overslaan.
- Kleine kwetsbaarheden in weinig gebruikte software, tenzij ze actief misbruikt worden of iets bijzonders laten zien.
- Incidentnieuws zonder enige technische inhoud of nieuwe informatie (bijv. alleen "bedrijf X is gehackt, onderzoek loopt"), tenzij het een groot Nederlands incident is. Dan kort, met wat bekend en onbekend is.
- Claims van ransomwaregroepen op hun eigen sites, zonder bevestiging door de organisatie of een betrouwbare bron.
- Productmarketing van leveranciers.
- Nieuws over leveranciers (overnames, koers), behalve groot nieuws (`security_market`, uitzonderingsregel).
- Herhalingen van eerder getoond nieuws zonder nieuwe informatie.
