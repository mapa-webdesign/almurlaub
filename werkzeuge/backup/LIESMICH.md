# Wöchentliche Sicherung (Mac)

Ruft jeden **Sonntag um 20:00 Uhr** `export.php` ab und legt das Archiv
in `~/Backups/Almurlaub` ab. War der Mac zu der Zeit aus oder im
Ruhezustand, läuft die Sicherung beim nächsten Aufwachen nach.
Die neuesten **26** Sicherungen (ein halbes Jahr) bleiben erhalten.

## Einrichten (einmalig)

```bash
cd almurlaub/werkzeuge/backup
./install.sh
```

Fragt nach dem Cookie-Wert (`cookie_wert` aus `config.php`), legt ihn im
**Schlüsselbund** ab und macht sofort einen Testlauf.

## Im Alltag

- **Protokoll:** `~/Backups/Almurlaub/backup.log`
- **Schlägt eine Sicherung fehl**, erscheint eine Mitteilung auf dem Mac.
- **Sofort sichern:** `~/bin/almurlaub-backup.sh`
- **Cookie geändert?** `./install.sh` einfach nochmal ausführen.
- **Entfernen:** `./install.sh --entfernen` (Sicherungen bleiben liegen)

## Zurückspielen

Archiv entpacken und die Ordner `daten/` bzw. `fotos/` per Dateimanager
ins Webverzeichnis der Subdomain hochladen.

## Hinweis zu iCloud

Als Ziel ist bewusst **nicht** iCloud Drive eingestellt: macOS blockiert
dort Schreibzugriffe aus Hintergrund-Jobs ohne Zusatzfreigabe. Wer die
Sicherungen zusätzlich in der Cloud will, zieht `~/Backups/Almurlaub` in
die Time-Machine-Sicherung oder kopiert den Ordner von Hand.
