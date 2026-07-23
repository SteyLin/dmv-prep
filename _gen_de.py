#!/usr/bin/env python3
"""
Generates /de/ Germany Fahrschule Theoriepruefung page (bilingual DE/EN).

Tabbed + bilingual layout: a Deutsch/English toggle switches every label,
question, option and explanation live. Tabs:
  - full    : Vollstaendige Pruefung / Full Practice Exam
  - signs   : Verkehrszeichen / Traffic Signs
  - rules   : Verkehrsregeln / Driving Rules
  - safety  : Verkehrssicherheit / Road Safety
Timed Mock Exam + Review Wrong Answers added. JS kept OUTSIDE the f-string.
Reuses COMMON_CSS + AdSense Auto-ads.
"""
import os, json

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "de")
os.makedirs(OUT, exist_ok=True)

PUB = "ca-pub-7503096549502749"
ADSENSE = f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={PUB}" crossorigin="anonymous"></script>'

COMMON_CSS = """
  :root{
    --bg:#f7f9fc; --card:#ffffff; --ink:#1f2933; --muted:#6b7280;
    --accent:#2563eb; --accent-soft:#eff4ff; --good:#16a34a; --good-soft:#ecfdf3;
    --bad:#dc2626; --bad-soft:#fef2f2; --line:#e5e7eb; --explain:#f8fafc;
  }
  html[data-theme="dark"]{
    --bg:#0f1419; --card:#1a2027; --ink:#e6e9ee; --muted:#9aa4b2;
    --accent:#3b82f6; --accent-soft:#16223b; --good:#22c55e; --good-soft:#0f2a1c;
    --bad:#ef4444; --bad-soft:#2a1518; --line:#2a323c; --explain:#141a21;
  }
  *{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
  body{background:var(--bg);color:var(--ink);min-height:100vh;line-height:1.5;transition:background .2s,color .2s;}
  body{background-image:radial-gradient(1200px 600px at 50% -10%, var(--accent-soft) 0%, transparent 60%);}
  .wrap{max-width:1100px;margin:0 auto;padding:28px 20px 80px;}
  .topbar{display:flex;justify-content:flex-end;align-items:center;gap:10px;margin-bottom:14px;flex-wrap:wrap;}
  .theme-btn{background:var(--card);border:1px solid var(--line);color:var(--ink);padding:8px 14px;border-radius:10px;cursor:pointer;font-size:.85rem;font-weight:600;transition:.15s;}
  .theme-btn:hover{border-color:var(--accent);}
  header{text-align:center;margin:18px 0 22px;}
  h1{font-size:2.2rem;font-weight:900;letter-spacing:-.03em;}
  h1 .em{color:var(--accent);}
  .sub{color:var(--muted);margin-top:10px;font-size:1.05rem;max-width:780px;margin-left:auto;margin-right:auto;}
  a{color:var(--accent);}
  .breadcrumb{color:var(--muted);font-size:.85rem;margin-bottom:12px;}
  .breadcrumb a{text-decoration:none;}
  .card{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:26px;box-shadow:0 8px 30px rgba(0,0,0,.08);margin-bottom:16px;}

  .langbar{display:flex;justify-content:center;gap:8px;margin-bottom:18px;}
  .langbtn{background:var(--card);border:1px solid var(--line);color:var(--ink);padding:9px 18px;border-radius:999px;cursor:pointer;font-size:.9rem;font-weight:700;transition:.12s;}
  .langbtn:hover{border-color:var(--accent);}
  .langbtn.active{background:var(--accent);color:#fff;border-color:var(--accent);}

  .tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;}
  .tab{background:var(--card);border:1px solid var(--line);color:var(--ink);padding:11px 16px;border-radius:12px;cursor:pointer;font-size:.92rem;font-weight:700;transition:.12s;flex:1 1 auto;text-align:center;}
  .tab:hover{border-color:var(--accent);}
  .tab.active{background:var(--accent);color:#fff;border-color:var(--accent);}
  .tab .tcount{display:block;font-size:.74rem;font-weight:600;opacity:.8;margin-top:2px;}

  .exambar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:18px;}
  .exambar .timed{background:var(--card);border:1px solid var(--line);color:var(--accent);padding:9px 16px;border-radius:12px;font-weight:800;font-size:.95rem;display:none;}
  .exambar .act{padding:11px 18px;font-size:.92rem;}

  .meta{display:flex;justify-content:space-between;align-items:center;color:var(--muted);font-size:.85rem;margin-bottom:16px;}
  .badge{display:inline-block;background:var(--accent-soft);color:var(--accent);padding:5px 12px;border-radius:999px;font-size:.78rem;font-weight:700;}
  .q-text{font-size:1.18rem;font-weight:700;line-height:1.45;margin-bottom:18px;scroll-margin-top:20px;}
  .opt{display:block;width:100%;text-align:left;background:var(--card);border:1.5px solid var(--line);color:var(--ink);padding:15px 18px;border-radius:12px;margin-bottom:12px;cursor:pointer;font-size:1.02rem;transition:.12s;}
  .opt:hover{border-color:var(--accent);background:var(--accent-soft);}
  .opt.sel{border-color:var(--accent);background:var(--accent-soft);font-weight:700;}
  .opt.correct{border-color:var(--good);background:var(--good-soft);color:var(--good);font-weight:700;}
  .opt.wrong{border-color:var(--bad);background:var(--bad-soft);color:var(--bad);font-weight:700;}
  .opt:disabled{cursor:default;}
  .explain{background:var(--explain);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:8px;padding:12px 14px;margin-top:14px;font-size:.9rem;color:var(--muted);line-height:1.5;}
  .nav{display:flex;justify-content:space-between;gap:12px;margin-top:20px;}
  .act{background:var(--accent);color:#fff;border:none;padding:13px 24px;border-radius:12px;font-size:1rem;font-weight:700;cursor:pointer;transition:.12s;}
  .act:hover{filter:brightness(.92);}
  .act.ghost{background:var(--card);color:var(--ink);border:1.5px solid var(--line);}
  .act:disabled{opacity:.4;cursor:not-allowed;}
  .result{text-align:center;padding:8px 0;}
  .score{font-size:3.4rem;font-weight:900;letter-spacing:-.04em;margin:10px 0;}
  .verdict{color:var(--muted);font-size:1.02rem;margin-bottom:20px;}
  .foot{color:var(--muted);font-size:.78rem;margin-top:10px;line-height:1.6;text-align:center;}
  .src{font-size:.76rem;color:var(--muted);margin-top:22px;text-align:center;line-height:1.6;border-top:1px solid var(--line);padding-top:16px;}
  .pickgrid{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px;justify-content:center;}
  .pickgrid .pn{width:34px;height:34px;border-radius:9px;border:1px solid var(--line);background:var(--card);color:var(--muted);font-weight:700;font-size:.82rem;cursor:pointer;}
  .pickgrid .pn.done{background:var(--good-soft);color:var(--good);border-color:var(--good);}
  .pickgrid .pn.wrong{background:var(--bad-soft);color:var(--bad);border-color:var(--bad);}
"""

JS = r"""
const DATA = __DATA_JSON__;
const I18N = {
  de: { full:"Vollstaendige Pruefung", signs:"Verkehrszeichen", rules:"Verkehrsregeln", safety:"Verkehrssicherheit",
    back:"← Zurueck", next:"Weiter →", finish:"Beenden ✓", restart:"Test wiederholen", alltests:"← Alle Tests",
    done:"Pruefung beendet", answered:"Beantwortet", of:"von", pass:"% korrekt. Sie sind im bestandenen Bereich - gut gemacht!", fail:"% korrekt. Lernen Sie die Verkehrsregeln und versuchen Sie es erneut.",
    review:"🔁 Falsche wiederholen", timeTitle:"⏱ Simulierte Pruefung", timeLeft:"Zeit", reviewDone:"← Zurueck zu den Tests", reviewComplete:"Wiederholung abgeschlossen", allok:"Alle korrigiert - super!", again:"Wiederholen und erneut versuchen." },
  en: { full:"Full Practice Exam", signs:"Traffic Signs", rules:"Driving Rules", safety:"Road Safety",
    back:"← Back", next:"Next →", finish:"Finish ✓", restart:"Restart This Test", alltests:"← All Tests",
    done:"Exam Complete", answered:"Answered", of:"of", pass:"% correct. You're in the passing range - nice work!", fail:"% correct. Keep studying the road rules and try again.",
    review:"🔁 Review Wrong Answers", timeTitle:"⏱ Timed Mock Exam", timeLeft:"Time", reviewDone:"← Back to Tests", reviewComplete:"Review Complete", allok:"All corrected - great!", again:"Keep reviewing and try again." }
};
let lang = "de";
let curTab = "full";
let idx=0, picks=[], answered=[];
let timed = false, timeLeft = 0, timerId = null;
const quiz=document.getElementById('quiz');
const done=document.getElementById('done');
const tabBadge=document.getElementById('tabBadge');
const timeBox=document.getElementById('timeBox');
function Q(q){ return lang==="de" ? q.q_de : q.q_en; }
function OPTS(q){ return lang==="de" ? q.options_de : q.options_en; }
function EXPL(q){ return lang==="de" ? q.e_de : q.e_en; }
function L(k){ return I18N[lang][k]; }
function fmt(s){ const m=Math.floor(s/60), ss=s%60; return (m<10?'0':'')+m+':'+(ss<10?'0':'')+ss; }
function startTimer(){ clearInterval(timerId); timeLeft = DATA[curTab].length*60; timeBox.textContent='⏱ '+fmt(timeLeft); timeBox.style.display='inline-block';
  timerId=setInterval(function(){ timeLeft--; timeBox.textContent='⏱ '+fmt(timeLeft); if(timeLeft<=0){ clearInterval(timerId); finish(); } },1000); }
function stopTimer(){ clearInterval(timerId); timeBox.style.display='none'; }
function tabLabel(t){ return lang==="de" ? document.querySelector('.tab[data-tab="'+t+'"]').dataset.labelDe : document.querySelector('.tab[data-tab="'+t+'"]').dataset.labelEn; }

function loadTab(tab, useTimed){
  curTab=tab; idx=0; timed = !!useTimed;
  const qs=DATA[tab];
  picks=new Array(qs.length).fill(-1); answered=new Array(qs.length).fill(false);
  done.classList.add('hidden'); quiz.classList.remove('hidden');
  tabBadge.textContent = tabLabel(tab)+(timed?' ('+L('timeTitle')+')':'');
  document.querySelectorAll('.tab').forEach(function(t){ t.classList.toggle('active', t.dataset.tab===tab); });
  if(timed) startTimer(); else stopTimer();
  render();
}
function render(){
  const qs=DATA[curTab]; const q=qs[idx];
  document.getElementById('qProg').textContent=(idx+1)+' / '+qs.length;
  document.getElementById('qCount').textContent=L('answered')+' '+answered.filter(Boolean).length+' '+L('of')+' '+qs.length;
  document.getElementById('qHolder').innerHTML='<div class="q-text" id="q'+(idx+1)+'">'+(idx+1)+'. '+Q(q)+'</div>';
  const opts=document.getElementById('opts'); opts.innerHTML='';
  OPTS(q).forEach(function(opt,i){
    const b=document.createElement('button'); b.className='opt'; b.textContent=opt;
    if(picks[idx]===i) b.classList.add('sel');
    if(answered[idx]){
      if(i===q.answer) b.classList.add('correct');
      else if(i===picks[idx]) b.classList.add('wrong');
      b.disabled=true;
    }
    b.onclick=function(){ choose(i); }; opts.appendChild(b);
  });
  if(answered[idx] && EXPL(q)){ const ex=document.createElement('div'); ex.className='explain'; ex.innerHTML='💡 '+EXPL(q); opts.appendChild(ex); }
  document.getElementById('prevBtn').disabled = idx===0;
  document.getElementById('nextBtn').textContent = (idx===qs.length-1)?L('finish'):L('next');
  renderGrid();
}
function renderGrid(){
  const qs=DATA[curTab]; const g=document.getElementById('pickGrid'); g.innerHTML='';
  qs.forEach(function(q,i){
    const b=document.createElement('button'); b.className='pn'; b.textContent=(i+1);
    if(answered[i]){ b.classList.add('done'); if(picks[i]!==q.answer) b.classList.add('wrong'); }
    b.onclick=function(){ idx=i; render(); }; g.appendChild(b);
  });
}
function choose(i){ if(answered[idx]) return; picks[idx]=i; answered[idx]=true; render(); }
document.getElementById('nextBtn').onclick=function(){
  if(!answered[idx]){ alert(lang==="de"?"Bitte eine Antwort auswaehlen.":"Please select an answer."); return; }
  if(idx<DATA[curTab].length-1){ idx++; render(); } else finish();
};
document.getElementById('prevBtn').onclick=function(){ if(idx>0){ idx--; render(); } };
function wrongList(){ return DATA[curTab].map(function(q,i){ return i; }).filter(function(i){ return picks[i]!==DATA[curTab][i].answer; }); }
function finish(){
  stopTimer();
  const qs=DATA[curTab];
  let correct=0; qs.forEach(function(q,i){ if(picks[i]===q.answer) correct++; });
  const total=qs.length; const pct=Math.round(correct/total*100);
  quiz.classList.add('hidden'); done.classList.remove('hidden');
  document.getElementById('doneBadge').textContent=tabLabel(curTab)+(timed?' ('+L('timeTitle')+')':'');
  document.getElementById('score').textContent=correct+' / '+total;
  document.getElementById('verdict').textContent = pct>=80 ? L('pass').replace('%',pct) : L('fail').replace('%',pct);
  const wl=wrongList();
  const rb=document.getElementById('reviewBtn');
  rb.style.display = wl.length? 'inline-block':'none';
  rb.textContent = L('review')+' ('+wl.length+')';
}
document.getElementById('retryBtn').onclick=function(){ loadTab(curTab, timed); };
document.getElementById('tabsBtn').onclick=function(){ done.classList.add('hidden'); quiz.classList.remove('hidden'); };
document.getElementById('reviewBtn').onclick=function(){ const wl=wrongList(); if(!wl.length) return; reviewMode(wl); };
document.querySelectorAll('.tab').forEach(function(t){ t.onclick=function(){ loadTab(t.dataset.tab, false); }; });
document.getElementById('timedBtn').onclick=function(){ loadTab('full', true); };
function reviewMode(wl){
  const qs=DATA[curTab];
  const rq = wl.map(function(i){ return {q:qs[i], a:picks[i]}; });
  quiz.classList.remove('hidden'); done.classList.add('hidden');
  tabBadge.textContent=L('review'); stopTimer();
  let r=0, rcorrect=0;
  picks=new Array(qs.length).fill(-1); answered=new Array(qs.length).fill(false);
  function showR(){
    if(r>=rq.length){ const h='<div class="card result"><h2>'+L('reviewComplete')+'</h2><div class="score">'+rcorrect+' / '+rq.length+'</div><p class="verdict">'+(rcorrect===rq.length?L('allok'):L('again'))+'</p><button class="act" id="reviewDoneBtn">'+L('reviewDone')+'</button></div>'; quiz.innerHTML=h; document.getElementById('reviewDoneBtn').onclick=function(){ window.location.reload(); }; return; }
    const item=rq[r]; const q=item.q;
    document.getElementById('qProg').textContent=L('review')+' '+(r+1)+' / '+rq.length;
    document.getElementById('qCount').textContent='';
    document.getElementById('qHolder').innerHTML='<div class="q-text">'+(r+1)+'. '+Q(q)+'</div>';
    const opts=document.getElementById('opts'); opts.innerHTML='';
    OPTS(q).forEach(function(opt,i){
      const b=document.createElement('button'); b.className='opt'; b.textContent=opt;
      if(i===q.answer) b.classList.add('correct');
      if(i===item.a && i!==q.answer) b.classList.add('wrong');
      b.disabled=true; opts.appendChild(b);
    });
    const ex=document.createElement('div'); ex.className='explain'; ex.innerHTML='💡 '+EXPL(q); opts.appendChild(ex);
    document.getElementById('prevBtn').style.display='none';
    document.getElementById('nextBtn').textContent=L('next');
    document.getElementById('nextBtn').onclick=function(){ if(item.a===q.answer) rcorrect++; r++; showR(); };
  }
  showR();
}
function applyLang(l){
  lang=l;
  document.querySelectorAll('.langbtn').forEach(function(b){ b.classList.toggle('active', b.dataset.lang===l); });
  document.documentElement.lang = (l==="de"?"de":"en");
  document.getElementById('sub').textContent = I18N[l].sub;
  document.getElementById('src').textContent = I18N[l].src;
  document.getElementById('doneTitle').textContent = I18N[l].done;
  document.getElementById('prevBtn').textContent = I18N[l].back;
  document.getElementById('retryBtn').textContent = I18N[l].restart;
  document.getElementById('tabsBtn').textContent = I18N[l].alltests;
  document.querySelectorAll('.tab').forEach(function(t){ t.querySelector('.tn').textContent = (l==="de"?t.dataset.labelDe:t.dataset.labelEn); });
  if(!done.classList.contains('hidden')){ finish(); } else { loadTab(curTab, timed); }
}
document.querySelectorAll('.langbtn').forEach(function(b){ b.onclick=function(){ applyLang(b.dataset.lang); }; });
render();
"""

EXTRA = """
const themeBtn=document.getElementById('themeBtn');
function applyTheme(t){document.documentElement.setAttribute('data-theme',t); themeBtn.textContent = t==='dark' ? '☀️ Light' : '🌙 Dark'; try{localStorage.setItem('dmvTheme',t);}catch(e){} }
let savedTheme='light'; try{savedTheme=localStorage.getItem('dmvTheme')||'light';}catch(e){} applyTheme(savedTheme);
themeBtn.onclick=()=>applyTheme(document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark');
"""
GTRANS = """
function googleTranslateElementInit(){ new google.translate.TranslateElement({pageLanguage:'de', includedLanguages:'en,tr,ar,fr,es,zh,ru,vi,ko,ht', layout:google.translate.TranslateElement.InlineLayout.SIMPLE},'google_translate_element'); }
"""

def build_data(de):
    cats = de["categories"]
    by_id = {c["id"]: c["questions"] for c in cats}
    full = []
    for c in cats:
        full.extend(c["questions"])
    return {"full": full, "signs": by_id["signs"], "rules": by_id["rules"], "safety": by_id["safety"]}

def page_html(de):
    data = build_data(de)
    nfull = len(data["full"]); nsigns = len(data["signs"]); nrules = len(data["rules"]); nsafety = len(data["safety"])
    title = "Germany Fahrschule Theoriepruefung - Free Driving Theory Test (DE/EN) | DriveReady Hub"
    desc = ("Free Germany driving theory test (Fahrschule) practice with " + str(nsigns) + "+" + str(nrules) + "+" + str(nsafety) + " questions. "
            "Switch between German & English. Traffic signs, rules and road safety - 100% free.")
    canonical = "https://drivereadyhub.com/de/"
    ld = {"@context":"https://schema.org","@type":"QAPage","name":title,"url":canonical,
          "about":{"@type":"Thing","name":"Germany driving theory test (Fahrschule)"},
          "publisher":{"@type":"Organization","name":"DriveReady Hub","url":"https://drivereadyhub.com"}}

    js = JS.replace("__DATA_JSON__", json.dumps(data))
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="google-adsense-account" content="{PUB}">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/favicon.svg">
<meta property="og:type" content="website">
<meta property="og:site_name" content="DriveReady Hub">
<meta property="og:locale" content="de_DE">
<meta property="og:locale:alternate" content="en_US">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://drivereadyhub.com/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:url" content="{canonical}">
<meta name="twitter:image" content="https://drivereadyhub.com/og-image.png">
{ADSENSE}
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>
<style>{COMMON_CSS}</style>
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <div id="google_translate_element"></div>
    <button class="theme-btn" id="themeBtn">🌙 Dark</button>
  </div>

  <div class="breadcrumb"><a href="/">Home</a> &middot; <strong>Germany Fahrschule</strong></div>
  <header>
    <h1>🇩🇪 Germany <span class="em">Theoriepruefung</span></h1>
    <p class="sub" id="sub">Freie Fahrschule-Theoriepruefung zum Ueben - Verkehrszeichen, Regeln und Verkehrssicherheit. Auf Deutsch oder Englisch.</p>
  </header>

  <div class="langbar">
    <button class="langbtn active" data-lang="de">🇩🇪 Deutsch</button>
    <button class="langbtn" data-lang="en">🇬🇧 English</button>
  </div>

  <div class="exambar">
    <button class="act ghost" id="timedBtn">⏱ Simulierte Pruefung</button>
    <span class="timed" id="timeBox">⏱ 00:00</span>
  </div>

  <div class="tabs">
    <div class="tab active" data-tab="full" data-label-de="Vollstaendige Pruefung" data-label-en="Full Practice Exam"><span class="tn">Vollstaendige Pruefung</span><span class="tcount">{nfull} Fragen</span></div>
    <div class="tab" data-tab="signs" data-label-de="Verkehrszeichen" data-label-en="Traffic Signs"><span class="tn">Verkehrszeichen</span><span class="tcount">{nsigns} Fragen</span></div>
    <div class="tab" data-tab="rules" data-label-de="Verkehrsregeln" data-label-en="Driving Rules"><span class="tn">Verkehrsregeln</span><span class="tcount">{nrules} Fragen</span></div>
    <div class="tab" data-tab="safety" data-label-de="Verkehrssicherheit" data-label-en="Road Safety"><span class="tn">Verkehrssicherheit</span><span class="tcount">{nsafety} Fragen</span></div>
  </div>

  <div id="quiz">
    <div class="card">
      <div class="meta">
        <span class="badge" id="tabBadge">Vollstaendige Pruefung</span>
        <span id="qProg"></span>
      </div>
      <div id="qHolder"></div>
      <div id="opts"></div>
      <div class="nav">
        <button class="act ghost" id="prevBtn">← Zurueck</button>
        <button class="act" id="nextBtn">Weiter →</button>
      </div>
      <div class="pickgrid" id="pickGrid"></div>
    </div>
    <p class="foot" id="qCount"></p>
  </div>

  <div id="done" class="hidden">
    <div class="card result">
      <span class="badge" id="doneBadge"></span>
      <h2 style="margin-top:10px;" id="doneTitle">Pruefung beendet</h2>
      <div class="score" id="score"></div>
      <p class="verdict" id="verdict"></p>
      <button class="act" id="retryBtn">Test wiederholen</button>
      <button class="act ghost" id="reviewBtn" style="margin-left:8px;display:none;">🔁 Falsche wiederholen</button>
      <button class="act ghost" id="tabsBtn" style="margin-left:8px;">← Alle Tests</button>
    </div>
  </div>

  <p class="foot src" id="src">Fragen sind Theoriepruefungs-Material im Stil des TUEV/DEKRA (public domain). Nur zur Information, nicht mit TUEV, DEKRA oder einer Behoerde verbunden.</p>

  <div style="text-align:center;color:var(--muted);font-size:.76rem;margin-top:30px;padding-top:18px;border-top:1px solid var(--line);line-height:1.7;">
    <a href="/" style="color:var(--muted);text-decoration:none;">Home</a>
    <span style="margin:0 8px;">&middot;</span>
    <a href="/uk/" style="color:var(--muted);text-decoration:none;">UK</a>
    <span style="margin:0 8px;">&middot;</span>
    <a href="/ca/" style="color:var(--muted);text-decoration:none;">Canada</a>
    <span style="margin:0 8px;">&middot;</span>
    <a href="/au/" style="color:var(--muted);text-decoration:none;">Australia</a>
    <span style="margin:0 8px;">&middot;</span>
    <a href="/ie/" style="color:var(--muted);text-decoration:none;">Ireland</a>
    <br>
    DriveReady Hub - Informational only. Not affiliated with any DMV or government agency.
  </div>
</div>

<script>
{js}
</script>
<script>
{EXTRA}
</script>
<script>
{GTRANS}
</script>
<script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
</body>
</html>'''

if __name__ == "__main__":
    import importlib.util
    spec = importlib.util.spec_from_file_location("dedata", os.path.join(ROOT, "_de_data.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    with open(os.path.join(OUT, "index.html"), "w") as f:
        f.write(page_html(mod.DE))
    nfull = sum(len(c["questions"]) for c in mod.DE["categories"])
    print("wrote de/index.html | full=%d signs=%d rules=%d safety=%d" % (
        nfull, len(mod.DE["categories"][0]["questions"]),
        len(mod.DE["categories"][1]["questions"]), len(mod.DE["categories"][2]["questions"])))
