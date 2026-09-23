<?php
/**
 * api.php – Live-Datenspeicher für die Almurlaub-Seiten
 * -----------------------------------------------------
 * Einfacher JSON-Speicher, den Einkaufsliste, Abrechnung und
 * Bierrechner gemeinsam nutzen. Ein "doc" = eine Datei.
 *
 * Lesen:     GET  api.php?doc=einkauf2027
 *            -> {"rev":<int>, "data":{...}}
 *
 * Schreiben: POST api.php?doc=einkauf2027
 *            {"set":   {"items.f1": {...}, "personen": 11}}   Punkt = Ebene tiefer
 *            {"unset": ["custom.c17", "items.c17"]}
 *            -> gibt den neuen Gesamtstand zurück (gleiches Format wie GET)
 *
 * Die Dateien liegen in DATEN_DIR und sind per .htaccess vom direkten
 * Abruf ausgeschlossen. Zugriff nur mit gültigem Login-Cookie, weil die
 * .htaccess diese Datei mitschützt.
 */

declare(strict_types=1);

$cfg = __DIR__ . '/config.php';
$DATEN_DIR = is_file($cfg)
    ? ((require $cfg)['daten_dir'] ?? __DIR__ . '/daten')
    : __DIR__ . '/daten';

const MAX_BYTES  = 2 * 1024 * 1024;   // 2 MB je Dokument
const MAX_TIEFE  = 6;                 // Schachtelungstiefe bei "a.b.c"

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex, nofollow');

function raus(array $d, int $code = 200): never {
    http_response_code($code);
    echo json_encode($d, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_FORCE_OBJECT);
    exit;
}

/* --- Dokumentname prüfen --- */
$doc = (string)($_GET['doc'] ?? '');
if (!preg_match('/^[a-z][a-z0-9_-]{0,40}$/', $doc)) {
    raus(['fehler' => 'Ungültiger doc-Name.'], 400);
}

if (!is_dir($DATEN_DIR) && !@mkdir($DATEN_DIR, 0775, true) && !is_dir($DATEN_DIR)) {
    raus(['fehler' => 'Datenordner nicht anlegbar.'], 500);
}
$datei = $DATEN_DIR . '/daten-' . $doc . '.json';

/* --- Hilfsfunktionen für Punkt-Pfade --- */
function pfadSetzen(array &$ziel, string $pfad, $wert): void {
    $teile = explode('.', $pfad);
    if (count($teile) > MAX_TIEFE) return;
    $c = &$ziel;
    foreach ($teile as $i => $t) {
        if ($t === '') return;
        if ($i === count($teile) - 1) { $c[$t] = $wert; return; }
        if (!isset($c[$t]) || !is_array($c[$t])) $c[$t] = [];
        $c = &$c[$t];
    }
}

function pfadLoeschen(array &$ziel, string $pfad): void {
    $teile = explode('.', $pfad);
    $c = &$ziel;
    foreach ($teile as $i => $t) {
        if ($t === '') return;
        if ($i === count($teile) - 1) { unset($c[$t]); return; }
        if (!isset($c[$t]) || !is_array($c[$t])) return;
        $c = &$c[$t];
    }
}

/* --- Datei lesen (mit gemeinsamer Sperre) --- */
function lade(string $datei): array {
    if (!is_file($datei)) return [];
    $fh = @fopen($datei, 'r');
    if (!$fh) return [];
    @flock($fh, LOCK_SH);
    $roh = stream_get_contents($fh);
    @flock($fh, LOCK_UN);
    fclose($fh);
    if ($roh === false || $roh === '') return [];
    $d = json_decode($roh, true);
    return is_array($d) ? $d : [];
}

function rev(string $datei): int {
    clearstatcache(true, $datei);
    return is_file($datei) ? (int)filemtime($datei) : 0;
}

/* ================= LESEN ================= */
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    raus(['rev' => rev($datei), 'data' => (object)lade($datei)]);
}

/* ================= SCHREIBEN ================= */
$roh = file_get_contents('php://input');
if ($roh === false || strlen($roh) > MAX_BYTES) {
    raus(['fehler' => 'Anfrage leer oder zu groß.'], 400);
}
$befehl = json_decode($roh, true);
if (!is_array($befehl)) {
    raus(['fehler' => 'Kein gültiges JSON.'], 400);
}

/* Exklusive Sperre über die gesamte Änderung – sonst gehen
   gleichzeitige Haken von zwei Handys verloren. */
$fh = @fopen($datei, 'c+');
if (!$fh) raus(['fehler' => 'Datei nicht schreibbar.'], 500);
@flock($fh, LOCK_EX);

$inhalt = stream_get_contents($fh);
$daten  = [];
if (is_string($inhalt) && $inhalt !== '') {
    $tmp = json_decode($inhalt, true);
    if (is_array($tmp)) $daten = $tmp;
}

if (isset($befehl['set']) && is_array($befehl['set'])) {
    foreach ($befehl['set'] as $pfad => $wert) {
        if (!is_string($pfad) || $pfad === '') continue;
        if (!preg_match('/^[A-Za-z0-9_.:-]{1,120}$/', $pfad)) continue;
        pfadSetzen($daten, $pfad, $wert);
    }
}
if (isset($befehl['unset']) && is_array($befehl['unset'])) {
    foreach ($befehl['unset'] as $pfad) {
        if (!is_string($pfad) || $pfad === '') continue;
        if (!preg_match('/^[A-Za-z0-9_.:-]{1,120}$/', $pfad)) continue;
        pfadLoeschen($daten, $pfad);
    }
}

$neu = json_encode($daten, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_FORCE_OBJECT);
if ($neu === false || strlen($neu) > MAX_BYTES) {
    @flock($fh, LOCK_UN); fclose($fh);
    raus(['fehler' => 'Ergebnis zu groß oder nicht kodierbar.'], 400);
}

ftruncate($fh, 0);
rewind($fh);
fwrite($fh, $neu);
fflush($fh);
@flock($fh, LOCK_UN);
fclose($fh);
@chmod($datei, 0664);

raus(['rev' => rev($datei), 'data' => (object)$daten]);
