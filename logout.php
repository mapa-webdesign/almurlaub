<?php
/**
 * logout.php – Abmelden (Cookie löschen)
 * Muss von der .htaccess ausgenommen sein (ist sie).
 */

const COOKIE_NAME = 'almauth';   // Name ist fest, der Wert steht in config.php

$sicher = (($_SERVER['HTTPS'] ?? '') === 'on')
       || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https');

/* Cookie auf abgelaufen setzen – gleiche Parameter wie beim Setzen,
   sonst löscht der Browser es nicht zuverlässig. */
setcookie(COOKIE_NAME, '', [
    'expires'  => time() - 3600,
    'path'     => '/',
    'secure'   => $sicher,
    'httponly' => true,
    'samesite' => 'Lax',
]);
unset($_COOKIE[COOKIE_NAME]);

header('Cache-Control: no-store');
header('X-Robots-Tag: noindex, nofollow');
header('Content-Type: text/html; charset=utf-8');
?>
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="refresh" content="3; url=login.php">
<title>Abgemeldet – Urlaub auf der Alm</title>
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bitter:wght@400;600&family=Caveat:wght@700&display=swap" rel="stylesheet">
<style>
  :root{
    --holz-dunkel:#3a2a1c; --holz:#5a4130; --holz-grau:#8a7a68;
    --creme:#f4ecd9; --schwammerl:#d99a3c; --schwammerl-hell:#eab861;
  }
  *{box-sizing:border-box}
  body{
    margin:0;min-height:100vh;font-family:'Bitter',Georgia,serif;color:var(--creme);
    background:
      repeating-linear-gradient(90deg, rgba(0,0,0,.14) 0 2px, rgba(0,0,0,0) 2px 7px),
      linear-gradient(160deg, var(--holz) 0%, var(--holz-dunkel) 60%, #2a1d12 100%);
    display:flex;align-items:center;justify-content:center;padding:24px 16px;text-align:center;
  }
  h1{font-family:'Caveat',cursive;font-size:clamp(2rem,8vw,3rem);margin:0 0 8px}
  p{color:var(--schwammerl-hell);margin:0 0 22px}
  a{
    display:inline-block;font-weight:700;text-decoration:none;
    padding:12px 28px;border-radius:10px;background:var(--schwammerl);color:#2e2318;
    box-shadow:0 3px 0 #a9762a;
  }
  a:hover{background:var(--schwammerl-hell)}
  .fuss{margin-top:24px;color:var(--holz-grau);font-size:.78rem}
</style>
</head>
<body>
  <main>
    <h1>🍺 Pfiat di!</h1>
    <p>Du bist abgemeldet. Bis zum nächsten Mal.</p>
    <a href="login.php">Wieder aufsperrn</a>
    <div class="fuss">Weiterleitung in 3 Sekunden …</div>
  </main>
</body>
</html>
