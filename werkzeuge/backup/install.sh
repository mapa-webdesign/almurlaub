#!/bin/bash
# ============================================================
#  install.sh – richtet die wöchentliche Almurlaub-Sicherung
#  auf dem Mac ein (einmalig ausführen)
#  ------------------------------------------------------------
#  1. kopiert almurlaub-backup.sh nach ~/bin
#  2. legt den Cookie-Wert im Schlüsselbund ab
#  3. richtet einen launchd-Job ein: jeden Sonntag 20:00 Uhr
#     (war der Mac da aus oder im Ruhezustand, läuft er beim
#      nächsten Aufwachen nach)
#  4. macht sofort einen Testlauf
#
#  Entfernen:  ./install.sh --entfernen
# ============================================================

set -eu

LABEL="de.mapa-ai.almurlaub-backup"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
SKRIPT="$HOME/bin/almurlaub-backup.sh"
HIER="$(cd "$(dirname "$0")" && pwd)"

if [ "${1:-}" = "--entfernen" ]; then
    launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
    rm -f "$PLIST" "$SKRIPT"
    security delete-generic-password -s almurlaub-backup >/dev/null 2>&1 || true
    echo "Entfernt. Vorhandene Sicherungen in ~/Backups/Almurlaub bleiben erhalten."
    exit 0
fi

[ "$(uname)" = "Darwin" ] || { echo "Nur für macOS gedacht." >&2; exit 1; }

# --- 1. Skript ablegen ---
mkdir -p "$HOME/bin"
cp "$HIER/almurlaub-backup.sh" "$SKRIPT"
chmod 755 "$SKRIPT"
echo "✓ Skript nach $SKRIPT kopiert"

# --- 2. Cookie in den Schlüsselbund ---
echo
echo "Cookie-Wert eingeben – steht in config.php bei 'cookie_wert'"
echo "(bzw. in der .htaccess hinter 'almauth='). Eingabe bleibt unsichtbar."
read -rs -p "Cookie-Wert: " COOKIE
echo
[ -n "$COOKIE" ] || { echo "Leere Eingabe – abgebrochen." >&2; exit 1; }
security delete-generic-password -s almurlaub-backup >/dev/null 2>&1 || true
security add-generic-password -s almurlaub-backup -a "$USER" -w "$COOKIE" \
    -T /usr/bin/security -U
unset COOKIE
echo "✓ Cookie im Schlüsselbund gespeichert (Eintrag: almurlaub-backup)"

# --- 3. launchd-Job ---
mkdir -p "$HOME/Library/LaunchAgents" "$HOME/Backups/Almurlaub"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>             <string>$LABEL</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$SKRIPT</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key> <integer>0</integer>
        <key>Hour</key>    <integer>20</integer>
        <key>Minute</key>  <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>   <string>$HOME/Backups/Almurlaub/launchd.log</string>
    <key>StandardErrorPath</key> <string>$HOME/Backups/Almurlaub/launchd.log</string>
</dict>
</plist>
EOF
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo "✓ Wöchentlicher Job eingerichtet (sonntags 20:00 Uhr)"

# --- 4. Testlauf ---
echo
echo "Testlauf …"
if "$SKRIPT"; then
    echo
    echo "✓ Fertig. Sicherungen liegen in ~/Backups/Almurlaub"
else
    echo
    echo "✗ Testlauf fehlgeschlagen – siehe ~/Backups/Almurlaub/backup.log" >&2
    exit 1
fi
