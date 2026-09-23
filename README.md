# 🏔️ Urlaub auf der Alm

Interne Website der Almurlaub-Truppe – Hüttenurlaub-Tradition seit 1999.
Hütten-Historie, Planung des laufenden Jahres, Packliste, live geteilte
Einkaufsliste, Abrechnung, Bierrechner und Fotogalerie.

**Live:** https://almurlaub.mapa-ai.de
**Hosting:** Hostinger · **Deploy:** automatischer Git-Pull aus diesem Repository

---

## ⚡ Einrichtung auf einem neuen Server

1. Repository per Git-Deploy in das Webverzeichnis ziehen lassen.
2. `config.example.php` nach `config.php` kopieren und ausfüllen:
   ```bash
   cp config.example.php config.php
   ```
   Darin eintragen: Bierparole und ein langer Zufallswert als Cookie-Wert.
3. **Wichtig:** Der Cookie-Wert in `config.php` und in der `.htaccess`
   müssen identisch sein. In der `.htaccess` steht er in der Zeile
   `RewriteCond %{HTTP_COOKIE} !almauth=…`
4. Schreibbare Ordner anlegen:
   ```bash
   mkdir -p daten fotos && chmod 775 daten fotos
   ```
5. Aufrufen, Bierparole eingeben, fertig.

> `config.php`, `daten/` und die Foto-Uploads stehen in `.gitignore` und
> werden von einem Deploy **nie** überschrieben.

---

## 📁 Aufbau

```
├─ index.html            Historie: alle Hütten seit 1999, Bestenliste, Sprüche
├─ packliste.html        Packliste (Haken nur lokal im Browser)
├─ huettensuche.html     Hütten-Status der laufenden Suche
├─ login.php             Bierparole-Login (Zugangsdaten aus config.php)
├─ logout.php            Abmelden
├─ api.php               Live-Datenspeicher für die geteilten Listen
├─ export.php            Sicherung der Laufzeitdaten als Archiv
├─ alm.css               zentrales Stylesheet (alle Seiten)
├─ alm-nav.js            Burger-Menü + Untermenü je Jahresbereich
├─ .htaccess             Zugangsschutz, Sperren, Cache-Regeln
│
├─ 2026/                 Archiv-Jahr        ┐  index, einkauf, abrechnung,
├─ 2027/                 laufendes Jahr     ┘  fotos, bierrechner, upload.php
│
├─ config.example.php    Vorlage für config.php
└─ .gitignore
```

### Nicht im Repository (Laufzeitdaten)

| Pfad | Inhalt | Sicherung |
|---|---|---|
| `config.php` | Parole, Cookie-Wert | einmalig, liegt nur auf dem Server |
| `daten/daten-*.json` | Einkaufshaken, Abrechnung, Bierrechner | `export.php` |
| `fotos/<jahr>/` | hochgeladene Bilder | `export.php` |

Ist ein Urlaub vorbei und das Album fertig, kann es bewusst archiviert werden:

```bash
git add -f fotos/2027 && git commit -m "Fotos 2027 archiviert"
```

---

## 🆕 Ein neues Jahr anlegen

1. Ordner kopieren: `cp -r 2027 2028`
2. In den fünf Seiten `2027` durch `2028` ersetzen – auch bei den
   API-Namen (`einkauf2027` → `einkauf2028` usw.), sonst teilen sich
   beide Jahre denselben Datenstand.
3. Inhalte leeren: Countdown-Ziel, Hütten, Truppe, To-Dos.
4. Den Menüpunkt „Alm 2028" in **allen** Seiten ergänzen – das Nav-Markup
   ist in jeder Datei einzeln eingebettet.

`alm-nav.js` braucht dafür keine Änderung: Es erkennt jeden Menüpunkt der
Form „Alm ‹Jahr›" selbst und baut ihm sein Untermenü.

---

## 🔌 Die Live-Daten-Schnittstelle

Ein gemeinsamer JSON-Speicher für alle geteilten Listen. Die Seiten fragen
alle 4 Sekunden nach Änderungen.

```
GET  api.php?doc=einkauf2027
     → {"rev":1790106688,"data":{…}}

POST api.php?doc=einkauf2027
     {"set":   {"items.f1": {"done":1,"wer":"Manu"}, "personen": 11}}
     {"unset": ["custom.c17"]}
```

Der Punkt in `items.f1` steht für eine Ebene tiefer. Ein ganzer Teilbaum
lässt sich mit `{"set":{"items":{}}}` zurücksetzen.

**Doc-Namen pro Jahr getrennt:** `einkauf2027`, `abrechnung2027`,
`bier2027`, `todos2027`.

---

## 🎨 Design

Holz-Hintergrund, Creme-Karten, alpine Gemütlichkeit. Farben als
CSS-Variablen in `alm.css` – bitte immer die Variablen verwenden,
keine festen Hex-Werte:

`--holz-dunkel #3a2a1c` · `--holz #5a4130` · `--creme #f4ecd9` ·
`--schwammerl #d99a3c` (Gold) · `--tanne #3d5a3f` (Grün) ·
`--geranie #b8452f` (Rot) · `--tinte #2e2318`

Schriften: **Bitter** (Text) und **Caveat** (handschriftliche Akzente).

---

## ⚠️ Zu beachten

- **Nie Zugangsdaten committen.** Sie gehören ausschließlich in
  `config.php`. Die `.htaccess` sperrt zusätzlich `.md`, `.json`, `.log`
  und `.bak` vom direkten Abruf.
- **Nav-Markup ist dupliziert** – Menüänderungen in allen Seiten nachziehen.
  Relative Pfade unterscheiden sich je Ordner.
- **Katalog und Rechenlogik stehen im HTML**, nur der veränderliche
  Zustand liegt in `api.php`. Eine neue Zutat heißt also: HTML bearbeiten.
- **Vor größeren Umbauten** einmal `export.php` aufrufen und das Archiv
  wegsichern.
