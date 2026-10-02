/* Export für die Abrechnungsseiten (2026/, 2027/, …)
   -------------------------------------------------
   PDF (über den Druckdialog), CSV für Excel, JSON-Sicherung und
   Einspielen einer Sicherung. Die Seite stellt ihre Daten über
   window.almAbrechnung bereit (siehe Skript in abrechnung.html).   */
(function(){
  var A = window.almAbrechnung;
  if (!A) return;

  function datum(){
    var t = new Date();
    return ('0'+t.getDate()).slice(-2)+'.'+('0'+(t.getMonth()+1)).slice(-2)+'.'+t.getFullYear();
  }
  function isoDatum(){ return new Date().toISOString().slice(0,10); }

  function herunterladen(inhalt, name, typ){
    var blob = new Blob([inhalt], {type: typ});
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  }

  /* Gleiche Rechnung wie die Bilanz-Tabelle der Seite */
  function bilanz(){
    var ps = A.parteien(), as = A.ausgaben();
    var sumA = as.reduce(function(s,a){ return s+a.betrag; }, 0);
    var sumN = ps.reduce(function(s,p){ return s+p.naechte; }, 0);
    var satz = sumN > 0 ? sumA/sumN : 0;
    return {
      ausgaben: as, sumA: sumA, sumN: sumN, satz: satz,
      zeilen: ps.map(function(p){
        var gezahlt = as.filter(function(a){ return a.partei===p.id; }).reduce(function(s,a){ return s+a.betrag; }, 0);
        var kosten = p.naechte * satz;
        return {p:p, gezahlt:gezahlt, kosten:kosten, bilanz: gezahlt + p.anzahlung - kosten};
      })
    };
  }

  /* ---------- PDF / Drucken ---------- */
  document.getElementById('x-pdf').addEventListener('click', function(){
    document.getElementById('druck-stand').textContent = 'Stand ' + datum();
    window.print();
  });

  /* ---------- CSV für Excel (Semikolon, Dezimalkomma, UTF-8 mit BOM) ---------- */
  function feld(v){
    v = (v == null ? '' : String(v));
    return /[;"\n\r]/.test(v) ? '"' + v.replace(/"/g,'""') + '"' : v;
  }
  function zahl(n){ return (Math.round(n*100)/100).toFixed(2).replace('.', ','); }

  document.getElementById('x-csv').addEventListener('click', function(){
    var b = bilanz(), namen = {};
    b.zeilen.forEach(function(z){ namen[z.p.id] = z.p.name; });
    var z = [];
    z.push(['Abrechnung Almurlaub ' + A.jahr, 'Stand ' + datum()]);
    z.push([]);
    z.push(['AUSGABEN']);
    z.push(['Was', 'Wer hat gezahlt', 'Betrag €']);
    b.ausgaben.forEach(function(a){ z.push([a.text, namen[a.partei] || '?', zahl(a.betrag)]); });
    z.push(['Summe', '', zahl(b.sumA)]);
    z.push([]);
    z.push(['BILANZ']);
    z.push(['Partei', 'Übernachtungen', 'Kosten €', 'Ausgaben €', 'Anzahlung €', 'Bilanz €', '']);
    b.zeilen.forEach(function(r){
      var hinweis = r.bilanz < -0.005 ? 'zahlt' : (r.bilanz > 0.005 ? 'bekommt zurück' : 'passt');
      z.push([r.p.name, r.p.naechte, zahl(r.kosten), zahl(r.gezahlt), zahl(r.p.anzahlung), zahl(r.bilanz), hinweis]);
    });
    z.push([]);
    z.push(['Übernachtungen gesamt', b.sumN]);
    z.push(['Kosten je Übernachtung €', zahl(b.satz)]);
    var csv = '﻿' + z.map(function(r){ return r.map(feld).join(';'); }).join('\r\n') + '\r\n';
    herunterladen(csv, 'abrechnung-' + A.jahr + '-' + isoDatum() + '.csv', 'text/csv;charset=utf-8');
  });

  /* ---------- JSON-Sicherung ---------- */
  document.getElementById('x-json').addEventListener('click', function(){
    var d = A.daten();
    var sicherung = {
      typ: 'almurlaub-abrechnung',
      jahr: A.jahr,
      exportiert: new Date().toISOString(),
      daten: { parteien: d.parteien || {}, ausgaben: d.ausgaben || {} }
    };
    herunterladen(JSON.stringify(sicherung, null, 2),
      'abrechnung-' + A.jahr + '-' + isoDatum() + '.json', 'application/json');
  });

  /* ---------- Sicherung einspielen ---------- */
  document.getElementById('x-import').addEventListener('change', function(e){
    var datei = e.target.files[0];
    e.target.value = '';
    if (!datei) return;
    var leser = new FileReader();
    leser.onload = function(){
      var s;
      try { s = JSON.parse(leser.result); } catch(err) { alert('Des is koa gültige Sicherung (kein JSON).'); return; }
      var d = (s && s.daten) || s;
      if (!d || typeof d.parteien !== 'object') { alert('In der Datei steht keine Abrechnung.'); return; }
      var anzA = Object.keys(d.ausgaben || {}).length, anzP = Object.keys(d.parteien).length;
      var frage = 'Sicherung einspielen?\n\n' + anzP + ' Parteien, ' + anzA + ' Ausgaben' +
        (s.exportiert ? '\nvom ' + new Date(s.exportiert).toLocaleString('de-DE') : '') +
        '\n\nDer aktuelle Stand der Abrechnung ' + A.jahr + ' wird dabei für alle ERSETZT.';
      if (s.jahr && String(s.jahr) !== String(A.jahr))
        frage = '⚠️ Die Sicherung ist von ' + s.jahr + ', das hier ist die Abrechnung ' + A.jahr + '!\n\n' + frage;
      if (!confirm(frage)) return;
      A.sende({set: {parteien: d.parteien, ausgaben: d.ausgaben || {}}});
    };
    leser.readAsText(datei);
  });
})();
