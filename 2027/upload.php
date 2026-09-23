<?php
/**
 * upload.php – Foto-Upload für den Jahresbereich der Almurlaub-Website
 * -------------------------------------------------------------------
 * WICHTIG: Das Jahr wird automatisch aus dem Ordnernamen abgeleitet.
 * Liegt die Datei in /2027/, speichert sie nach <fotos_dir>/2027/
 * (fotos_dir aus config.php, Standard: /fotos).
 * Dieselbe Datei kann also unverändert in jeden Jahresordner kopiert werden.
 *
 * Schnittstelle (von fotos.html erwartet):
 *   GET                              -> {"fotos":[{id,datei,von,zeit}, ...]}
 *   POST aktion=upload, von, dateien[] -> {"ok":true,"hochgeladen":[...],
 *                                          "uebersprungen":N,"data":{"fotos":[...]}}
 *   POST aktion=loeschen, id           -> {"ok":true,"data":{"fotos":[...]}}
 */

declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex, nofollow');

// ---------------------------------------------------------------
//  Konfiguration
// ---------------------------------------------------------------
$cfgDatei   = __DIR__ . '/../config.php';
$cfg        = is_file($cfgDatei) ? (require $cfgDatei) : [];
$JAHR       = basename(__DIR__);                 // <- leitet z.B. "2027" ab
$FOTO_DIR   = ($cfg['fotos_dir'] ?? __DIR__ . '/../fotos') . '/' . $JAHR;   // Zielordner für die Bilder
$INDEX      = $FOTO_DIR . '/_index.json';        // Verzeichnis der Fotos
$MAX_BYTES  = 12 * 1024 * 1024;                  // 12 MB je Foto
$ERLAUBT    = [                                  // MIME-Typ => Dateiendung
    'image/jpeg' => 'jpeg',
    'image/png'  => 'png',
    'image/webp' => 'webp',
    'image/gif'  => 'gif',
];

// Sicherheitsnetz: nur vierstellige Jahreszahl als Ordnername zulassen
if (!preg_match('/^\d{4}$/', $JAHR)) {
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'Ordnername ist kein Jahr: ' . $JAHR]);
    exit;
}

// ---------------------------------------------------------------
//  Hilfsfunktionen
// ---------------------------------------------------------------
function raus(array $daten): never {
    echo json_encode($daten, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

function fehler(string $text, int $code = 400): never {
    http_response_code($code);
    raus(['ok' => false, 'error' => $text]);
}

function lade_index(string $index): array {
    if (!is_file($index)) return [];
    $roh = file_get_contents($index);
    if ($roh === false || $roh === '') return [];
    $daten = json_decode($roh, true);
    return is_array($daten) ? $daten : [];
}

function speichere_index(string $index, array $fotos): bool {
    $tmp = $index . '.tmp-' . bin2hex(random_bytes(4));
    $ok  = file_put_contents(
        $tmp,
        json_encode(array_values($fotos), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
        LOCK_EX
    );
    if ($ok === false) { @unlink($tmp); return false; }
    return rename($tmp, $index);
}

/** Neueste zuerst */
function sortiere(array $fotos): array {
    usort($fotos, fn($a, $b) => strcmp((string)($b['zeit'] ?? ''), (string)($a['zeit'] ?? '')));
    return $fotos;
}

// Zielordner sicherstellen
if (!is_dir($FOTO_DIR) && !@mkdir($FOTO_DIR, 0775, true) && !is_dir($FOTO_DIR)) {
    fehler('Foto-Ordner konnte nicht angelegt werden: fotos/' . $JAHR, 500);
}
if (!is_writable($FOTO_DIR)) {
    fehler('Foto-Ordner ist nicht beschreibbar: fotos/' . $JAHR, 500);
}

$fotos  = sortiere(lade_index($INDEX));
$aktion = $_POST['aktion'] ?? '';

// ---------------------------------------------------------------
//  GET – Liste ausgeben
// ---------------------------------------------------------------
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    raus(['fotos' => $fotos]);
}

// ---------------------------------------------------------------
//  POST: Löschen
// ---------------------------------------------------------------
if ($aktion === 'loeschen') {
    $id = (string)($_POST['id'] ?? '');
    if ($id === '') fehler('Keine ID angegeben.');

    $bleibt = [];
    foreach ($fotos as $f) {
        if (($f['id'] ?? '') === $id) {
            $datei = basename((string)($f['datei'] ?? ''));
            if ($datei !== '' && is_file($FOTO_DIR . '/' . $datei)) {
                @unlink($FOTO_DIR . '/' . $datei);
            }
            continue;
        }
        $bleibt[] = $f;
    }
    speichere_index($INDEX, $bleibt);
    raus(['ok' => true, 'data' => ['fotos' => sortiere($bleibt)]]);
}

// ---------------------------------------------------------------
//  POST: Upload
// ---------------------------------------------------------------
if ($aktion === 'upload') {
    $von = trim((string)($_POST['von'] ?? ''));
    if ($von === '') $von = 'Unbekannt';
    // Länge begrenzen – ohne mbstring-Abhängigkeit
    if (function_exists('mb_substr')) {
        if (mb_strlen($von, 'UTF-8') > 40) $von = mb_substr($von, 0, 40, 'UTF-8');
    } elseif (strlen($von) > 40) {
        $von = preg_replace('/[\x80-\xBF]+$/', '', substr($von, 0, 40)); // schneidet keine Umlaute kaputt
    }

    if (empty($_FILES['dateien']) || !isset($_FILES['dateien']['tmp_name'])) {
        fehler('Keine Dateien empfangen.');
    }

    $tmpListe   = (array)$_FILES['dateien']['tmp_name'];
    $fehlerliste = (array)$_FILES['dateien']['error'];
    $groessen   = (array)$_FILES['dateien']['size'];

    $hochgeladen   = [];
    $uebersprungen = 0;
    $finfo         = new finfo(FILEINFO_MIME_TYPE);

    foreach ($tmpListe as $i => $tmp) {
        // Grundprüfungen
        if (($fehlerliste[$i] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK
            || !is_uploaded_file((string)$tmp)) { $uebersprungen++; continue; }

        if (($groessen[$i] ?? 0) <= 0 || ($groessen[$i] ?? 0) > $MAX_BYTES) {
            $uebersprungen++; continue;
        }

        // Inhaltsbasierte Typprüfung – nicht auf den Dateinamen verlassen
        $mime = $finfo->file((string)$tmp);
        if (!is_string($mime) || !isset($ERLAUBT[$mime])) { $uebersprungen++; continue; }

        // Zusätzlich: muss ein echtes Bild sein
        $masse = @getimagesize((string)$tmp);
        if ($masse === false) { $uebersprungen++; continue; }

        $endung = $ERLAUBT[$mime];
        $zeit   = new DateTimeImmutable('now');
        $id     = $zeit->format('Ymd-His') . '-' . bin2hex(random_bytes(4));
        $datei  = $id . '.' . $endung;
        $ziel   = $FOTO_DIR . '/' . $datei;

        if (!@move_uploaded_file((string)$tmp, $ziel)) { $uebersprungen++; continue; }
        @chmod($ziel, 0644);

        $eintrag = [
            'id'    => $id,
            'datei' => $datei,
            'von'   => $von,
            'zeit'  => $zeit->format('c'),
        ];
        $fotos[]       = $eintrag;
        $hochgeladen[] = $eintrag;

        // Gleiche Sekunde + mehrere Bilder: eindeutige IDs sicherstellen
        usleep(1000);
    }

    if ($hochgeladen && !speichere_index($INDEX, $fotos)) {
        fehler('Fotos gespeichert, aber die Liste konnte nicht geschrieben werden.', 500);
    }

    raus([
        'ok'            => true,
        'hochgeladen'   => $hochgeladen,
        'uebersprungen' => $uebersprungen,
        'data'          => ['fotos' => sortiere($fotos)],
    ]);
}

fehler('Unbekannte Aktion.');
