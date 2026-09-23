<?php
/**
 * login.php – Bierparole für almurlaub.mapa-ai.de
 * ------------------------------------------------------
 * Prüft die Parole und setzt das Cookie, auf das die .htaccess achtet.
 * Muss selbst von der .htaccess ausgenommen sein (ist sie).
 */

/* Zugangsdaten kommen aus config.php (nicht im Repository).
   Fehlt sie, bricht der Login bewusst ab statt unsicher weiterzulaufen. */
$cfgDatei = __DIR__ . '/config.php';
if (!is_file($cfgDatei)) {
    http_response_code(500);
    exit('config.php fehlt – bitte aus config.example.php anlegen.');
}
$cfg = require $cfgDatei;

define('PAROLE',       (string)($cfg['parole'] ?? ''));
define('COOKIE_NAME',  'almauth');
define('COOKIE_WERT',  (string)($cfg['cookie_wert'] ?? ''));
define('TAGE_GUELTIG', (int)($cfg['tage_gueltig'] ?? 90));

if (PAROLE === '' || COOKIE_WERT === '' || str_starts_with(PAROLE, 'HIER-')) {
    http_response_code(500);
    exit('config.php ist noch nicht ausgefüllt.');
}

/* --- Zielseite nach dem Login (nur seiteninterne Pfade zulassen) --- */
function sicheresZiel(?string $z): string {
    if (!is_string($z) || $z === '') return '/';
    if ($z[0] !== '/' || str_starts_with($z, '//')) return '/';   // keine fremden Adressen
    if (str_contains($z, "\n") || str_contains($z, "\r")) return '/';
    if (preg_match('#^/(login|logout)\.php#i', $z)) return '/';
    return $z;
}
$ziel = sicheresZiel($_GET['ziel'] ?? $_POST['ziel'] ?? '/');

/* --- Schon angemeldet? Dann direkt weiter --- */
if (($_COOKIE[COOKIE_NAME] ?? '') === COOKIE_WERT && $_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: ' . $ziel);
    exit;
}

$fehler = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $eingabe = trim((string)($_POST['parole'] ?? ''));
    /* Gross-/Kleinschreibung egal – strtolower reicht, die Parole ist rein ASCII.
       Kein mbstring nötig, das ist nicht auf jedem Server aktiv. */
    if (hash_equals(strtolower(PAROLE), strtolower($eingabe))) {
        setcookie(COOKIE_NAME, COOKIE_WERT, [
            'expires'  => time() + 60 * 60 * 24 * TAGE_GUELTIG,
            'path'     => '/',
            'secure'   => (($_SERVER['HTTPS'] ?? '') === 'on')
                          || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https'),
            'httponly' => true,
            'samesite' => 'Lax',
        ]);
        header('Location: ' . $ziel);
        exit;
    }
    usleep(600000);                    // bremst stures Durchprobieren
    $fehler = 'Des war nix. Nochmal.';
}

header('Content-Type: text/html; charset=utf-8');
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex, nofollow');
?>
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bierparole – Urlaub auf der Alm</title>
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bitter:wght@400;600;800&family=Caveat:wght@500;700&display=swap" rel="stylesheet">
<style>
  :root{
    --holz-dunkel:#3a2a1c; --holz:#5a4130; --holz-hell:#7a5c42; --holz-grau:#8a7a68;
    --creme:#f4ecd9; --creme-dunkel:#e8dcc0;
    --schwammerl:#d99a3c; --schwammerl-hell:#eab861;
    --tanne:#3d5a3f; --geranie:#b8452f; --nebel:#aebbc4; --tinte:#2e2318;
  }
  *{box-sizing:border-box}
  body{
    margin:0;min-height:100vh;font-family:'Bitter',Georgia,serif;color:var(--creme);
    background:
      repeating-linear-gradient(90deg, rgba(0,0,0,.14) 0 2px, rgba(0,0,0,0) 2px 7px),
      linear-gradient(160deg, var(--holz) 0%, var(--holz-dunkel) 60%, #2a1d12 100%);
    display:flex;align-items:center;justify-content:center;padding:24px 16px;
  }
  .kasten{width:100%;max-width:560px;text-align:center}
  h1{
    font-family:'Caveat',cursive;font-size:clamp(2.3rem,9vw,3.4rem);
    margin:0 0 4px;color:var(--creme);text-shadow:0 2px 6px rgba(0,0,0,.5);
  }
  .spruch{color:var(--schwammerl-hell);font-size:.95rem;margin-bottom:26px;font-style:italic}

  /* --- Bierdeckel --- */
  .deckel-reihe{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-bottom:28px}
  .deckel{
    width:112px;height:112px;border-radius:50%;
    background:radial-gradient(circle at 50% 42%, var(--creme) 0 58%, var(--creme-dunkel) 58% 100%);
    border:3px solid rgba(46,35,24,.35);
    box-shadow:0 4px 12px rgba(0,0,0,.45), inset 0 0 0 6px rgba(46,35,24,.06);
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    padding:8px;color:var(--tinte);transform:rotate(var(--dreh,0deg));
  }
  .deckel .marke{font-weight:800;font-size:.74rem;line-height:1.15;letter-spacing:.02em}
  .deckel .sorte{font-size:.6rem;color:var(--holz-hell);margin-top:3px;line-height:1.2}
  .deckel .krug{font-size:1.15rem;margin-bottom:3px}

  /* --- Eingabe --- */
  form{display:flex;flex-direction:column;gap:12px;align-items:center}
  label{font-size:.9rem;color:var(--nebel)}
  input[type=password]{
    width:100%;max-width:320px;font-family:'Bitter',Georgia,serif;font-size:1.05rem;text-align:center;
    padding:13px 14px;border-radius:10px;border:2px solid rgba(217,154,60,.45);
    background:var(--creme);color:var(--tinte);
  }
  input[type=password]:focus{outline:3px solid var(--schwammerl);outline-offset:1px;border-color:transparent}
  button{
    font-family:'Bitter',Georgia,serif;font-size:1rem;font-weight:700;cursor:pointer;
    padding:12px 30px;border:none;border-radius:10px;
    background:var(--schwammerl);color:#2e2318;box-shadow:0 3px 0 #a9762a;
  }
  button:hover{background:var(--schwammerl-hell)}
  button:active{transform:translateY(2px);box-shadow:0 1px 0 #a9762a}
  .fehler{
    background:rgba(184,69,47,.22);border:1px solid var(--geranie);color:#ffd9d1;
    border-radius:10px;padding:10px 14px;margin-bottom:16px;font-size:.9rem;
  }
  .fuss{margin-top:30px;color:var(--holz-grau);font-size:.76rem}
  @media (max-width:420px){ .deckel{width:92px;height:92px} }
</style>
</head>
<body>
  <main class="kasten">
    <h1>🏔️ Urlaub auf der Alm</h1>
    <div class="spruch">Kein Zutritt für Schwachschwoaba</div>

    <div class="deckel-reihe" aria-hidden="true">
      <div class="deckel" style="--dreh:-4deg">
        <span class="krug">🍺</span>
        <span class="marke">Hoslbegga</span>
        <span class="sorte">Haselbacher Helles<br>Löwenbrauerei Passau</span>
      </div>
      <div class="deckel" style="--dreh:3deg">
        <span class="krug">🍺</span>
        <span class="marke">WaldGraf</span>
        <span class="sorte">Original Helles<br>G-Tränk, Röhrnbach</span>
      </div>
      <div class="deckel" style="--dreh:-2deg">
        <span class="krug">🍺</span>
        <span class="marke">Villacher</span>
        <span class="sorte">Märzen<br>Kärnten</span>
      </div>
      <div class="deckel" style="--dreh:5deg">
        <span class="krug">🍺</span>
        <span class="marke">Stiegl</span>
        <span class="sorte">Salzburg</span>
      </div>
    </div>

    <?php if ($fehler !== ''): ?>
      <div class="fehler" role="alert">🍺 <?= htmlspecialchars($fehler, ENT_QUOTES, 'UTF-8') ?></div>
    <?php endif; ?>

    <form method="post" action="login.php">
      <input type="hidden" name="ziel" value="<?= htmlspecialchars($ziel, ENT_QUOTES, 'UTF-8') ?>">
      <label for="parole">Bierparole?</label>
      <input type="password" id="parole" name="parole" autocomplete="current-password"
             autocapitalize="none" autocorrect="off" spellcheck="false" autofocus required>
      <button type="submit">Aufsperrn</button>
    </form>

    <div class="fuss">Bleibt 90 Tage gemerkt &middot; seit 1999</div>
  </main>
</body>
</html>
