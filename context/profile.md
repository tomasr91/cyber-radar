---
id: profile
type: context
schema_version: 1
updated: 2026-11-03
---

# Profiel

Dit bestand beschrijft voor wie CyberScope schrijft, wat de lezer al weet en hoe de uitleg daarop wordt afgestemd. Het is een samenvatting van het persoonlijke interesse- en leerprofiel van 3-11-2026. Werkcontext staat in `werkcontext.md`.

**Labels:** `[bekend]` = door de lezer opgegeven · `[aanname]` = redelijke afleiding, nog bevestigen · `[aanvullen]` = ontbreekt nog.

In de taken heet de lezer **"de lezer"**. Schrijf in de app in de jij-vorm.

## 1. Rol en achtergrond

- `[bekend]` Senior Customer Success Manager bij een cybersecurityleverancier (zie `werkcontext.md`).
- `[bekend]` Basiskennis van cybersecurity. Bekend met SIEM, vulnerability management, threat intelligence en algemene securityprincipes, op het niveau "weet waarvoor het wordt gebruikt".
- `[bekend]` Doel is niet om zelf securityproblemen op te lossen, maar om technische ontwikkelingen te begrijpen, de impact van incidenten in te schatten, de juiste vragen aan klanten te stellen en technische antwoorden te snappen.

## 2. Kennisniveau

### Wat de lezer al enigszins begrijpt — kort houden, niet uitgebreid opnieuw uitleggen
- `[bekend]` Wat cybersecurity in algemene zin is en waarom organisaties het nodig hebben.
- `[bekend]` Wat een SIEM ongeveer doet, wat vulnerability management inhoudt en wat threat intelligence is.
- `[bekend]` Waarom kwetsbaarheden belangrijk zijn, en waarom incidenten gedetecteerd en voorkomen moeten worden.

### Wat de lezer wil leren — hier ligt de waarde
- `[bekend]` Hoe software en infrastructuur technisch werken (servers, websites, HTTP, databases, DNS, authenticatie).
- `[bekend]` Hoe aanvallers kwetsbaarheden ontdekken en misbruiken, en welke stappen ze echt doorlopen.
- `[bekend]` Hoe een aanval zich ontwikkelt van eerste toegang naar verdere toegang binnen een organisatie.
- `[bekend]` Hoe securityproducten aanvallen detecteren, en hoe logs, netwerkverkeer en meldingen samenhangen.
- `[bekend]` Hoe securityteams bepalen welke kwetsbaarheden voorrang krijgen.
- `[bekend]` Hoe organisaties reageren op echte incidenten.

**Uitgangspunt:** ga niet uit van technische voorkennis. Leg een nieuw begrip eerst uit voordat je het gebruikt om iets ingewikkelders te beschrijven. Maak het niet eenvoudiger dan het is.

### De keten die de lezer wil leren zien
Bij elk technisch onderwerp, waar het kan:
1. De technologie die een organisatie gebruikt.
2. De kwetsbaarheid die daarin kan zitten.
3. Hoe een aanvaller die misbruikt.
4. De gevolgen voor de organisatie.
5. Hoe een securityteam de aanval ziet (detectie).
6. Welke maatregelen het risico beperken.

## 3. Wat de lezer met de app wil bereiken

- **Dagelijks bijblijven** met wat er speelt in cybersecurity, in een compacte feed.
- **Echt iets leren**: na het lezen begrijpen hoe het technisch werkt, niet alleen dát het gebeurde.
- **Beter in gesprek met klanten**: weten welke vragen je kunt stellen en wat de antwoorden betekenen.
- De belangrijkste ontwerpkeuze: CyberScope vertelt niet alleen wat er gebeurt, maar helpt begrijpen hoe cybersecurity technisch werkt.

## 4. Nieuws dat de lezer waardevol vindt

**Wel:**
- Actuele hacks, datalekken, ransomware en aanvallen op cloud en infrastructuur, mét de technische oorzaak (voorbeeld: een hack bij een grote Nederlandse organisatie).
- Nieuwe kwetsbaarheden en softwarefouten (PHP, Windows, Linux, webservers, browsers, databases, API's, cloudplatformen), zero-days, actief misbruikte kwetsbaarheden.
- Technische aanvalsmethoden: phishing, malware, ransomware, SQL injection, XSS, RCE, privilege escalation, credential theft, authentication bypass, laterale beweging, command and control.
- Webtechnologie en software: hoe het normaal werkt en waar het misgaat.
- SIEM en detectie, vulnerability management, threat intelligence: hoe het in de praktijk werkt.
- Een technisch artikel over een kwetsbaarheid is minstens zo waardevol als een groot incident.

**Niet:**
- Een korte samenvatting van een nieuwsbericht zonder uitleg.
- Een CVE-nummer met een CVSS-score en verder niets.
- Een lijst met termen of maatregelen zonder technische context.
- Een feed met alleen grote hacks, of alleen securityproducten.
- Een handleiding om aanvallen uit te voeren.
- Herhaling van hetzelfde nieuws.

**Richtverdeling** (flexibel, geen quota; details in `interests.yml` → `interest_areas`):

| Interessegebied | Richtpercentage |
|---|---|
| Nieuwe kwetsbaarheden en softwarefouten | 30% |
| Hoe aanvallen technisch werken | 30% |
| Actuele hacks en incidenten | 25% |
| Detectie en securitypraktijk (SIEM, VM, TI) | 15% |

Nieuws over securityleveranciers alleen bij groot nieuws, en niet vaak.

**Regio:** Nederland eerst, dan Benelux, dan Europa, dan Noord-Amerika, dan de rest van de wereld.

## 5. Uitlegstijl

- `[bekend]` "Jip en Janneke-taal": begrijpelijk Nederlands, zonder dat de inhoud oppervlakkig wordt.
- `[bekend]` Volgorde: eerst eenvoudig uitleggen, dan de technische werking, dan een concreet voorbeeld, dan wat het betekent voor organisaties.
- `[bekend]` Moeilijke termen direct uitleggen, vergelijkingen gebruiken waar ze helpen, korte alinea's.
- `[bekend]` Altijd onderscheid tussen **feiten**, **vermoedens** en **mogelijkheden**. Een mogelijke aanvalsmethode nooit presenteren als de gebruikte methode als dat niet bevestigd is.
- `[bekend]` Uitleggen *waarom* iets gevaarlijk is.

Voorbeeld van de gewenste verhouding (Remote Code Execution):
- *Wat betekent het?* Een aanvaller kan onder bepaalde omstandigheden een server opdrachten laten uitvoeren die van de aanvaller komen.
- *Hoe werkt het?* De server ontvangt een verzoek. Door een fout in de software wordt invoer onveilig verwerkt, waardoor de aanvaller code kan laten uitvoeren.
- *Wat kan een aanvaller ermee?* Dat hangt af van de fout en de rechten van het proces: gegevens bekijken, software installeren, andere systemen proberen te bereiken.
- *Voorkomen en detecteren?* Patchen, goed configureren, toegang beperken en verdachte activiteit monitoren.

## 6. Leerpad (geleidelijk, niet strikt op volgorde)

Gebruik actuele artikelen om deze onderwerpen op een natuurlijke manier te introduceren:

1. **Technische basis:** server, client, hoe een website werkt, HTTP, database, IP-adres, DNS, firewall, authenticatie, autorisatie.
2. **Kwetsbaarheden en aanvallen:** CVE, exploit, zero-day, RCE, SQL injection, phishing, malware, privilege escalation.
3. **Aanvalsketens:** binnenkomen, toegang uitbreiden, andere systemen bereiken, gegevens verzamelen, detectie ontwijken, onderzoek.
4. **Securitypraktijk:** SIEM, logs verzamelen, detectieregels, vulnerability management, patching, threat intelligence, incident response.

De verdiepingen in `verdieping.yml` volgen dit leerpad.

## 7. Leesritme

- `[bekend]` Elke dag, ook in het weekend. De feed wordt 's nachts ververst.
- `[bekend]` Compact: liever een paar goed uitgelegde stukken dan veel korte berichten. Lengte mag verschillen per onderwerp.
- `[aanvullen]` Hoeveel tijd per dag beschikbaar is voor lezen.
