# CLAUDE.md — Almurlaub Website

> Projekt-Gedächtnis für **Claude Code**. Liegt im Repository-Root.
> Stand: **02.10.2026** · Sprache im Projekt: Deutsch (bairisch gefärbt)

---

## ⚠️ Zuerst lesen: Zugangsdaten

**In dieses Repository gehören NIEMALS Zugangsdaten.** Das ist keine
Formalie – im September 2026 landete eine Doku-Datei mit FTP-Passwort und
Deploy-Token auf dem öffentlich erreichbaren Webspace.

- Parole und Cookie-Wert stehen ausschließlich in `config.php` (gitignored).
- Der Cookie-Wert steht zwangsläufig auch in der `.htaccess`, weil Apache
  `config.php` nicht lesen kann → **das Repository muss privat bleiben.**
- Martins alte `Projekt-Info.md` (lokal, nicht im Repo) enthält das alte
  FTP-Passwort, die alte Parole und den alten Cookie – vermutlich die
  Datei, die im September geleakt ist. **Nie ins Repo übernehmen.**
- Die `.htaccess` sperrt zusätzlich `.md`, `.json`, `.log`, `.bak`, `.ini`,
  `.git/`, `unterlagen/` vom
  direkten Abruf. Diese Datei hier wäre also selbst dann nicht abrufbar.

---

## Worum es geht

Interne Website der Almurlaub-Truppe – jährlicher Hüttenurlaub seit 1999,
organisiert von **Martin Pappenberger** (alleiniger Entwickler).
Inhalte: Hütten-Historie, Planung des laufenden Jahres, Packliste, live
geteilte Einkaufsliste, Abrechnung, Bierrechner, Fotogalerie.

- **Ziel-URL:** https://almurlaub.mapa-ai.de
- **Hosting:** Hostinger
- **Deploy:** automatischer Git-Pull aus diesem Repository
- **Vorher:** almurlaub.pappenberger.org bei domainfactory – der Webspace
  wurde im September 2026 komplett geleert, Wiederherstellung war nicht
  mehr möglich. Daher dieser Neuaufbau.

---

## 🔴 Offene Aufgaben (Stand 02.10.2026)

**Erledigt:** GitHub-Repo (privat) · Hostinger-Subdomain + Git-Deploy mit
Webhook · DNS bei **Cloudflare** (`A almurlaub → 88.222.222.193`, *DNS only*)
· Let's-Encrypt-SSL + HTTPS-Umleitung · `config.php` auf dem Server ·
Login geprüft · `daten/` beschreibbar · Foto-Upload getestet · Logo +
Favicon · alle 22 Gestaltungs-/Hütten-Fotos · Backup-Skript geschrieben.

**Bei Martin offen:**
1. **Sicherheit:** FTP-Passwort bei domainfactory ändern (falls Zugang noch
   existiert), FTP-Daten aus der Notion-Seite „Urlaub auf der Alm“ löschen,
   Parole in `config.php` wechseln, falls noch die alte von 2026.
2. **Backup einrichten:** `git pull`, dann `werkzeuge/backup/install.sh`.

### Inhaltlich noch offen
- **Truppe 2027** steht nicht fest (2026 waren es 11 Leut').
- **Hütte 2027** noch nicht entschieden – 2 Angebote da (Hofer, Preimes),
  Roner Kasa erst ab 28.08. frei, Kreuzwirt ausgebucht
  (2028 angefragt), Kalser- und Larer Hütte neu (je ca. 10 Plätze).
- **Chili con Carne** in der Einkaufsliste 2027 ist als *Entwurf* markiert,
  Mengen aus der 2025er-Liste abgeleitet und ungeprüft.

---

## Was verloren ging

| Weg | Ersatz |
|---|---|
| Gestaltungs- und Hütten-Fotos (`fotos/*.jpg`, `fotos/huetten/`) | **wiederhergestellt** aus Martins Fundus (Okt. 2026), jetzt im Repo |
| Fotoalbum 2026 (`fotos/2026/`, Uploads der Truppe) | weg – nur durch erneutes Hochladen |
| Bier-Etiketten (`fotos/biere/`) | weg – von keiner Seite verwendet |
| Live-Daten 2026 (Einkauf, To-Dos) | weg |
| Abrechnung 2026 | **rekonstruiert** aus Martins Screenshot (Okt. 2026): Parteien, Nächte, Ausgaben-Summe je Partei – Einzelposten verloren. Kopie in `unterlagen/abrechnung-2026.{pdf,json}` |
| `api.php` | **neu gebaut**, getestet |
| `login.php`, `logout.php`, `.htaccess` | **neu gebaut**, getestet |
| HTML-Seiten, CSS, JS | aus Sicherung vom 21.09.2026, vollständig |

---

## Aufbau

```
├─ index.html            Historie: Hütten seit 1999, Bestenliste, Sprüche-Wand
├─ packliste.html        Packliste (Haken nur lokal im Browser, kein Sync)
├─ huettensuche.html     Hütten-Status der laufenden Suche
├─ login.php             Bierparole-Login (Daten aus config.php)
├─ logout.php            Abmelden
├─ api.php               Live-Datenspeicher der geteilten Listen
├─ export.php            Sicherung der Laufzeitdaten (ZIP bzw. tar.gz)
├─ alm.css               zentrales Stylesheet – ALLE Seiten
├─ alm-nav.js            Burger-Menü + Untermenü je Jahresbereich – ALLE Seiten
├─ abrechnung-export.js  PDF/Drucken, CSV, JSON-Sicherung + Einspielen – Abrechnungsseiten
├─ .htaccess             Zugangsschutz, Sperren, Cache
├─ logo.svg              Logo (Bierdeckel-Rund) – auch Favicon; favicon.ico, apple-touch-icon.png
├─ fotos/                Gestaltungsfotos (*.jpg) + fotos/huetten/ – im Repo
├─ 2026/                 Archiv    ┐ index, einkauf, abrechnung,
├─ 2027/                 aktuell   ┘ fotos, bierrechner, upload.php
├─ unterlagen/           Hüttenurlaub 2025 (PDF), Abrechnung 2026 (PDF+JSON), Rezepte – gesperrt
├─ werkzeuge/backup/     Wöchentliche Sicherung von export.php auf dem Mac
├─ config.example.php
└─ .gitignore
```

**Nicht im Repository:** `config.php`, `daten/`, `fotos/<jahr>/` (Uploads) – werden
vom Server geschrieben und von einem Deploy nie angefasst.

**Ohne Login abrufbar** (Ausnahmen in der `.htaccess`): `login.php`,
`logout.php`, `logo.svg`, `favicon.ico`, `apple-touch-icon.png`, `fotos/biere/`.

---

## Navigation

- **Hauptmenü:** Historie · Alm 2027 · Alm 2026 · Packliste · Hütten-Suche · Abmelden
- **Untermenü je Jahr:** Übersicht · Einkaufsliste · Abrechnung · Fotos · Bierrechner
- ⚠️ **Das Nav-Markup steht in jeder Seite einzeln** (kein Include).
  Menüänderungen müssen in **allen** Seiten nachgezogen werden, und die
  relativen Pfade unterscheiden sich je Ordner:
  Root → `2027/index.html` · in `/2026/` → `../2027/index.html` · in `/2027/` → `index.html`
- **Mobil (< 800 px):** `alm-nav.js` baut den Burger und hängt die
  Unterseiten als aufklappbare Punkte ein. Es erkennt **jeden** Menüpunkt
  der Form „Alm ‹Jahr›" per Regex – beim Anlegen von 2028 ist am Skript
  nichts zu tun. Die Unterseitenliste steht in `SUBSEITEN` und muss zur
  `.jahr-nav-innen` in den Seiten passen.

---

## Live-Daten (`api.php`)

Gemeinsamer JSON-Speicher, Clients fragen alle 4 s nach.

```
GET  api.php?doc=einkauf2027   → {"rev":<int>,"data":{…}}
POST api.php?doc=einkauf2027
     {"set":   {"items.f1":{"done":1,"wer":"Manu"}, "personen":11}}
     {"unset": ["custom.c17"]}
```

Punkt = eine Ebene tiefer. Teilbaum leeren: `{"set":{"items":{}}}`.
Ablage in `daten/daten-<doc>.json`, Schreibzugriffe mit `flock` serialisiert.

**Doc-Namen pro Jahr getrennt** – sonst teilen sich zwei Jahrgänge einen
Datenstand: `einkauf2027`, `abrechnung2027`, `bier2027`, `todos2027`.

### Einkaufsliste 2027 – Datenmodell im HTML
```
KATALOG  = { zutat_id: {name, einheit, gruppe, fix?, wer?} }
GERICHTE = [ {id, name, emoji, portionen, skaliert, entwurf?, notiz?, zutaten:{id:menge}} ]
```
- `einheit: ""` = zählbare Sache, das Wort steckt im Namen
- `fix` = feste Einkaufsmenge für Vorräte (statt „3 TL Salz")
- `skaliert: false` = feste Menge (Hüttenkram, Ausrüstung)
- **Zwei Ansichten:** *Nach Kategorie* (zusammengefasst, zum Einkaufen –
  Standard) und *Nach Rezept* (je Gericht, zum Kochen). Haken gelten pro
  Zutat und sind in beiden Ansichten identisch.
- **Neues Gericht:** Block in `GERICHTE` anhängen, fehlende Zutaten in
  `KATALOG` eintragen. Merge, Gruppierung und „Wofür"-Chips entstehen selbst.
- Namens-Dropdown je Zeile ist änderbar, **bis abgehakt → gesperrt (🔒)**.

### Abrechnung
```
data = { parteien:{id:{name,naechte,anzahlung}}, ausgaben:{id:{…}} }
satz = Σ Ausgaben / Σ Übernachtungen
Bilanz = eigene Ausgaben + Anzahlung − (Übernachtungen × satz)
```
**Sichern & Teilen** (`abrechnung-export.js`, Daten über `window.almAbrechnung`):
PDF über den Druckdialog (Druck-CSS in `alm.css`, greift nur auf Seiten mit
`.druck-kopf`), CSV für Excel (`;`, Dezimalkomma, BOM), JSON-Sicherung
`{typ, jahr, exportiert, daten:{parteien, ausgaben}}`; Einspielen ersetzt
`parteien` und `ausgaben` für alle (mit Rückfrage, warnt bei falschem Jahr).

---

## Design

Holz-Hintergrund, Creme-Karten, alpine Gemütlichkeit. **Immer die
CSS-Variablen aus `alm.css :root` verwenden**, keine festen Hex-Werte:

`--holz-dunkel #3a2a1c` · `--holz #5a4130` · `--holz-hell #7a5c42` ·
`--holz-grau #8a7a68` · `--creme #f4ecd9` · `--creme-dunkel #e8dcc0` ·
`--schwammerl #d99a3c` · `--schwammerl-hell #eab861` · `--tanne #3d5a3f` ·
`--tanne-hell #5a7d5c` · `--geranie #b8452f` · `--nebel #aebbc4` · `--tinte #2e2318`

Schriften: **Bitter** (Text), **Caveat** (handschriftliche Akzente).
Tonfall in Texten: freundlich, bairisch angehaucht („Wievui?", „Wos?",
„Kein Zutritt für Schwachschwoaba").

---

## Neues Jahr anlegen

1. `cp -r 2027 2028`
2. In den fünf Seiten `2027` → `2028`, **inklusive der API-Doc-Namen**
3. Inhalte leeren: Countdown-Ziel (`var ziel`), Hütten, Truppe, To-Dos
4. Menüpunkt „Alm 2028" in **allen** Seiten ergänzen (Pfade je Ordner beachten)
5. `upload.php` mitkopieren – sie leitet das Jahr über `basename(__DIR__)`
   selbst ab und legt `<fotos_dir>/2028/` beim ersten Upload selbst an

---

## Urlaub 2026 (abgeschlossen)

Lorenzer Hütte, Kärnten – **zum 12. Mal**, 25.07.–01.08.2026, 7 Nächte,
140 €/Nacht = 980 €. **11 Leut':** Pappenberger (Martl, Manu, Max, Alois),
Robert, Bettina, Franz, Andreas (Andi), Da Baule, Da Blaume, Da Ott.
**Abrechnung:** 1.915,10 € Ausgaben, 46 Übernachtungen, 41,63 €/Übernachtung.
Bilanz: Pappe's +105,92 · Ott +187,57 · Franz +88,57 · Baule −183,43 ·
Blaume −198,63 (+ = bekommt zurück). **Erledigt:** Baule → Ott,
Blaume → Franz und Pappe's, Rest 4,14 € Blaume → Ott bar – alles beglichen.
Vermerk als Abschnitt „Abgerechnet“ statisch in `2026/abrechnung.html`.

**Bestenliste:** Lorenzer 12× · Obere Roner Kasa 7× · Hoisen 4× ·
Mahrhütte 2× · Rest je 1×

## Urlaub 2027 (in Planung)

**Wunschtermin:** Sa 07. – Sa 14.08.2027 (7 Nächte, KW 31/32; zuvor kurz
14.–21.08. bzw. KW 36 im Gespräch – beides überholt).
**Flexibel:** Nicht jede Hütte ist genau in der Woche frei. Ist sie es
nicht, werden andere Zeiträume (auch Fr–Fr o. Ä.) und andere Hütten
geprüft. Bei jeder Hütte deshalb den tatsächlich angebotenen Zeitraum
eintragen, nicht den Wunschtermin. Countdown in `2027/index.html`
(`var ziel`, Monat 0-basiert) erst bei Buchung auf den echten Anreisetag
setzen.

**Hütten-Kandidaten** (Stand 02.10.2026):
- **Hofer Hütte** (Nockberge) – Angebot **Fr 13.–Fr 20.08.**, 10 Erw.:
  1.575 Miete + 90 Endreinigung + 315 Kurtaxe = **1.980 €** (198 €/P.),
  inkl. Handtücher, Betriebskosten, Brennholz. Achtung: Fr–Fr.
- **Preimes Kasa** (Airbnb) – **Sa 14.–Sa 21.08. vom Gastgeber direkt
  bestätigt**, 10 Gäste: **2.150 €** (215 €/P.) laut Airbnb; Preis bei
  Direktbuchung angefragt (evtl. günstiger), Kurtaxe noch ungeklärt.
- Obere Roner Kasa (Suntinger) – **August 2027 belegt**; laut Dani (WhatsApp)
  nur 28.08.–18.09.2027 frei → für 2028 früh anfragen. Wird auch als „Almhütte
  PSD-00611“ auf kaernten-ferienwohnungen.com angeboten (= Roner Kasa).
- Hinweis für Suchen: **Hüttenpartner „DOR-SBG“ = Huberalm** (2024 dort),
  **„Almhütte PSD-00611“ = Obere Roner Kasa** – Portale nennen Hütten oft
  nur per Code, vor dem Vorschlagen gegen die Historie prüfen.
- **Kalserhütte** (Oberdrauburg, Drautal) – neu, anfragen: bis 10 P., ab
  160 €/Nacht + Nebenkosten; telefonisch +43 4710 2644 / +43 664 9054195
- **Larer Hütte** (Lessach, Prebersee, Lungau) – neu, anfragen: ca. 10 P.,
  ab 100 €/Nacht + Ortstaxe/Strom; annemarie.jesner@sbg.at
- Kreuzwirthütte – **2027 ausgebucht**; Reservierungsanfrage für **2028** läuft
  (2026 doppelt vergeben → Zusage unbedingt schriftlich)

**Rezept-Notiz:** „Rigatoni al Porno" (Dutch Oven ft12) ist für 11 Personen
hinterlegt. Faustregeln zum Gegenrechnen bei Änderungen: Fleisch zu Tomaten
etwa 1:1, rund 0,8 ml Sauce je Gramm gekochter Nudeln, Topf höchstens zu
vier Fünfteln füllen.

---

## Lessons Learned

- **Keine Zugangsdaten in Dateien, die im Webverzeichnis landen.**
- **Sieben Tage Hoster-Backup reichen nicht**, um einen Verlust zu bemerken.
  Eigene Sicherung ist Pflicht – dafür gibt es `export.php`.
- **Vor jedem größeren Umbau** den Live-Stand ziehen und wegsichern.
- **Nach jedem Deploy das Ergebnis wirklich abrufen**, nicht der
  Erfolgsmeldung vertrauen.
- **JS vor dem Commit prüfen:** Skriptblöcke extrahieren, `node --check`.
- **`mbstring` ist nicht überall aktiv** – `mb_*`-Funktionen meiden oder
  absichern. Hat schon zweimal zu einem leeren HTTP 500 geführt.
- **Mengen in Rezepten gegenrechnen**, nicht nur einzeln plausibel wählen.
  Eine frühere Fassung hatte 3 kg Tomaten auf 1,4 kg Nudeln.
- **Viele Dateien gleichzeitig ändern:** Python-Skript mit String-Ersetzung
  ist zuverlässiger als viele Einzeledits – und vorher prüfen, ob das
  Suchmuster wirklich genau einmal vorkommt.
- **Umlaute in Dateinamen vom Mac** sind NFD-kodiert (u + ¨). `glob`/`cp`
  mit getipptem „ü“ finden sie nicht – `unicodedata.normalize('NFC', …)`
  oder Platzhalter (`H*tte`) nehmen.
- **PHP nimmt nur 20 Dateien je Anfrage** (`max_file_uploads`) und verwirft
  den Rest kommentarlos – `uebersprungen` bleibt 0. Eine `.user.ini` greift
  auf Hostinger nicht (getestet). Deshalb schickt `fotos.html` die Fotos in
  Paketen zu je 10 (`PAKET`).
- **Handyfotos enthalten GPS-Koordinaten.** Vor dem Einchecken EXIF
  entfernen; Original-Uploads auf GitHub-Branches danach löschen lassen.
- **`esc()` in den Seiten-Skripten muss auch `"` maskieren**, sobald der
  Wert in einem HTML-Attribut landet (`value="…"`) – sonst bricht ein Name
  wie `Baule "Da"` das Eingabefeld (behoben Okt. 2026).
- **Caching:** Die `.htaccess` setzt global `no-store` (Live-Listen), aber
  Bilder bekommen 30 Tage `max-age` und CSS/JS `no-cache` (prüfen per
  304). Sonst lädt die Fotoseite bei jedem Aufruf alles neu. Galerien nur
  neu zeichnen, wenn sich die Liste wirklich geändert hat (`stand`).
