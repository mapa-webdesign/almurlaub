# CLAUDE.md — Almurlaub Website

> Projekt-Gedächtnis für **Claude Code**. Liegt im Repository-Root.
> Stand: **22.09.2026** · Sprache im Projekt: Deutsch (bairisch gefärbt)

---

## ⚠️ Zuerst lesen: Zugangsdaten

**In dieses Repository gehören NIEMALS Zugangsdaten.** Das ist keine
Formalie – im September 2026 landete eine Doku-Datei mit FTP-Passwort und
Deploy-Token auf dem öffentlich erreichbaren Webspace.

- Parole und Cookie-Wert stehen ausschließlich in `config.php` (gitignored).
- Der Cookie-Wert steht zwangsläufig auch in der `.htaccess`, weil Apache
  `config.php` nicht lesen kann → **das Repository muss privat bleiben.**
- Die `.htaccess` sperrt zusätzlich `.md`, `.json`, `.log`, `.bak` vom
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

## 🔴 Offene Aufgaben (Stand 23.09.2026)

1. ~~**GitHub-Repository anlegen**~~ – erledigt (`mapa-webdesign/almurlaub`, privat).
2. **Hostinger einrichten:**
   - Subdomain `almurlaub.mapa-ai.de` anlegen
   - Git-Deploy verbinden: Repo, Branch `main`, Zielverzeichnis der Subdomain
   - Webhook für automatischen Pull eintragen
3. **Auf dem Server einmalig:**
   - ~~`config.php` anlegen~~ – liegt bereits auf dem Server.
   - `mkdir -p daten fotos && chmod 775 daten fotos`
   - Prüfen: Cookie-Wert in `config.php` muss mit dem in `.htaccess` übereinstimmen.
4. **Prüfen:** Login, Einkaufsliste 2027 (Haken setzen, zweites Gerät
   gegenchecken), Abrechnung, Bierrechner, Foto-Upload, `export.php`.
5. **Danach:** regelmäßige Sicherung einrichten – `export.php` wöchentlich
   abrufen und wegspeichern (z. B. Aufgabe auf Martins Mac). Hostingers
   eigene Backups kommen dazu.

### Inhaltlich noch offen
- **Truppe 2027** steht nicht fest (2026 waren es 11 Leut').
- **Hütte 2027** noch nicht entschieden – vier Kandidaten stehen auf der
  Übersichtsseite, alle noch unangefragt.
- **Chili con Carne** in der Einkaufsliste 2027 ist als *Entwurf* markiert,
  Mengen aus der 2025er-Liste abgeleitet und ungeprüft.

---

## Was verloren ging

| Weg | Ersatz |
|---|---|
| Alle Fotos (`fotos/`) | nicht wiederherstellbar – Galerien starten leer |
| Live-Daten 2026/2027 | nicht wiederherstellbar – Listen starten leer |
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
├─ .htaccess             Zugangsschutz, Sperren, Cache
├─ 2026/                 Archiv    ┐ index, einkauf, abrechnung,
├─ 2027/                 aktuell   ┘ fotos, bierrechner, upload.php
├─ config.example.php
└─ .gitignore
```

**Nicht im Repository:** `config.php`, `daten/`, `fotos/<jahr>/` – werden
vom Server geschrieben und von einem Deploy nie angefasst.

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
5. `fotos/2028/` anlegen, `upload.php` mitkopieren – sie leitet das Jahr
   über `basename(__DIR__)` selbst ab, muss also nicht angepasst werden

---

## Urlaub 2026 (abgeschlossen)

Lorenzer Hütte, Kärnten – **zum 12. Mal**, 25.07.–01.08.2026, 7 Nächte,
140 €/Nacht = 980 €. **11 Leut':** Pappenberger (Martl, Manu, Max, Alois),
Robert, Bettina, Franz, Andreas (Andi), Da Baule, Da Blaume, Da Ott.

**Bestenliste:** Lorenzer 12× · Obere Roner Kasa 7× · Hoisen 4× ·
Mahrhütte 2× · Rest je 1×

## Urlaub 2027 (in Planung)

**Termin:** Sa 04. – Sa 11.09.2027 (KW 36, 7 Nächte) – anvisiert, noch
nicht bestätigt. Countdown läuft bereits.

**Hütten-Kandidaten** (alle noch unangefragt):
Preimes Kasa (Airbnb) · Obere Roner Kasa (Suntinger) · Kreuzwirthütte
(war 2026 doppelt vergeben – diesmal schriftlich bestätigen lassen) ·
Hofer Hütte (Nockberge)

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
