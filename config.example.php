<?php
/**
 * config.example.php – Vorlage
 * -----------------------------
 * Kopie anlegen als  config.php  und echte Werte eintragen.
 * config.php steht in .gitignore und landet NIE im Repository.
 *
 * Auf dem Server einmalig anlegen – ein git pull überschreibt sie nicht.
 */
return [
    // Bierparole für den Login
    'parole' => 'HIER-DIE-PAROLE',

    // Wert des Zugangs-Cookies. Beliebige lange Zeichenfolge.
    // Muss mit dem Wert in der .htaccess übereinstimmen!
    'cookie_wert' => 'HIER-EIN-LANGER-ZUFALLSWERT',

    // Wie lange der Login gemerkt wird
    'tage_gueltig' => 90,

    // Wo die Live-Daten liegen (außerhalb von Git)
    'daten_dir' => __DIR__ . '/daten',

    // Wo die hochgeladenen Fotos liegen (außerhalb von Git)
    'fotos_dir' => __DIR__ . '/fotos',
];
