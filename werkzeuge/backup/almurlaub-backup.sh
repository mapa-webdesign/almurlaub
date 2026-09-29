#!/bin/bash
# ============================================================
#  almurlaub-backup.sh – wöchentliche Sicherung der Live-Daten
#  ------------------------------------------------------------
#  Ruft export.php ab (Einkaufshaken, Abrechnung, Bierrechner,
#  hochgeladene Fotos) und legt das Archiv lokal ab.
#
#  Der Zugangs-Cookie steht NICHT in diesem Skript, sondern im
#  macOS-Schlüsselbund (Eintrag "almurlaub-backup").
#  Einrichten: siehe install.sh bzw. LIESMICH.md
#
#  Einstellbar über Umgebungsvariablen:
#    ALM_ZIEL     Zielordner          (Standard: ~/Backups/Almurlaub)
#    ALM_BEHALTEN Anzahl Sicherungen  (Standard: 26 = ein halbes Jahr)
#    ALM_COOKIE   Cookie-Wert direkt  (nur zum Testen, sonst Schlüsselbund)
# ============================================================

set -u

URL="https://almurlaub.mapa-ai.de/export.php"
ZIEL="${ALM_ZIEL:-$HOME/Backups/Almurlaub}"
BEHALTEN="${ALM_BEHALTEN:-26}"
LOG="$ZIEL/backup.log"

mkdir -p "$ZIEL" || { echo "Zielordner nicht anlegbar: $ZIEL" >&2; exit 1; }

log() { echo "$(date '+%Y-%m-%d %H:%M:%S')  $*" >> "$LOG"; echo "$*"; }

melde_fehler() {
    log "FEHLER: $1"
    # Mitteilung in der macOS-Mitteilungszentrale (auf Linux still ignoriert)
    command -v osascript >/dev/null 2>&1 && osascript -e \
        "display notification \"$1\" with title \"Almurlaub-Backup fehlgeschlagen\" sound name \"Basso\"" 2>/dev/null
    exit 1
}

# --- Cookie holen ---
COOKIE="${ALM_COOKIE:-}"
if [ -z "$COOKIE" ] && command -v security >/dev/null 2>&1; then
    COOKIE="$(security find-generic-password -s almurlaub-backup -w 2>/dev/null)"
fi
[ -n "$COOKIE" ] || melde_fehler "Kein Cookie im Schlüsselbund (almurlaub-backup). install.sh ausführen."

# --- Abrufen ---
TMP="$(mktemp "$ZIEL/.laden.XXXXXX")" || melde_fehler "Temporäre Datei nicht anlegbar."
trap 'rm -f "$TMP"' EXIT

ANTWORT="$(curl -sS --max-time 300 --retry 3 --retry-delay 20 \
    -H "Cookie: almauth=$COOKIE" \
    -o "$TMP" -w '%{http_code} %{content_type}' "$URL" 2>&1)" \
    || melde_fehler "Server nicht erreichbar: $ANTWORT"

CODE="${ANTWORT%% *}"
TYP="${ANTWORT#* }"

case "$CODE" in
    200) ;;
    302) melde_fehler "Umleitung zum Login – Cookie falsch oder geändert." ;;
    404) log "Nichts zu sichern – noch keine Daten und keine Fotos auf dem Server."; exit 0 ;;
    *)   melde_fehler "HTTP $CODE: $(head -c 200 "$TMP")" ;;
esac

# --- Format erkennen und prüfen ---
STEMPEL="$(date '+%Y-%m-%d-%H%M')"
case "$TYP" in
    application/zip*)
        DATEI="$ZIEL/almurlaub-daten-$STEMPEL.zip"
        unzip -tq "$TMP" >/dev/null 2>&1 || melde_fehler "ZIP ist beschädigt." ;;
    application/gzip*|application/x-gzip*)
        DATEI="$ZIEL/almurlaub-daten-$STEMPEL.tar.gz"
        tar -tzf "$TMP" >/dev/null 2>&1 || melde_fehler "tar.gz ist beschädigt." ;;
    *)
        melde_fehler "Unerwarteter Inhaltstyp: $TYP" ;;
esac

mv "$TMP" "$DATEI" || melde_fehler "Archiv konnte nicht abgelegt werden."
trap - EXIT
log "OK: $(basename "$DATEI") ($(du -h "$DATEI" | cut -f1))"

# --- Alte Sicherungen aufräumen (die neuesten $BEHALTEN bleiben) ---
ls -1t "$ZIEL"/almurlaub-daten-* 2>/dev/null | tail -n +"$((BEHALTEN + 1))" | while read -r alt; do
    rm -f "$alt" && log "Gelöscht (zu alt): $(basename "$alt")"
done

exit 0
