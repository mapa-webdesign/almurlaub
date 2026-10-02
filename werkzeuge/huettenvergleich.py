# Erzeugt huettenvergleich.html aus der Datenliste H. Aus dem Repo-Root ausführen:
#   python3 werkzeuge/huettenvergleich.py
# Kriterien je Hütte als 6 Zeichen: j = erfüllt, n = nicht erfüllt, ? = unbekannt
# Reihenfolge: 12 P./5 SZ · Alleinlage · Lagerfeuer · Brunnen · WC · warme Dusche
import html

# (gruppe, name, url, ort, land, höhe, gps, plätze, zimmer, kriterien, preis/woche, belegung – wird nicht angezeigt)
H = [
  # --- Aktuelle Kandidaten ---
  ('k','Hofer Hütte','https://www.huettenland.com/huette/1580/Hofer-Huette-in-den-Nockbergen/','Gmünd','Ktn',1750,'46.8686,13.5778',15,5,'?jjjjj','1.980 €','ab 13.08.'),
  ('k','Preimes Kasa','https://www.airbnb.de/rooms/1175192828385082031','Mörtschach','Ktn',None,'46.927,12.874',10,5,'njjjjj','2.150 €','14.–21.08.'),
  ('k','Kalserhütte','https://xn--kalserhtte-geb.at/','Oberdrauburg','Ktn',1800,'46.7613,12.9224',10,4,'nn??jj','ab 160 €/N.','Anfrage'),
  ('k','Larer Hütte','https://www.larerhuette.at/','Lessach','Sbg',1600,'',10,4,'n??jjj','ab 100 €/N.','Anfrage'),
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
  ('b','Huberalm','https://www.huettenpartner.com/huetten/gasteinertal/dor_sbg.html','Dorfgastein','Sbg',1150,'47.2768,13.0659',14,5,'jjjjj?','–','–'),
  ('b','Obere Roner Kasa','https://www.urlaubambauernhof.at/de/hoefe/ronerkasa','Mörtschach','Ktn',1450,'46.9205,12.8983',10,4,'n?jjjj','–','ab 28.08.'),
  ('b','Kreuzerhütte','https://www.urlaubambauernhof.at/de/hoefe/kreuzerhuette','Bad St. Leonhard','Ktn',1500,'46.9535,14.7982',10,5,'njnjjj','–','–'),
  ('b','Wallner Kasa','https://www.urlaubambauernhof.at/de/hoefe/wallnerkasa','Heiligenblut','Ktn',1600,'47.0481,12.8207',10,4,'njnjj?','–','–'),
  ('b','Mahrhütte Tschiernock','https://www.urlaubambauernhof.at/de/hoefe/marhuette','Eisentratten','Ktn',1700,'46.8777,13.5784',6,3,'nn?jjj','–','–'),
  ('b','Kreuzwirthütte','https://www.urlaubambauernhof.at/de/hoefe/kreuzwirthuette','Radenthein','Ktn',1500,'46.8462,13.7252',9,3,'n??jjj','–','belegt'),
  ('b','Sonnalmhütte','https://www.urlaubambauernhof.at/hoefe/sonnalmhuette','Gmünd','Ktn',1500,'46.9614,13.5419',11,4,'n?n?jj','–','–'),
  ('b','Bodener Alm','https://www.huettenland.com/huette/1302/Bodner-Almhuette-im-Kristeinertal/','Kristeinertal','OT',1500,'46.8157,12.5580',6,4,'n?njj?','–','–'),
  ('b','Lorenzer Hütte','','–','Ktn',None,'',None,None,'??????','–','–'),
  ('b','Hoisen Hütte','https://hoisenhuette.at/','Rennweg','Ktn',None,'',None,None,'??????','–','–'),
  ('b','Paulmahdhütte','https://www.paulmahdhuette.com','Rennweg','Ktn',None,'',None,None,'??????','–','–'),
  ('b','Rettensteinhütte','https://www.huettenzauber-tirol.at/huetten/rettensteinhuette','Aschau','T',None,'',None,None,'??????','–','–'),
]
KRIT = ['12 P. / 5 SZ','Alleinlage','Lagerfeuer','Brunnen','WC','warme Dusche']
KOPF = ['12&nbsp;P.<br>5&nbsp;SZ','Allein-<br>lage','Lager-<br>feuer','Brun-<br>nen','WC','warme<br>Dusche']
ZEICHEN = {'j':('✓','ok'),'n':('✗','nein'),'?':('?','offen')}

def punkte(k): return k.count('j')
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
    return (f'<tr class="p{punkte(k)}"><th scope="row">{n}</th><td>{ortz}</td><td class="mitte">{karte}</td>'
            f'<td class="zahl">{h}</td><td class="zahl">{z(pl)}</td><td class="zahl">{z(sz)}</td>{kk}'
            f'<td class="zahl punkte">{punkte(k)}</td><td>{html.escape(preis)}</td></tr>')

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
          <th>Preis/Woche</th></tr></thead>
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
</style>''')

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
</body>
</html>
'''
open('huettenvergleich.html','w',encoding='utf-8').write(kopf+body)
print('voll:', voll, '| 5/6:', [r[1] for r in fuenf])
