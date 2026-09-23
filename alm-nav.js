/* Mobiles Burger-Menü für die Almurlaub-Navigation
   ------------------------------------------------
   Baut den Burger-Button und hängt die Unterseiten jedes Jahresbereichs
   ("Alm 2026", "Alm 2027", …) als aufklappbare Unterpunkte ins Menü.
   Die Jahreszahl steht NICHT im Code – jeder Hauptpunkt der Form
   "Alm <Jahr>" bekommt automatisch sein eigenes Untermenü.            */
(function(){
  var nav = document.querySelector('.alm-nav');
  if (!nav) return;
  var innen = nav.querySelector('.nav-innen');
  if (!innen) return;

  var btn = document.createElement('button');
  btn.className = 'nav-burger';
  btn.setAttribute('aria-label', 'Menü öffnen');
  btn.setAttribute('aria-expanded', 'false');
  btn.innerHTML = '☰';
  var logo = innen.querySelector('.logo');
  if (logo) logo.insertAdjacentElement('afterend', btn);
  else innen.insertBefore(btn, innen.firstChild);

  /* Unterseiten eines Jahresbereichs – Pendant zur .jahr-nav-innen.
     Bei Änderungen bitte beides pflegen. */
  var SUBSEITEN = [
    ['index.html',       'Übersicht'],
    ['einkauf.html',     '🛒 Einkaufsliste'],
    ['abrechnung.html',  '💰 Abrechnung'],
    ['fotos.html',       '📸 Fotos'],
    ['bierrechner.html', '🍺 Bierrechner']
  ];

  var aktuelleDatei = location.pathname.split('/').pop() || 'index.html';

  var jahrLinks = [];
  innen.querySelectorAll('a.nav-link').forEach(function(a){
    if (/^Alm\s+\d{4}$/.test(a.textContent.trim())) jahrLinks.push(a);
  });

  jahrLinks.forEach(function(almLink){
    var href  = almLink.getAttribute('href') || '';
    var basis = href.replace(/index\.html$/, '');
    var imBereich = almLink.classList.contains('aktiv');

    var zeile = document.createElement('div');
    zeile.className = 'nav-item-mit-sub';
    almLink.insertAdjacentElement('afterend', zeile);
    zeile.appendChild(almLink);

    var toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'nav-sub-toggle';
    toggle.innerHTML = '<span aria-hidden="true">▾</span>';
    toggle.setAttribute('aria-label', 'Untermenü ' + almLink.textContent.trim() + ' ein-/ausblenden');
    zeile.appendChild(toggle);

    var letzter = zeile, subs = [], hatAktiv = false;
    SUBSEITEN.forEach(function(seite){
      var link = document.createElement('a');
      link.className = 'nav-link nav-sub';
      link.href = basis + seite[0];
      link.textContent = seite[1];
      if (imBereich && seite[0] === aktuelleDatei){ link.classList.add('aktiv'); hatAktiv = true; }
      letzter.insertAdjacentElement('afterend', link);
      letzter = link;
      subs.push(link);
    });

    function setzeOffen(offen){
      subs.forEach(function(l){ l.classList.toggle('auf', offen); });
      toggle.classList.toggle('auf', offen);
      toggle.setAttribute('aria-expanded', offen ? 'true' : 'false');
    }
    setzeOffen(imBereich || hatAktiv);

    toggle.addEventListener('click', function(e){
      e.stopPropagation();
      setzeOffen(!toggle.classList.contains('auf'));
    });
  });

  function schliessen(){
    nav.classList.remove('offen');
    btn.innerHTML = '☰';
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-label', 'Menü öffnen');
  }
  btn.addEventListener('click', function(){
    var offen = nav.classList.toggle('offen');
    btn.innerHTML = offen ? '✕' : '☰';
    btn.setAttribute('aria-expanded', offen ? 'true' : 'false');
    btn.setAttribute('aria-label', offen ? 'Menü schließen' : 'Menü öffnen');
  });
  innen.querySelectorAll('a.nav-link').forEach(function(a){
    a.addEventListener('click', schliessen);
  });
  document.addEventListener('click', function(e){
    if (nav.classList.contains('offen') && !nav.contains(e.target)) schliessen();
  });
  window.addEventListener('resize', function(){
    if (window.innerWidth >= 800) schliessen();
  });
})();
