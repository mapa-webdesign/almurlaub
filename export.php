<?php
/**
 * export.php – Sicherung der Laufzeitdaten
 * -----------------------------------------
 * Packt alles, was NICHT im Git-Repository liegt, in ein ZIP:
 *   - daten/daten-*.json  (Einkaufshaken, Abrechnung, Bierrechner)
 *   - fotos/              (hochgeladene Bilder)
 *
 * Aufruf im Browser:  /export.php      -> ZIP zum Herunterladen
 *                     /export.php?info=1 -> nur Übersicht als JSON
 *
 * Geschützt durch den normalen Login (die .htaccess schützt diese Datei mit).
 */

declare(strict_types=1);

$cfgDatei = __DIR__ . '/config.php';
$cfg = is_file($cfgDatei) ? (require $cfgDatei) : [];
$DATEN = $cfg['daten_dir'] ?? __DIR__ . '/daten';
$FOTOS = $cfg['fotos_dir'] ?? __DIR__ . '/fotos';

/* --- Übersicht, was gesichert würde --- */
function sammle(string $ordner): array {
    if (!is_dir($ordner)) return [];
    $raus = [];
    $it = new RecursiveIteratorIterator(
        new RecursiveDirectoryIterator($ordner, FilesystemIterator::SKIP_DOTS)
    );
    foreach ($it as $f) {
        if ($f->isFile()) $raus[] = $f->getPathname();
    }
    return $raus;
}

$dateien = array_merge(sammle($DATEN), sammle($FOTOS));
$gesamt  = array_sum(array_map(fn($f) => filesize($f) ?: 0, $dateien));

if (isset($_GET['info'])) {
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    echo json_encode([
        'dateien' => count($dateien),
        'bytes'   => $gesamt,
        'daten'   => count(sammle($DATEN)),
        'fotos'   => count(sammle($FOTOS)),
        'zeit'    => date('c'),
    ], JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT);
    exit;
}

if (!$dateien) {
    http_response_code(404);
    exit('Nichts zu sichern – weder Daten noch Fotos vorhanden.');
}

$stempel = date('Y-m-d-Hi');
$wurzel  = realpath(__DIR__);
$hinweis = "Almurlaub – Laufzeitdaten\n" .
           "Erstellt: " . date('d.m.Y H:i') . "\n" .
           "Dateien: " . count($dateien) . "\n\n" .
           "Enthält Live-Daten und Fotos, die NICHT im Git-Repository liegen.\n" .
           "Zurückspielen: Inhalt ins Webverzeichnis entpacken.\n";

/* Internen Pfad im Archiv bestimmen */
function internerPfad(string $real, string $wurzel): string {
    return str_starts_with($real, $wurzel)
        ? ltrim(substr($real, strlen($wurzel)), '/\\')
        : basename($real);
}

/* --- Weg 1: ZipArchive, falls vorhanden --- */
if (class_exists('ZipArchive')) {
    $tmp = tempnam(sys_get_temp_dir(), 'alm');
    $zip = new ZipArchive();
    if ($zip->open($tmp, ZipArchive::OVERWRITE) !== true) {
        http_response_code(500);
        exit('ZIP konnte nicht erstellt werden.');
    }
    foreach ($dateien as $f) {
        $real = realpath($f);
        if ($real !== false) $zip->addFile($real, internerPfad($real, $wurzel));
    }
    $zip->addFromString('SICHERUNG.txt', $hinweis);
    $zip->close();

    header('Content-Type: application/zip');
    header('Content-Disposition: attachment; filename="almurlaub-daten-' . $stempel . '.zip"');
    header('Content-Length: ' . filesize($tmp));
    header('Cache-Control: no-store');
    readfile($tmp);
    @unlink($tmp);
    exit;
}

/* --- Weg 2: tar.gz über PharData --- */
if (class_exists('PharData')) {
    $basis = sys_get_temp_dir() . '/almurlaub-' . $stempel . '-' . bin2hex(random_bytes(3));
    try {
        $tar = new PharData($basis . '.tar');
        foreach ($dateien as $f) {
            $real = realpath($f);
            if ($real !== false) $tar->addFile($real, internerPfad($real, $wurzel));
        }
        $tar->addFromString('SICHERUNG.txt', $hinweis);
        $tar->compress(Phar::GZ);
        unset($tar);
        @unlink($basis . '.tar');

        $fertig = $basis . '.tar.gz';
        header('Content-Type: application/gzip');
        header('Content-Disposition: attachment; filename="almurlaub-daten-' . $stempel . '.tar.gz"');
        header('Content-Length: ' . filesize($fertig));
        header('Cache-Control: no-store');
        readfile($fertig);
        @unlink($fertig);
        exit;
    } catch (Throwable $e) {
        @unlink($basis . '.tar');
        http_response_code(500);
        exit('Archiv konnte nicht erstellt werden: ' . $e->getMessage());
    }
}

http_response_code(500);
exit('Weder ZipArchive noch PharData verfügbar – bitte Daten per FTP sichern.');

/* ab hier nicht mehr erreichbar */
