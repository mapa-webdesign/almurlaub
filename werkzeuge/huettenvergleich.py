# Erzeugt huettenvergleich.html aus der Datenliste H. Aus dem Repo-Root ausführen:
#   python3 werkzeuge/huettenvergleich.py
import html
# Kriterienwerte: 'j' = ✓ (steht auf Seite), 'a' = ✓* (aus Ausstattung abgeleitet), 'm' = ✓ laut Martin,
# 'n' = ✗, 'g' = ✗ nur Grill, '?' = unbekannt
# (gruppe, name, status, gemeinde, region, land, hoehe, gps, plaetze, K1..K6, preis, august, url, notiz)
H=[
# --- Aktuelle Kandidaten / Angebote ---
('k','Hofer Hütte','Angebot','Gmünd','Lieser-/Maltatal, Nockberge','Kärnten','1.750 m','46.8686,13.5778','bis 15 · 5 SZ + Matratzenlager','?','j','j','j','j','a','1.980 € (10 P., inkl. Kurtaxe)','belegt bis 13.08., frei Fr 13.–27.08.','https://www.huettenland.com/huette/1580/Hofer-Huette-in-den-Nockbergen/','12 nur mit Matratzenlager'),
('k','Preimes Kasa','bestätigt 14.–21.08.','Rettenbach (laut Airbnb)','Wangenitz, Mölltal','Kärnten','–','46.927,12.874','10 · 5 DZ','n','j','j','j','j','j','2.150 € + Taxe 4,50 €/P./Tag','frei 14.–21.08.; 01.–13.08. belegt','https://www.airbnb.de/rooms/1175192828385082031','GPS ungefähr'),
('k','Kalserhütte','Anfrage läuft','Oberdrauburg','Drautal, Lienzer Dolomiten','Kärnten','1.800 m','46.7613,12.9224','10 · 4 SZ','n','n','?','?','j','j','ab 160 €/Nacht + NK','kein Online-Kalender','https://xn--kalserhtte-geb.at/','Hochstadelhaus (bewirtschaftet) wenige Meter entfernt; GPS = Hof im Tal'),
('k','Larer Hütte','Anfrage läuft','Lessach','Prebersee, Lungau','Salzburg','1.600 m','','ca. 10 · 4 SZ + Heubett','n','?','?','j','j','j','ab 100 €/Nacht + NK','kein Online-Kalender','https://www.larerhuette.at/',''),
# --- Neue Funde ---
('n','Thomannbauerhütte','neu','Gmünd (Innernöring)','Nöringgraben, Lieser-/Maltatal','Kärnten','über 1.500 m','46.8971,13.5948','bis 14 · 5 SZ','j','j','?','j','j','j','auf Anfrage','kein Online-Kalender','https://www.urlaubambauernhof.at/de/hoefe/thomannbauerhuette','„Absolute Alleinlage“, Warmwasser über Solar. Fam. Mößler +43 676 4050730'),
('n','Almhütte Kuhgraben','neu','Bad St. Leonhard (Kliening)','Klippitztörl, Lavanttal','Kärnten','1.250 m','46.9528,14.7119','12 · 5 SZ','j','j','?','?','j','a','2.690 € + NK','online nicht buchbar → anfragen','https://www.huetten.com/de/huette/almhuette-kuhgraben-rt30204.html',''),
('n','Hütte BOA-STM','neu','Donnersbach','Niedere Tauern','Steiermark','1.100 m','47.4654,14.1104','12 · 5 SZ','j','j','g','?','j','?','1.490 € + NK','07.–14.08. frei','https://www.huettenpartner.com/huetten/donnersbach/boa_stm.html','Name nur als Code – vorm Anfragen klären'),
('n','Gamsbergstube','neu','Pack','Hebalm','Steiermark','1.400 m','46.9258,15.0166','19 · 8 SZ','j','j','g','?','j','a','2.959 € + 300 € Wäsche','ganzer August frei','https://www.huetten.com/de/huette/gamsbergstube-rt34542.html','100 m zum Hebalm-See, Lifte in der Nähe'),
('n','Schwarzenbichlalm','neu','Zederhaus','Riedingtal, Lungau','Salzburg','1.350 m','47.1835,13.4408','bis 14 · 5 Zimmer','j','?','?','?','j','?','auf Anfrage','Kalender unklar','https://www.urlaubambauernhof.at/de/hoefe/schwarzenbichlalm',''),
('n','Griesslhütte','neu','Flachau','Grießenkar','Salzburg','–','47.3509,13.3737','bis 12 · 6 SZ','j','?','?','?','j','?','auf Anfrage','Kalender unklar','https://www.urlaubambauernhof.at/de/hoefe/griesslhuette','direkt an der Skipiste'),
('n','Hütte PBF-00003','neu','Bad St. Leonhard','Klippitztörl, Lavanttal','Kärnten','1.200 m','46.9557,14.7646','12 · 6 DZ (2 Wohneinheiten)','j','j','g','?','j','a','ab 110 €/Nacht','2027 komplett gesperrt','https://www.kaernten-ferienwohnungen.com/huette-pbf-00003/',''),
('n','Faschinghütte','neu','Bischofshofen','Haidberg','Salzburg','–','47.3892,13.1640','16 · 6 SZ','j','?','g','?','j','a','3.490 € + Strom','nur So–So frei (01./08./15.08.)','https://www.huetten.com/de/huette/faschinghuette-rt37165.html',''),
('n','Schafferalm','neu','St. Stefan ob Leoben','Erzberg-Leoben','Steiermark','–','47.3529,14.9373','9 + 3 Zusatzbetten · 5 SZ','n','j','j','?','j','a','auf Anfrage','frei nur 01.08. und 30.–31.08.','https://www.urlaubambauernhof.at/de/hoefe/schafferalm',''),
('n','Untersöllhof','neu','Krimml','Krimml','Salzburg','1.000 m','47.2263,12.1821','19 · 5 Zimmer','j','n','j','?','j','a','4.490 € + NK','August frei','https://www.huetten.com/de/huette/untersoellhof-rt45507.html','700 m bis Krimml'),
('n','Raunighof','neu','St. Margareten im Rosental','Karawanken','Kärnten','bis 1.500 m','46.5364,14.4593','bis 14 · 5 SZ','j','n','j','j','j','?','4.038 €','ab 07.08. frei','https://www.urlaubambauernhof.at/de/hoefe/raunighof','Hüttengruppe'),
('n','Zwengerhof','neu','Villgratental','Villgratental','Osttirol','1.410 m','46.8150,12.3395','bis 15 · 6 SZ','j','?','g','j','j','a','auf Anfrage (Preisrechner)','07.–14.08. frei','https://www.huettenland.com/huette/891/Zwengerhof-Villgratental-in-Osttirol/','Bauernhaus, Nähe Dorf'),
('n','Bauernhaus Oberlohr','neu','Kals am Großglockner','Großglockner','Osttirol','1.300 m','46.9839,12.6405','bis 18 · 9 SZ','j','?','g','?','j','a','auf Anfrage (Preisrechner)','07.–14.08. frei','https://www.huettenland.com/huette/1475/','Bauernhaus'),
('n','Moselebauer Alm','neu','Bad St. Leonhard (Kliening)','Klippitztörl','Kärnten','1.600 m','46.9541,14.6901','14 · 6 SZ','j','n','?','?','j','a','2.790 € + 54 €/Tag Energie','07.–14.08. frei','https://www.huetten.com/','Hüttendorf mit Restaurant'),
('n','Eseihütte','neu','Göriach','Lungau','Salzburg','1.287 m','47.2068,13.7552','bis 15 · 4 Räume','n','j','j','j','n','j','auf Anfrage','Kalender unklar','https://www.urlaubambauernhof.at/de/hoefe/eseihuette','in der Hütte nur Plumpsklo'),
('n','Galsterbergalm','neu','Michaelerberg-Pruggern','Ennstal','Steiermark','–','47.4177,13.8864','10 Betten + Couches · 5 SZ','n','n','j','j','j','a','auf Anfrage','Kalender unklar','https://www.urlaubambauernhof.at/de/hoefe/galsterbergalm','Skigebiet'),
('n','Holzhütte Tuxertal','neu','Tuxertal','Zillertal','Tirol','1.200 m','47.1583,11.7681','bis 14 · 4 SZ','n','n','g','?','j','a','auf Anfrage','August frei','https://www.huettenland.com/huette/6/','gehört zum Bauerngut'),
# --- Schon dort / früher angefragt ---
('b','Huberalm','besucht 2024','Dorfgastein','Gasteinertal','Salzburg','1.150 m','47.2768,13.0659','bis 14 · 5 SZ','j','j','m','j','j','?','–','–','https://www.huettenpartner.com/huetten/gasteinertal/dor_sbg.html','bei Hüttenpartner als DOR-SBG; nur 1 Dusche/WC'),
('b','Obere Roner Kasa','7× besucht','Mörtschach','Wangenitztal, Hohe Tauern','Kärnten','1.450 m','46.9205,12.8983','10 · 3 DZ + 4 unterm Dach','n','?','j','j','j','j','–','August belegt, frei ab 28.08.','https://www.urlaubambauernhof.at/de/hoefe/ronerkasa','Untere Roner Kasa ca. 250 m entfernt'),
('b','Kreuzerhütte','angefragt 2026','Bad St. Leonhard (Kliening)','Lavanttal','Kärnten','bis 1.500 m','46.9535,14.7982','10 · 5 DZ','n','j','g','j','j','j','–','–','https://www.urlaubambauernhof.at/de/hoefe/kreuzerhuette',''),
('b','Wallner Kasa','besucht 2014','Heiligenblut','Großglockner','Kärnten','ca. 1.600 m','47.0481,12.8207','10 · 4 SZ','n','j','g','j','j','?','–','–','https://www.urlaubambauernhof.at/de/hoefe/wallnerkasa',''),
('b','Mahrhütte Tschiernock','2× besucht','Eisentratten','Lieser-/Maltatal','Kärnten','1.700 m','46.8777,13.5784','bis 6 · 3 Zimmer','n','n','?','j','j','j','–','–','https://www.urlaubambauernhof.at/de/hoefe/marhuette','Teil eines Almhüttendorfs'),
('b','Kreuzwirthütte','angefragt (2028)','Radenthein','Langalmtal, Nockberge','Kärnten','über 1.500 m','46.8462,13.7252','bis 9 · 3 SZ','n','?','?','j','j','j','–','2027 ausgebucht','https://www.urlaubambauernhof.at/de/hoefe/kreuzwirthuette',''),
('b','Sonnalmhütte','angefragt 2026','Gmünd (Stubeck)','Lieser-/Maltatal','Kärnten','über 1.500 m','46.9614,13.5419','bis 11 · 4 Zimmer','n','?','g','?','j','j','–','–','https://www.urlaubambauernhof.at/hoefe/sonnalmhuette','Verpflegungshütte in der Nähe'),
('b','Bodener Alm','besucht 2011','Kristeinertal','Kristeinertal','Osttirol','1.500 m','46.8157,12.5580','bis 6 · 4 SZ','n','?','g','j','j','?','–','–','https://www.huettenland.com/huette/1302/Bodner-Almhuette-im-Kristeinertal/',''),
('b','Lorenzer Hütte','12× besucht','–','–','Kärnten','–','','–','?','?','?','?','?','?','–','–','','auf keinem Portal gefunden'),
('b','Hoisen Hütte','4× besucht','Rennweg am Katschberg','Krangler Alm','Kärnten','–','','–','?','?','?','?','?','?','–','–','https://hoisenhuette.at/','Portal-Treffer „Hoisenkasa“ (Saalachtal) ist eine andere Hütte'),
('b','Paulmahdhütte','besucht 1999','Rennweg','Lausnitzalm, Nockberge','Kärnten','–','','–','?','?','?','?','?','?','–','–','https://www.paulmahdhuette.com','auf keinem freigegebenen Portal'),
('b','Rettensteinhütte','besucht 2013','Aschau','Spertental, Kitzbüheler Alpen','Tirol','–','','–','?','?','?','?','?','?','–','–','https://www.huettenzauber-tirol.at/huetten/rettensteinhuette','auf keinem freigegebenen Portal'),
]
ZEICHEN={'j':('✓','ok','steht auf der Hütten-Seite'),'a':('✓*','ok','aus der Ausstattung abgeleitet'),'m':('✓','ok','laut Martin'),
         'n':('✗','nein','nicht erfüllt'),'g':('✗ Grill','nein','nur Grill, keine Lagerfeuerstelle'),'?':('?','offen','auf der Seite nicht erkennbar')}
def punkte(k): return sum(1 for x in k if x in 'jam')
def zelle(x):
    t,c,tip=ZEICHEN[x]; return f'<td class="k {c}" title="{tip}">{t}</td>'
def zeile(r):
    g,name,status,gem,reg,land,hoehe,gps,pl,*rest=r
    k=rest[:6]; preis,aug,url,notiz=rest[6:]
    p=punkte(k)
    n=f'<a href="{url}" target="_blank" rel="noopener">{html.escape(name)}</a>' if url else html.escape(name)
    if notiz: n+=f'<span class="notiz">{html.escape(notiz)}</span>'
    lage=' · '.join(x for x in (gem,reg,land) if x and x!='–') or '–'
    if gps:
        la,lo=gps.split(',')
        lage+=f'<span class="notiz"><a href="https://www.openstreetmap.org/?mlat={la}&amp;mlon={lo}#map=14/{la}/{lo}" target="_blank" rel="noopener">📍 Karte</a></span>'
    return (f'<tr class="p{p}"><th scope="row">{n}</th><td>{html.escape(status)}</td><td>{lage}</td><td class="zahl">{hoehe}</td>'
            f'<td>{html.escape(pl)}</td>'+''.join(zelle(x) for x in k)+
            f'<td class="zahl punkte">{p}/6</td><td>{html.escape(preis)}</td><td>{html.escape(aug)}</td></tr>')
def tabelle(gruppe,titel,em):
    rows=sorted([r for r in H if r[0]==gruppe],key=lambda r:-punkte(r[9:15]))
    return f'''
  <section>
    <div class="sek-titel"><span class="em">{em}</span><h2>{titel}</h2><div class="linie"></div></div>
    <div class="karte"><div class="tab-scroll">
      <table class="tabelle vergleich">
        <thead><tr><th>Hütte</th><th>Status</th><th>Lage</th><th class="zahl">Höhe</th><th>Plätze / Zimmer</th>
          <th title="Platz für 12, min. 5 Schlafzimmer">12 P.<br>5 SZ</th><th title="Almhütte in Alleinlage">Allein&shy;lage</th>
          <th title="Lagerfeuerstelle">Lager&shy;feuer</th><th title="Brunnen (Grand)">Brunnen</th><th title="Fließend Wasser mit WC">WC</th>
          <th title="Warme Dusche">warme Dusche</th><th class="zahl">Σ</th><th>Preis / Woche</th><th>August 2027</th></tr></thead>
        <tbody>{''.join(zeile(r) for r in rows)}</tbody>
      </table>
    </div></div>
  </section>'''
voll=[r[1] for r in H if punkte(r[9:15])==6]
fuenf=sorted([r for r in H if punkte(r[9:15])==5],key=lambda r:r[0])
seite=open('huettensuche.html',encoding='utf-8').read()
kopf=seite[:seite.index('<header class="seitenkopf">')].replace('<title>Hütten-Suche – Urlaub auf der Alm</title>','<title>Hütten-Vergleich – Urlaub auf der Alm</title>')
kopf=kopf.replace('<link rel="stylesheet" href="alm.css">','''<link rel="stylesheet" href="alm.css">
<style>
  .vergleich th,.vergleich td{white-space:nowrap}
  .vergleich tbody th{text-align:left;font-weight:700;white-space:normal;min-width:180px;position:sticky;left:0;background:var(--creme)}
  .vergleich tbody th{text-transform:none;letter-spacing:0;font-size:.9rem;color:var(--tinte)}
  .vergleich a{color:var(--holz-dunkel)}
  .vergleich .notiz a{color:var(--tanne)}
  .vergleich .notiz{display:block;font-weight:400;font-size:.74rem;color:var(--holz-grau);font-style:italic;white-space:normal}
  .vergleich td:nth-child(3){white-space:normal;min-width:180px}
  .vergleich td.k{text-align:center;font-weight:700}
  .vergleich td.ok{color:var(--tanne)}
  .vergleich td.nein{color:var(--geranie)}
  .vergleich td.offen{color:var(--holz-grau)}
  .vergleich tr.p6 th,.vergleich tr.p6 td.punkte{color:var(--tanne)}
  .vergleich td.punkte{font-weight:800}
  .legende{font-size:.82rem;color:var(--holz);line-height:1.7}
  .legende b{display:inline-block;min-width:2.2em}
</style>''')
voll_txt = ('<strong>'+', '.join(voll)+'</strong>') if voll else '<strong>Keine – nachweislich.</strong> Bei den besten fehlt jeweils nur eine Angabe.'
fuenf_li=''.join(f'<li><strong>{html.escape(r[1])}</strong> ({html.escape(r[2])}) – offen: '+', '.join(n for n,x in zip(['12 P./5 SZ','Alleinlage','Lagerfeuer','Brunnen','WC','warme Dusche'],r[9:15]) if x not in 'jam')+'</li>' for r in fuenf)
body=f'''<header class="seitenkopf">
  <h1>Hütten-Vergleich ⚖️</h1>
  <div class="untertitel">Alle Hütten gegen unsere Wunschliste – was erfüllt welche, wo liegt sie wirklich?</div>
</header>

<main class="wrap">

  <p style="margin-top:6px"><a class="btn sekundaer" href="huettensuche.html">← zurück zur Hütten-Suche</a></p>

  <section>
    <div class="sek-titel"><span class="em">🏆</span><h2>Erfüllt alles?</h2><div class="linie"></div></div>
    <div class="karte">
      <p>Alle sechs Kriterien: {voll_txt}</p>
      <p style="margin-top:10px">5 von 6 erfüllt:</p>
      <ul style="margin:6px 0 0 20px;line-height:1.7">{fuenf_li}</ul>
      <p class="legende" style="margin-top:12px">
        <b style="color:var(--tanne)">✓</b>steht auf der Hütten-Seite (oder laut Martin) ·
        <b style="color:var(--tanne)">✓*</b>aus der Ausstattung abgeleitet ·
        <b style="color:var(--geranie)">✗</b>nicht erfüllt („Grill“ = nur Grill, keine Feuerstelle) ·
        <b style="color:var(--holz-grau)">?</b>nicht erkennbar – nachfragen.<br>
        Spalten = unsere Wunschliste: Platz für 12 &amp; mind. 5 Schlafzimmer · Alleinlage · Lagerfeuerstelle ·
        Brunnen (Grand) · fließend Wasser mit WC · warme Dusche. Σ = erfüllte Kriterien.
      </p>
    </div>
  </section>
{tabelle('k','Aktuelle Kandidaten 2027','📨')}
{tabelle('n','Neue Funde (Okt. 2026)','🔎')}
{tabelle('b','Schon dort oder früher angefragt','✅')}

  <div class="hinweis-band">
    ℹ️ Stand 02.10.2026, aus den Hütten-Seiten der Portale (huettenland, huetten.com, Urlaub am Bauernhof, Hüttenpartner,
    kaernten-ferienwohnungen, Airbnb). Preise ohne Gewähr, Belegung laut Online-Kalender – verbindlich erst mit Anfrage.
    Wer mehr weiß (z. B. Feuerstelle bei der Lorenzer Hütte): Martin Bescheid sagen.
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
print('voll:',voll); print('5/6:',[r[1] for r in fuenf])
