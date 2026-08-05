#!/usr/bin/env python3
"""
Generates per-state static DMV practice pages under dmv/ so each state has its
own indexable URL (e.g. /dmv/ny/) with shareable question anchors (/dmv/ny/#q5)
and AdSense AUTO-ADS (page-level) for maximum revenue with zero slot-ID hassle.

Uses AdSense Auto-ads: a single async client script in <head>. Google places
and optimizes all ad units (in-content, anchor, sidebar) automatically. No
manual data-ad-slot IDs required.

Does NOT touch any existing file. Only writes into dmv/.
"""
import collections
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "dmv")
os.makedirs(OUT, exist_ok=True)

with open("/tmp/states.json") as f:
    STATES = json.load(f)

OFFICIAL_PATH = os.path.join(ROOT, "state_official_sources.json")
if not os.path.exists(OFFICIAL_PATH):
    raise RuntimeError("Missing required verified source data: state_official_sources.json")
with open(OFFICIAL_PATH) as f:
    OFFICIAL = json.load(f)
if set(OFFICIAL) != set(STATES):
    missing = sorted(set(STATES) - set(OFFICIAL))
    extra = sorted(set(OFFICIAL) - set(STATES))
    raise RuntimeError(f"Official-source state mismatch; missing={missing}, extra={extra}")
with open(os.path.join(ROOT, "index.html")) as f:
    idx = f.read()
m = re.search(r'ca-pub-\d+', idx)
PUB = "ca-pub-7503096549502749"
print("AdSense publisher:", PUB, "| states:", len(STATES))

# Preserve the state-specific study guide already present in each tracked page.
# These blocks contain the unique state facts added for AdSense originality.
# Refuse to regenerate if even one block cannot be found; silently replacing
# them with a generic template would recreate the old duplicate-content issue.
GUIDE_BLOCKS = {}
for state_key in STATES:
    existing_path = os.path.join(OUT, state_key, "index.html")
    if os.path.exists(existing_path):
        with open(existing_path) as existing_file:
            existing_html = existing_file.read()
        guide_match = re.search(
            r'<!-- STATE_GUIDE_START -->\s*(.*?)\s*<!-- STATE_GUIDE_END -->',
            existing_html,
            re.S,
        )
        if not guide_match:
            guide_match = re.search(
                r'(  <div class="card" style="margin-top:24px;">.*?</div>)\s*'
                r'(?=<div style="text-align:center;color:var\(--muted\))',
                existing_html,
                re.S,
            )
        if guide_match:
            GUIDE_BLOCKS[state_key] = guide_match.group(1).strip()

if set(GUIDE_BLOCKS) != set(STATES):
    missing_guides = sorted(set(STATES) - set(GUIDE_BLOCKS))
    raise RuntimeError(f"Refusing to regenerate: missing preserved state guides for {missing_guides}")

# Auto-ads: single script in <head>. Google handles all placement/optimization.
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
  header{text-align:center;margin:18px 0 26px;}
  h1{font-size:2.2rem;font-weight:900;letter-spacing:-.03em;}
  h1 .em{color:var(--accent);}
  .sub{color:var(--muted);margin-top:10px;font-size:1.05rem;max-width:780px;margin-left:auto;margin-right:auto;}
  a{color:var(--accent);}
  .breadcrumb{color:var(--muted);font-size:.85rem;margin-bottom:12px;}
  .breadcrumb a{text-decoration:none;}
  /* quiz */
  .card{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:26px;box-shadow:0 8px 30px rgba(0,0,0,.08);margin-bottom:16px;}
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
  .exambar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:18px;}
  .exambar .timed{background:var(--card);border:1px solid var(--line);color:var(--accent);padding:9px 16px;border-radius:12px;font-weight:800;font-size:.95rem;display:none;}
  .exambar .act{padding:11px 18px;font-size:.92rem;}
  .official-panel{background:linear-gradient(135deg,var(--accent-soft),var(--card));border:1px solid var(--line);border-radius:18px;padding:22px;margin:0 0 20px;box-shadow:0 8px 24px rgba(0,0,0,.05);}
  .official-kicker{color:var(--accent);font-size:.74rem;font-weight:900;letter-spacing:.11em;text-transform:uppercase;margin-bottom:6px;}
  .official-panel h2,.study-map h2{font-size:1.25rem;line-height:1.3;margin-bottom:7px;}
  .official-panel p,.study-map p{color:var(--muted);font-size:.9rem;}
  .resource-links{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:15px;}
  .resource-link{display:flex;align-items:center;justify-content:space-between;gap:8px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 13px;text-decoration:none;font-size:.84rem;font-weight:800;line-height:1.25;}
  .resource-link:hover{border-color:var(--accent);transform:translateY(-1px);}
  .study-map{margin-top:24px;}
  .topic-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:16px 0 22px;}
  .topic-item{border:1px solid var(--line);border-radius:12px;padding:12px;background:var(--explain);}
  .topic-row{display:flex;justify-content:space-between;gap:12px;font-size:.82rem;font-weight:800;margin-bottom:7px;}
  .topic-track{height:7px;border-radius:999px;background:var(--line);overflow:hidden;}
  .topic-fill{height:100%;border-radius:999px;background:var(--accent);}
  .fact-list{display:grid;gap:10px;margin:12px 0 0;padding:0;list-style:none;}
  .fact-list li{border-left:3px solid var(--accent);background:var(--explain);border-radius:8px;padding:11px 13px;color:var(--muted);font-size:.88rem;line-height:1.55;}
  .fact-list a{font-weight:800;white-space:nowrap;}
  @media(max-width:720px){.resource-links,.topic-grid{grid-template-columns:1fr;}}
"""

def state_full_name(s):
    return STATES[s]["name"].split(" (")[0]

TOPIC_RULES = [
    ("Licensing & permit rules", re.compile(r"\b(license|licence|permit|learner|graduated|gdl|suspend|revoke|point|applicant|vision test|knowledge test)\b", re.I)),
    ("Signs, signals & markings", re.compile(r"\b(sign|signal|traffic light|flashing|pavement marking|yellow line|white line|railroad|crossing)\b", re.I)),
    ("Alcohol & impaired driving", re.compile(r"\b(alcohol|bac|dui|dwi|owi|intox|impaired|drug|implied consent)\b", re.I)),
    ("Vehicle & passenger safety", re.compile(r"\b(seat belt|safety belt|child restraint|car seat|tire|brake|headlight|vehicle|equipment|windshield)\b", re.I)),
    ("Hazards & emergency driving", re.compile(r"\b(skid|hydroplan|emergency|crash|collision|fog|snow|rain|night|deer|breakdown|following distance)\b", re.I)),
    ("Road rules & right-of-way", re.compile(r"\b(speed|right.of.way|yield|pass|passing|lane|turn|parking|intersection|roundabout|school bus|freeway|highway|curb)\b", re.I)),
]

def topic_counts(questions):
    counts = collections.Counter()
    for question in questions:
        searchable = " ".join((question.get("q", ""), question.get("ref", "")))
        label = next((name for name, pattern in TOPIC_RULES if pattern.search(searchable)), "General driver knowledge")
        counts[label] += 1
    return counts

def safe_url(value):
    value = (value or "").strip()
    if not value.startswith(("https://", "http://")):
        raise ValueError(f"Official source URL must be absolute HTTP(S): {value!r}")
    return html.escape(value, quote=True)

def enrichment_html(state_key, full, questions):
    source = OFFICIAL[state_key]
    agency_name = html.escape(source["agency_name"])
    resources = [
        ("Licensing agency", source["agency_url"]),
        ("Official driver handbook", source["handbook_url"]),
        ("Knowledge-test information", source["knowledge_test_url"]),
    ]
    resource_links = "".join(
        f'<a class="resource-link" href="{safe_url(url)}" target="_blank" rel="noopener noreferrer">'
        f'<span>{html.escape(label)}</span><span aria-hidden="true">↗</span></a>'
        for label, url in resources
    )
    official_panel = f'''<section class="official-panel" aria-labelledby="official-{state_key}">
    <div class="official-kicker">Verified official resources</div>
    <h2 id="official-{state_key}">Study with {agency_name} materials</h2>
    <p>This independent practice test is paired with direct {full} government resources. Check the official handbook and licensing page for the latest eligibility, testing, fee, and appointment requirements.</p>
    <div class="resource-links">{resource_links}</div>
  </section>'''

    counts = topic_counts(questions)
    total = len(questions)
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    topic_items = "".join(
        f'''<div class="topic-item"><div class="topic-row"><span>{html.escape(label)}</span><span>{count} questions</span></div>
        <div class="topic-track"><div class="topic-fill" style="width:{max(4, round(count / total * 100))}%"></div></div></div>'''
        for label, count in ordered
    )
    top_topics = ordered[:2]
    emphasis = " and ".join(f"{label.lower()} ({count})" for label, count in top_topics)
    facts = source.get("facts") or []
    if len(facts) < 3:
        raise ValueError(f"At least three verified official facts are required for {state_key}")
    fact_items = "".join(
        f'<li>{html.escape(item["fact"])} '
        f'<a href="{safe_url(item["source_url"])}" target="_blank" rel="noopener noreferrer">Official source ↗</a></li>'
        for item in facts
    )
    study_map = f'''<section class="card study-map" aria-labelledby="study-map-{state_key}">
    <div class="official-kicker">Your {full} study map</div>
    <h2 id="study-map-{state_key}">What this {total}-question practice bank covers</h2>
    <p>The current {full} bank places its strongest emphasis on {html.escape(emphasis)}. Use the breakdown below to identify the handbook sections that deserve the most review.</p>
    <div class="topic-grid">{topic_items}</div>
    <h2>Verified {full} licensing and road-rule facts</h2>
    <p>These {full}-specific notes link back to the agency or handbook page used to verify them. Official requirements can change, so follow the linked source when preparing an application or test appointment.</p>
    <ul class="fact-list">{fact_items}</ul>
  </section>'''
    return official_panel, study_map

def page_html(state_key):
    st = STATES[state_key]
    full = state_full_name(state_key)
    short = state_key.upper()
    name = st["name"]
    nq = len(st["questions"])
    title = f"{full} DMV Practice Test ({short}) — Free {short} Permit & License Prep | DriveReady Hub"
    desc = f"Free {full} ({short}) DMV practice test with {nq} questions based on {full} driver-handbook topics. Study, answer, and check explanations — 100% free."
    canonical = f"https://drivereadyhub.com/dmv/{state_key}/"
    guide_html = GUIDE_BLOCKS[state_key]
    official_panel, study_map = enrichment_html(state_key, full, st["questions"])
    source_data = OFFICIAL[state_key]
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": title,
          "url": canonical, "about": {"@type": "Thing", "name": "Driver's license permit practice test"},
          "citation": [source_data["handbook_url"], source_data["knowledge_test_url"]],
          "publisher": {"@type": "Organization", "name": "DriveReady Hub", "url": "https://drivereadyhub.com"}}
    ld_json = json.dumps(ld, ensure_ascii=False)

    JS = r"""
const STATE_KEY = "__STATE_KEY__";
const STATE_DATA = __STATE_JSON__;
const QS = STATE_DATA.questions;
let idx=0, picks=new Array(QS.length).fill(-1), answered=new Array(QS.length).fill(false);
let timed=false, timeLeft=0, timerId=null;
const quiz=document.getElementById('quiz');
const done=document.getElementById('done');
const timeBox=document.getElementById('timeBox');

function fmt(s){ const m=Math.floor(s/60), ss=s%60; return (m<10?'0':'')+m+':'+(ss<10?'0':'')+ss; }
function startTimer(){ clearInterval(timerId); timeLeft = QS.length*60; timeBox.textContent='⏱ '+fmt(timeLeft); timeBox.style.display='inline-block';
  timerId=setInterval(function(){ timeLeft--; timeBox.textContent='⏱ '+fmt(timeLeft); if(timeLeft<=0){ clearInterval(timerId); finish(); } },1000); }
function stopTimer(){ clearInterval(timerId); timeBox.style.display='none'; }

function render(){
  const q=QS[idx];
  document.getElementById('qProg').textContent=(idx+1)+' / '+QS.length;
  document.getElementById('qCount').textContent='Question '+(idx+1)+' of '+QS.length;
  let holder=document.getElementById('qHolder');
  holder.innerHTML='<div class="q-text" id="q'+(idx+1)+'">'+(idx+1)+'. '+q.q+'</div>';
  const opts=document.getElementById('opts'); opts.innerHTML='';
  q.options.forEach(function(opt,i){
    const b=document.createElement('button'); b.className='opt'; b.textContent=opt;
    if(picks[idx]===i) b.classList.add('sel');
    if(answered[idx]){
      if(i===q.answer) b.classList.add('correct');
      else if(i===picks[idx]) b.classList.add('wrong');
      b.disabled=true;
    }
    b.onclick=function(){ choose(i); };
    opts.appendChild(b);
  });
  if(answered[idx] && q.explanation){ const ex=document.createElement('div'); ex.className='explain'; ex.innerHTML='💡 '+q.explanation; opts.appendChild(ex); }
  document.getElementById('prevBtn').disabled = idx===0;
  document.getElementById('nextBtn').textContent = (idx===QS.length-1)?'Finish ✓':'Next →';
}

function choose(i){ if(answered[idx]) return; picks[idx]=i; answered[idx]=true; render(); }
document.getElementById('nextBtn').onclick=function(){
  if(!answered[idx]){ alert('Please select an answer.'); return; }
  if(idx<QS.length-1){ idx++; render(); } else finish();
};
document.getElementById('prevBtn').onclick=function(){ if(idx>0){ idx--; render(); } };

function wrongList(){ return QS.map(function(q,i){ return i; }).filter(function(i){ return picks[i]!==QS[i].answer; }); }

function finish(){
  stopTimer();
  let correct=0; QS.forEach(function(q,i){ if(picks[i]===q.answer) correct++; });
  const total=QS.length; const pct=Math.round(correct/total*100);
  quiz.classList.add('hidden'); done.classList.remove('hidden');
  document.getElementById('doneBadge').textContent=STATE_DATA.name+(timed?' (Timed)':'');
  document.getElementById('score').textContent=correct+' / '+total;
  document.getElementById('verdict').textContent = pct>=80 ? pct+'% correct. You\'re in the passing range - nice work!' : pct+'% correct. Keep studying the handbook and try again.';
  const wl=wrongList();
  const rb=document.getElementById('reviewBtn');
  rb.style.display = wl.length? 'inline-block':'none';
  rb.textContent = '🔁 Review Wrong Answers ('+wl.length+')';
}
document.getElementById('retryBtn').onclick=function(){ idx=0; picks=new Array(QS.length).fill(-1); answered=new Array(QS.length).fill(false); timed=false; done.classList.add('hidden'); quiz.classList.remove('hidden'); stopTimer(); render(); };
document.getElementById('homeBtn').onclick=function(){ window.location.href='/'; };
document.getElementById('reviewBtn').onclick=function(){ const wl=wrongList(); if(!wl.length) return; reviewMode(wl); };
document.getElementById('timedBtn').onclick=function(){ timed=true; idx=0; picks=new Array(QS.length).fill(-1); answered=new Array(QS.length).fill(false); done.classList.add('hidden'); quiz.classList.remove('hidden'); startTimer(); render(); };

function reviewMode(wl){
  const rq = wl.map(function(i){ return {q:QS[i], a:picks[i]}; });
  quiz.classList.remove('hidden'); done.classList.add('hidden');
  document.getElementById('stateBadge').textContent='Review Wrong Answers'; stopTimer();
  let r=0, rcorrect=0;
  function showR(){
    if(r>=rq.length){ const h='<div class="card result"><h2>Review Complete</h2><div class="score">'+rcorrect+' / '+rq.length+'</div><p class="verdict">'+(rcorrect===rq.length?'All corrected - great!':'Keep reviewing and try again.')+'</p><button class="act" id="reviewDoneBtn">← Back to Tests</button></div>'; quiz.innerHTML=h; document.getElementById('reviewDoneBtn').onclick=function(){ window.location.reload(); }; return; }
    const item=rq[r]; const q=item.q;
    document.getElementById('qProg').textContent='Review '+(r+1)+' / '+rq.length;
    document.getElementById('qCount').textContent='';
    document.getElementById('qHolder').innerHTML='<div class="q-text">'+(r+1)+'. '+q.q+'</div>';
    const opts=document.getElementById('opts'); opts.innerHTML='';
    q.options.forEach(function(opt,i){
      const b=document.createElement('button'); b.className='opt'; b.textContent=opt;
      if(i===q.answer) b.classList.add('correct');
      if(i===item.a && i!==q.answer) b.classList.add('wrong');
      b.disabled=true; opts.appendChild(b);
    });
    const ex=document.createElement('div'); ex.className='explain'; ex.innerHTML='💡 '+q.explanation; opts.appendChild(ex);
    document.getElementById('prevBtn').style.display='none';
    document.getElementById('nextBtn').textContent='Next →';
    document.getElementById('nextBtn').onclick=function(){ if(item.a===q.answer) rcorrect++; r++; showR(); };
  }
  showR();
}

render();
"""
    extra = """
/* Theme toggle */
const themeBtn=document.getElementById('themeBtn');
function applyTheme(t){document.documentElement.setAttribute('data-theme',t); themeBtn.textContent = t==='dark' ? '☀️ Light' : '🌙 Dark'; try{localStorage.setItem('dmvTheme',t);}catch(e){} }
let savedTheme='light'; try{savedTheme=localStorage.getItem('dmvTheme')||'light';}catch(e){} applyTheme(savedTheme);
themeBtn.onclick=()=>applyTheme(document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark');
"""
    js = JS.replace("__STATE_KEY__", state_key).replace("__STATE_JSON__", json.dumps(st))
    return f'''<!DOCTYPE html>
<html lang="en">
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
<meta property="og:locale" content="en_US">
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
<script type="application/ld+json">{ld_json}</script>
<style>{COMMON_CSS}</style>
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <button class="theme-btn" id="themeBtn">🌙 Dark</button>
  </div>

  <div class="breadcrumb"><a href="/">Home</a> &middot; <a href="/#dmv">DMV Practice Tests</a> &middot; <strong>{full}</strong></div>
  <header>
    <h1>{full} <span class="em">DMV Practice</span></h1>
    <p class="sub">Free {short} permit and license practice test — {nq} questions based on {full} driver-handbook topics.</p>
  </header>

  {official_panel}

  <div class="exambar">
    <button class="act ghost" id="timedBtn">⏱ Timed Mock Exam</button>
    <span class="timed" id="timeBox">⏱ 00:00</span>
  </div>

  <div id="quiz">
    <div class="card">
      <div class="meta">
        <span class="badge" id="stateBadge">{name}</span>
        <span id="qProg"></span>
      </div>
      <div id="qHolder"></div>
      <div id="opts"></div>
      <div class="nav">
        <button class="act ghost" id="prevBtn">← Back</button>
        <button class="act" id="nextBtn">Next →</button>
      </div>
    </div>
    <p class="foot" id="qCount"></p>
  </div>

  <div id="done" class="hidden">
    <div class="card result">
      <span class="badge" id="doneBadge"></span>
      <h2 style="margin-top:10px;">Exam Complete</h2>
      <div class="score" id="score"></div>
      <p class="verdict" id="verdict"></p>
      <button class="act" id="retryBtn">Restart This Test</button>
      <button class="act ghost" id="reviewBtn" style="margin-left:8px;display:none;">🔁 Review Wrong Answers</button>
      <button class="act ghost" id="homeBtn" style="margin-left:8px;">← All States</button>
    </div>
  </div>

  <p class="foot src">Questions are original practice material based on {full} driver-handbook topics (public domain). Informational only, not affiliated with any DMV or government agency.</p>

<!-- STATE_GUIDE_START -->
{guide_html}
<!-- STATE_GUIDE_END -->

{study_map}

  <div style="text-align:center;color:var(--muted);font-size:.76rem;margin-top:30px;padding-top:18px;border-top:1px solid var(--line);line-height:1.7;">
    <a href="/" style="color:var(--muted);text-decoration:none;">Home</a>
    <span style="margin:0 8px;">·</span>
    <a href="/pages/faq.html" style="color:var(--muted);text-decoration:none;">FAQ</a>
    <span style="margin:0 8px;">·</span>
    <a href="/pages/about.html" style="color:var(--muted);text-decoration:none;">About</a>
    <span style="margin:0 8px;">·</span>
    <a href="/pages/privacy-policy.html" style="color:var(--muted);text-decoration:none;">Privacy Policy</a>
    <span style="margin:0 8px;">·</span>
    <a href="/pages/contact.html" style="color:var(--muted);text-decoration:none;">Contact</a>
    <br>
    DriveReady Hub — Informational only. Not affiliated with any DMV or government agency.
  </div>
</div>

<script>
{js}
</script>
<script>
{extra}
</script>
</body>
</html>'''

rendered_pages = {state_key: page_html(state_key) for state_key in STATES}

for k, rendered_html in rendered_pages.items():
    d = os.path.join(OUT, k)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w") as f:
        f.write(rendered_html)
    print("wrote dmv/%s/index.html" % k)

print("DONE. Total states:", len(rendered_pages))
