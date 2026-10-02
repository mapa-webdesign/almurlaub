# Erzeugt huettenvergleich.html aus der Datenliste H. Aus dem Repo-Root ausführen:
#   python3 werkzeuge/huettenvergleich.py
# Kriterien je Hütte als 6 Zeichen: j = erfüllt, n = nicht erfüllt, ? = unbekannt
# Reihenfolge: 12 P./5 SZ · Alleinlage · Lagerfeuer · Brunnen · WC · warme Dusche
import html

# (gruppe, name, url, ort, land, höhe, gps, plätze, zimmer, kriterien, preis/woche, belegung – wird nicht angezeigt)
H = [
  # --- Aktuelle Kandidaten ---
  ('k','Hofer Hütte','https://www.huettenland.com/huette/1580/Hofer-Huette-in-den-Nockbergen/','Gmünd','Ktn',1750,'46.8686,13.5778',15,5,'?jjjjj','1.980 €','ab 13.08.'),
  ('k','Preimes Kasa','https://www.airbnb.de/rooms/1175192828385082031','Mörtschach','Ktn',None,'46.927,12.874',12,5,'jjjjjj','2.348 €','14.–21.08.'),
  ('k','Kalserhütte','https://xn--kalserhtte-geb.at/','Oberdrauburg','Ktn',1800,'46.7613,12.9224',10,4,'nn??jj','ab 160 €/N.','Anfrage'),
  ('k','Larer Hütte','https://www.larerhuette.at/','Lessach','Sbg',1600,'',10,4,'n??jjj','ab 100 €/N.','Anfrage'),
  ('k','Reifhütte','https://www.huettenpartner.com/huetten/lachtal/rei_stm.html','Lachtal','Stmk',1660,'47.2514,14.3529',12,4,'njj?jj','1.490 €','07.–14.08.'),  # Feuerstelle laut Gästebewertung 2022
  ('k','Scharfetter Hütte','https://www.huettenpartner.com/huetten/abtenau/jos_sbg.html','Postalm','Sbg',1170,'47.635604,13.413717',12,4,'nj?jjj','ab 1.250 €','07.–14.08.'),  # 10 P. + 2 Zusatzbetten; Preis Sommer für 10 P.
  ('k','Huberalm','https://www.huettenpartner.com/huetten/gasteinertal/dor_sbg.html','Dorfgastein','Sbg',1150,'47.2768,13.0659',14,5,'jjjjjj','auf Anfrage','–'),  # Feuerstelle + warme Dusche laut Martin
  ('k','Obere Roner Kasa','https://www.urlaubambauernhof.at/de/hoefe/ronerkasa','Mörtschach','Ktn',1450,'46.9205,12.8983',10,4,'n?jjjj','≈ 2.040 €','28.08.–18.09.'),
  ('k','Lorenzer Hütte','https://www.bergwelten.com/t/b/23018','Kleblach-Lind','Ktn',1700,'46.766,13.366',11,5,'njjjjj','980 €','–'),  # laut Martin: 140 €/Nacht; GPS = Ort im Drautal, nicht die Hütte
  ('k','Hoisen Hütte','https://hoisenhuette.at/','Rennweg','Ktn',None,'',None,None,'??????','950 € (2025)','–'),
  # --- Neue Funde ---
  ('n','Thomannbauerhütte','https://www.urlaubambauernhof.at/de/hoefe/thomannbauerhuette','Gmünd','Ktn',1500,'46.8971,13.5948',14,5,'jj?jjj','Anfrage','Anfrage'),
  ('n','Almhütte Kuhgraben','https://www.huetten.com/de/huette/almhuette-kuhgraben-rt30204.html','Bad St. Leonhard','Ktn',1250,'46.9528,14.7119',12,5,'jj??jj','2.690 €','Anfrage'),
  ('n','Hütte BOA-STM','https://www.huettenpartner.com/huetten/donnersbach/boa_stm.html','Donnersbach','Stmk',1100,'47.4654,14.1104',12,5,'jjn?j?','1.490 €','07.–14.08.'),
  ('n','Gamsbergstube','https://www.huetten.com/de/huette/gamsbergstube-rt34542.html','Pack','Stmk',1400,'46.9258,15.0166',19,8,'jjn?jj','2.959 €','frei'),
  ('n','Schwarzenbichlalm','https://www.urlaubambauernhof.at/de/hoefe/schwarzenbichlalm','Zederhaus','Sbg',1350,'47.1835,13.4408',14,5,'j???j?','Anfrage','?'),
  ('n','Griesslhütte','https://www.urlaubambauernhof.at/de/hoefe/griesslhuette','Flachau','Sbg',None,'47.3509,13.3737',12,6,'j???j?','Anfrage','?'),
  ('n','Hütte PBF-00003','https://www.kaernten-ferienwohnungen.com/huette-pbf-00003/','Bad St. Leonhard','Ktn',1200,'46.9557,14.7646',12,6,'jjn?jj','ab 110 €/N.','belegt'),
  ('n','Faschinghütte','https://www.huetten.com/de/huette/faschinghuette-rt37165.html','Bischofshofen','Sbg',None,'47.3892,13.1640',16,6,'j?n?jj','3.490 €','So–So frei'),
  ('n','Schafferalm','https://www.urlaubambauernhof.at/de/hoefe/schafferalm','St. Stefan o. L.','Stmk',None,'47.3529,14.9373',12,5,'njj?jj','Anfrage','ab 30.08.'),
  ('n','Untersöllhof','https://www.huetten.com/de/huette/untersoellhof-rt45507.html','Krimml','Sbg',1000,'47.2263,12.1821',19,5,'jnj?jj','4.490 €','frei'),
  ('n','Raunighof','https://www.urlaubambauernhof.at/de/hoefe/raunighof','St. Margareten','Ktn',1500,'46.5364,14.4593',14,5,'jnjjj?','4.038 €','ab 07.08.'),
  ('n','Zwengerhof','https://www.huettenland.com/huette/891/Zwengerhof-Villgratental-in-Osttirol/','Villgraten','OT',1410,'46.8150,12.3395',15,6,'j?njjj','Anfrage','07.–14.08.'),
  ('n','Bauernhaus Oberlohr','https://www.huettenland.com/huette/1475/','Kals','OT',1300,'46.9839,12.6405',18,9,'j?n?jj','Anfrage','07.–14.08.'),
  ('n','Moselebauer Alm','https://www.huetten.com/','Bad St. Leonhard','Ktn',1600,'46.9541,14.6901',14,6,'jn??jj','2.790 €','07.–14.08.'),
  ('n','Eseihütte','https://www.urlaubambauernhof.at/de/hoefe/eseihuette','Göriach','Sbg',1290,'47.2068,13.7552',15,4,'njjjnj','Anfrage','?'),
  ('n','Galsterbergalm','https://www.urlaubambauernhof.at/de/hoefe/galsterbergalm','Pruggern','Stmk',None,'47.4177,13.8864',10,5,'nnjjjj','Anfrage','?'),
  ('n','Holzhütte Tuxertal','https://www.huettenland.com/huette/6/','Tux','T',1200,'47.1583,11.7681',14,4,'nnn?jj','Anfrage','frei'),
  # --- Schon dort / früher angefragt ---
  ('b','Kreuzerhütte','https://www.urlaubambauernhof.at/de/hoefe/kreuzerhuette','Bad St. Leonhard','Ktn',1500,'46.9535,14.7982',10,5,'njnjjj','–','–'),
  ('b','Wallner Kasa','https://www.urlaubambauernhof.at/de/hoefe/wallnerkasa','Heiligenblut','Ktn',1600,'47.0481,12.8207',10,4,'njnjj?','–','–'),
  ('b','Mahrhütte Tschiernock','https://www.urlaubambauernhof.at/de/hoefe/marhuette','Eisentratten','Ktn',1700,'46.8777,13.5784',6,3,'nn?jjj','–','–'),
  ('b','Kreuzwirthütte','https://www.urlaubambauernhof.at/de/hoefe/kreuzwirthuette','Radenthein','Ktn',1500,'46.8462,13.7252',9,3,'n??jjj','–','belegt'),
  ('b','Sonnalmhütte','https://www.urlaubambauernhof.at/hoefe/sonnalmhuette','Gmünd','Ktn',1500,'46.9614,13.5419',11,4,'n?n?jj','–','–'),
  ('b','Bodener Alm','https://www.huettenland.com/huette/1302/Bodner-Almhuette-im-Kristeinertal/','Kristeinertal','OT',1500,'46.8157,12.5580',6,4,'n?njj?','–','–'),
  ('b','Paulmahdhütte','https://www.paulmahdhuette.com','Rennweg','Ktn',None,'',None,None,'??????','–','–'),
  ('b','Rettensteinhütte','https://www.huettenzauber-tirol.at/huetten/rettensteinhuette','Aschau','T',None,'',None,None,'??????','–','–'),
]
KRIT = ['12 P. / 5 SZ','Alleinlage','Lagerfeuer','Brunnen','WC','warme Dusche']
KOPF = ['12&nbsp;P.<br>5&nbsp;SZ','Allein-<br>lage','Lager-<br>feuer','Brun-<br>nen','WC','warme<br>Dusche']
ZEICHEN = {'j':('✓','ok'),'n':('✗','nein'),'?':('?','offen')}

def punkte(k): return k.count('j')
def slug(name):
    import re
    t = name.lower().replace('ä','ae').replace('ö','oe').replace('ü','ue').replace('ß','ss')
    return re.sub(r'[^a-z0-9]+','-',t).strip('-')
_ids = [slug(r[1]) for r in H]
assert len(_ids) == len(set(_ids)), 'doppelte Hütten-ID'
def tsd(n): return f'{n:,}'.replace(',', '.')

def zeile(r):
    g,name,url,ort,land,hoehe,gps,pl,sz,k,preis,aug = r
    n = f'<a href="{url}" target="_blank" rel="noopener">{html.escape(name)}</a>' if url else html.escape(name)
    if gps:
        la,lo = gps.split(',')
        karte = (f'<a class="karte-knopf" href="https://www.openstreetmap.org/?mlat={la}&amp;mlon={lo}#map=14/{la}/{lo}" '
                 f'target="_blank" rel="noopener" title="{html.escape(name)} auf der Karte" aria-label="{html.escape(name)} auf der Karte">📍</a>')
    else:
        karte = '<span class="leer">–</span>'
    ortz = html.escape(ort) + (f' <span class="land">{land}</span>' if land else '')
    z = lambda v: f'{v}' if v is not None else '<span class="leer">–</span>'
    h = f'{tsd(hoehe)} m' if hoehe else '<span class="leer">–</span>'
    kk = ''.join(f'<td class="k {ZEICHEN[x][1]}">{ZEICHEN[x][0]}</td>' for x in k)
    wertung = ('<td class="wertung"><span class="sterne">'
               + ''.join(f'<button type="button" class="stern" data-n="{i}" aria-label="{i} von 5">★</button>' for i in range(1,6))
               + '</span><button type="button" class="raus-knopf" title="ausschließen">✕</button></td>')
    return (f'<tr class="p{punkte(k)}" data-id="{slug(name)}" data-sigma="{punkte(k)}"><th scope="row"><span class="name">{n}</span><div class="grund"></div></th><td>{ortz}</td><td class="mitte">{karte}</td>'
            f'<td class="zahl">{h}</td><td class="zahl">{z(pl)}</td><td class="zahl">{z(sz)}</td>{kk}'
            f'<td class="zahl punkte">{punkte(k)}</td><td>{html.escape(preis)}</td>{wertung}</tr>')

def tabelle(gruppe, titel, em):
    rows = sorted([r for r in H if r[0]==gruppe], key=lambda r: -punkte(r[9]))
    kopf = ''.join(f'<th class="k" title="{t}">{h}</th>' for h,t in zip(KOPF,KRIT))
    return f'''
  <section>
    <div class="sek-titel"><span class="em">{em}</span><h2>{titel}</h2><div class="linie"></div></div>
    <div class="karte"><div class="tab-scroll">
      <table class="tabelle vergleich">
        <thead><tr><th>Hütte</th><th>Ort</th><th class="mitte">Karte</th><th class="zahl">Höhe</th>
          <th class="zahl">Plätze</th><th class="zahl">Zimmer</th>{kopf}<th class="zahl" title="erfüllte Kriterien">Σ</th>
          <th>Preis/Woche</th><th class="mitte">Unsere Wertung</th></tr></thead>
        <tbody>{''.join(zeile(r) for r in rows)}</tbody>
      </table>
    </div></div>
  </section>'''

voll  = [r[1] for r in H if punkte(r[9])==6]
fuenf = [r for r in H if punkte(r[9])==5]
voll_txt = ('<strong>'+', '.join(voll)+'</strong>') if voll else '<strong>Keine – nachweislich.</strong> Bei den besten fehlt jeweils nur eine Angabe.'
fuenf_li = ''.join(f'<li><strong>{html.escape(r[1])}</strong> – offen: '
                   + ', '.join(n for n,x in zip(KRIT,r[9]) if x!='j') + '</li>' for r in fuenf)

seite = open('huettensuche.html', encoding='utf-8').read()
kopf = seite[:seite.index('<header class="seitenkopf">')].replace(
    '<title>Hütten-Suche – Urlaub auf der Alm</title>','<title>Hütten-Vergleich – Urlaub auf der Alm</title>')
kopf = kopf.replace('<link rel="stylesheet" href="alm.css">','''<link rel="stylesheet" href="alm.css">
<style>
  .vergleich{font-size:.84rem}
  .vergleich th,.vergleich td{white-space:nowrap;padding:8px 5px}
  .vergleich thead th{vertical-align:bottom;line-height:1.15;letter-spacing:.04em;font-size:.68rem}
  .vergleich .mitte{text-align:center}
  .vergleich tbody th{text-align:left;text-transform:none;letter-spacing:0;font-size:.9rem;font-weight:700;
    position:sticky;left:0;background:var(--creme);border-bottom:1px dashed rgba(90,65,48,.3)}
  .vergleich tbody th a{color:var(--holz-dunkel);text-decoration:none}
  .vergleich tbody th a:hover{text-decoration:underline}
  .vergleich .land{color:var(--holz-grau);font-size:.78rem}
  .vergleich .leer{color:var(--holz-grau)}
  .vergleich td.k,.vergleich th.k{text-align:center;font-weight:700;width:2.8em}
  .vergleich td.ok{color:var(--tanne)}
  .vergleich td.nein{color:var(--geranie)}
  .vergleich td.offen{color:var(--holz-grau);font-weight:400}
  .vergleich td.punkte{font-weight:800}
  .vergleich tr.p6 td.punkte,.vergleich tr.p5 td.punkte{color:var(--tanne)}
  .karte-knopf{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:50%;
    background:var(--tanne);text-decoration:none;font-size:.9rem;box-shadow:0 2px 0 rgba(0,0,0,.2)}
  .karte-knopf:hover{background:var(--tanne-hell)}
  .legende{font-size:.82rem;color:var(--holz);margin-top:12px}
  .vergleich td.wertung{text-align:center}
  .vergleich .stern,.vergleich .raus-knopf{background:none;border:0;cursor:pointer;font:inherit;padding:2px 1px;line-height:1}
  .vergleich .stern{font-size:1.15rem;color:var(--creme-dunkel);-webkit-text-stroke:1px var(--holz-grau)}
  .vergleich .stern.an{color:var(--schwammerl);-webkit-text-stroke:1px var(--holz)}
  .vergleich .sterne:hover .stern{color:var(--schwammerl-hell)}
  .vergleich .sterne .stern:hover~.stern{color:var(--creme-dunkel)}
  .vergleich .raus-knopf{margin-left:8px;width:24px;height:24px;border-radius:50%;color:var(--geranie);
    border:1.5px solid var(--geranie);font-weight:700;font-size:.8rem}
  .vergleich .raus-knopf:hover{background:var(--geranie);color:var(--creme)}
  .vergleich .grund{font-size:.74rem;font-weight:400;color:var(--geranie);white-space:normal;max-width:16em}
  .vergleich tr.raus td:not(.wertung){opacity:.4}
  .vergleich tr.raus .name,.vergleich tr.raus .name a{text-decoration:line-through;color:var(--holz-grau)}
  .vergleich tr.raus td.wertung .sterne{visibility:hidden}
  .vergleich tr.raus .raus-knopf{color:var(--tanne);border-color:var(--tanne)}
  .vergleich tr.raus .raus-knopf:hover{background:var(--tanne);color:var(--creme)}
  .ohne-raus .vergleich tr.raus{display:none}
  .wertung-leiste{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;justify-content:space-between;margin-top:12px;font-size:.88rem}
  .wertung-leiste label{cursor:pointer}
</style>''')

SKRIPT = r'''<script>
(function(){
  var API = 'api.php?doc=huetten2027';
  var state = {}, syncEl = document.getElementById('sync'), aus = document.getElementById('raus-aus');
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function eintrag(id){ return (state.h && state.h[id]) || {}; }

  function render(){
    document.querySelectorAll('table.vergleich tbody').forEach(function(tb){
      var rows = Array.prototype.slice.call(tb.rows);
      rows.forEach(function(tr, i){
        if (tr.dataset.pos === undefined) tr.dataset.pos = i;
        var e = eintrag(tr.dataset.id), n = +e.sterne || 0, raus = !!e.raus;
        tr.classList.toggle('raus', raus);
        tr.querySelectorAll('.stern').forEach(function(b){ b.classList.toggle('an', +b.dataset.n <= n); });
        var k = tr.querySelector('.raus-knopf');
        k.textContent = raus ? '↺' : '✕';
        k.title = raus ? 'wieder reinnehmen' : 'ausschließen';
        tr.querySelector('.grund').innerHTML = raus ? '✕ raus' + (e.grund ? ': ' + esc(e.grund) : '') : '';
      });
      rows.sort(function(a, b){
        var ea = eintrag(a.dataset.id), eb = eintrag(b.dataset.id);
        return (!!ea.raus - !!eb.raus) || ((+eb.sterne||0) - (+ea.sterne||0)) || (a.dataset.pos - b.dataset.pos);
      }).forEach(function(tr){ tb.appendChild(tr); });
    });
  }

  function setStatus(ok, text){
    syncEl.className = 'sync-status' + (ok ? '' : ' offline');
    syncEl.innerHTML = '<span class="punkt"></span>' + esc(text);
  }
  function anwenden(json){
    var neu = JSON.stringify(json.data || {});
    if (neu !== JSON.stringify(state)) { state = json.data || {}; render(); }
    var t = new Date();
    setStatus(true, 'live · Stand ' + ('0'+t.getHours()).slice(-2)+':'+('0'+t.getMinutes()).slice(-2)+':'+('0'+t.getSeconds()).slice(-2));
  }
  function lade(){
    fetch(API).then(function(r){ return r.json(); }).then(anwenden)
      .catch(function(){ setStatus(false, 'offline – versuche erneut …'); });
  }
  function sende(body){
    fetch(API, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)})
      .then(function(r){ return r.json(); }).then(anwenden)
      .catch(function(){ setStatus(false, 'Speichern fehlgeschlagen'); lade(); });
  }

  document.addEventListener('click', function(ev){
    var b = ev.target.closest('.vergleich .stern, .vergleich .raus-knopf');
    if (!b) return;
    var tr = b.closest('tr'), id = tr.dataset.id, e = eintrag(id), p = 'h.' + id + '.';
    var name = tr.querySelector('.name').textContent;
    if (b.classList.contains('stern')) {
      var n = +b.dataset.n, s = {};
      if ((+e.sterne||0) === n) sende({unset: [p + 'sterne']});
      else { s[p + 'sterne'] = n; sende({set: s}); }
    } else if (e.raus) {
      sende({unset: [p + 'raus', p + 'grund']});
    } else {
      var grund = prompt('Warum fliagt „' + name + '“ raus? (optional)', '');
      if (grund === null) return;
      var s2 = {}; s2[p + 'raus'] = 1;
      if (grund.trim()) s2[p + 'grund'] = grund.trim().slice(0, 120);
      sende({set: s2});
    }
  });

  try { aus.checked = localStorage.getItem('huetten-raus-aus') === '1'; } catch(e) {}
  function ausblenden(){ document.body.classList.toggle('ohne-raus', aus.checked); }
  aus.addEventListener('change', function(){
    ausblenden();
    try { localStorage.setItem('huetten-raus-aus', aus.checked ? '1' : '0'); } catch(e) {}
  });
  ausblenden();

  lade();
  setInterval(lade, 4000);
  document.addEventListener('visibilitychange', function(){ if (!document.hidden) lade(); });
})();
</script>'''

body = f'''<header class="seitenkopf">
  <h1>Hütten-Vergleich ⚖️</h1>
  <div class="untertitel">Alle Hütten gegen unsere Wunschliste</div>
</header>

<main class="wrap">

  <p style="margin-top:6px"><a class="btn sekundaer" href="huettensuche.html">← zurück zur Hütten-Suche</a></p>

  <section>
    <div class="sek-titel"><span class="em">🏆</span><h2>Erfüllt alles?</h2><div class="linie"></div></div>
    <div class="karte">
      <p>Alle sechs Kriterien: {voll_txt}</p>
      <p style="margin-top:10px">5 von 6:</p>
      <ul style="margin:6px 0 0 20px;line-height:1.7">{fuenf_li}</ul>
      <p class="legende"><span style="color:var(--tanne);font-weight:700">✓</span> erfüllt ·
        <span style="color:var(--geranie);font-weight:700">✗</span> nicht erfüllt ·
        <span style="color:var(--holz-grau)">?</span> unbekannt – nachfragen · Σ = erfüllte Kriterien ·
        Ktn = Kärnten, Sbg = Salzburg, Stmk = Steiermark, T = Tirol, OT = Osttirol</p>
    </div>
  </section>

  <div class="wertung-leiste">
    <span>⭐ Sterne vergeben, ✕ schließt eine Hütte aus (gilt für alle, live). Sortiert nach Wertung, dann Σ.</span>
    <label><input type="checkbox" id="raus-aus"> Ausgeschlossene ausblenden</label>
    <span class="sync-status" id="sync"><span class="punkt"></span>verbinde …</span>
  </div>
{tabelle('k','Aktuelle Kandidaten 2027','📨')}
{tabelle('n','Neue Funde','🔎')}
{tabelle('b','Schon dort oder angefragt','✅')}

  <div class="hinweis-band">
    ℹ️ Stand 02.10.2026, aus den Hütten-Seiten der Portale. Höhen gerundet, Preise ohne Gewähr –
    im Detail wird vor der Anfrage nochmal geprüft. Wer mehr weiß: Martin Bescheid sagen.
  </div>

  <footer>
    <span class="feuer">🔥</span>
    Hütten-Vergleich &middot; Stand 02.10.2026
  </footer>
</main>

<script src="alm-nav.js" defer></script>
{SKRIPT}
</body>
</html>
'''
open('huettenvergleich.html','w',encoding='utf-8').write(kopf+body)
print('voll:', voll, '| 5/6:', [r[1] for r in fuenf])
