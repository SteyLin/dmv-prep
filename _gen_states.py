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
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "dmv")
os.makedirs(OUT, exist_ok=True)

with open("/tmp/states.json") as f:
    STATES = json.load(f)

import re
with open(os.path.join(ROOT, "index.html")) as f:
    idx = f.read()
m = re.search(r'ca-pub-\d+', idx)
PUB = "ca-pub-7503096549502749"
print("AdSense publisher:", PUB, "| states:", len(STATES))

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
"""

def state_full_name(s):
    return STATES[s]["name"].split(" (")[0]

def page_html(state_key):
    st = STATES[state_key]
    full = state_full_name(state_key)
    short = state_key.upper()
    name = st["name"]
    nq = len(st["questions"])
    title = f"{full} DMV Practice Test ({short}) — Free {short} Permit & License Prep | DriveReady Hub"
    desc = f"Free {full} ({short}) DMV practice test with {nq} questions from the official {full} driver handbook. Study, answer, and check explanations — 100% free."
    canonical = f"/dmv/{state_key}/"

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="google-adsense-account" content="{PUB}">
<link rel="canonical" href="{canonical}">
{ADSENSE}
<style>{COMMON_CSS}</style>
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <div id="google_translate_element"></div>
    <button class="theme-btn" id="themeBtn">🌙 Dark</button>
  </div>

  <div class="breadcrumb"><a href="/">Home</a> &middot; <a href="/#dmv">DMV Practice Tests</a> &middot; <strong>{full}</strong></div>
  <header>
    <h1>{full} <span class="em">DMV Practice</span></h1>
    <p class="sub">Free {short} permit and license practice test — {nq} questions from the official {full} driver handbook.</p>
  </header>

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
      <button class="act ghost" id="homeBtn" style="margin-left:8px;">← All States</button>
    </div>
  </div>

  <p class="foot src">Questions sourced from official {full} DMV publications (public domain). Informational only, not affiliated with any DMV or government agency.</p>

  <div style="text-align:center;color:var(--muted);font-size:.76rem;margin-top:30px;padding-top:18px;border-top:1px solid var(--line);line-height:1.7;">
    <a href="/" style="color:var(--muted);text-decoration:none;">Home</a>
    <span style="margin:0 8px;">·</span>
    <a href="/pages/faq.html" style="color:var(--muted);text-decoration:none;">FAQ</a>
    <br>
    DriveReady Hub — Informational only. Not affiliated with any DMV or government agency.
  </div>
</div>

<script>
const STATE_KEY = "{state_key}";
const STATE_DATA = {json.dumps(st)};
</script>
<script>
/* Quiz logic (identical to homepage, scoped to a single state) */
const QS = STATE_DATA.questions;
let idx=0, picks=new Array(QS.length).fill(-1), answered=new Array(QS.length).fill(false);
const quiz=document.getElementById('quiz');
const done=document.getElementById('done');
function render(){{
  const q=QS[idx];
  document.getElementById('qProg').textContent=`${{idx+1}} / ${{QS.length}}`;
  document.getElementById('qCount').textContent=`Question ${{idx+1}} of ${{QS.length}}`;
  let holder=document.getElementById('qHolder');
  holder.innerHTML=`<div class="q-text" id="q${{idx+1}}">${{idx+1}}. ${{q.q}}</div>`;
  const opts=document.getElementById('opts');
  opts.innerHTML='';
  q.options.forEach((opt,i)=>{{
    const b=document.createElement('button');
    b.className='opt'; b.textContent=opt;
    if(picks[idx]===i) b.classList.add('sel');
    if(answered[idx]){{
      if(i===q.answer) b.classList.add('correct');
      else if(i===picks[idx]) b.classList.add('wrong');
      b.disabled=true;
    }}
    b.onclick=()=>choose(i);
    opts.appendChild(b);
  }});
  if(answered[idx] && q.explanation){{
    const ex=document.createElement('div'); ex.className='explain'; ex.innerHTML='💡 '+q.explanation; opts.appendChild(ex);
  }}
  document.getElementById('prevBtn').disabled = idx===0;
  document.getElementById('nextBtn').textContent = (idx===QS.length-1)?'Finish ✓':'Next →';
}}
function choose(i){{ if(answered[idx]) return; picks[idx]=i; answered[idx]=true; render(); }}
document.getElementById('nextBtn').onclick=()=>{{
  if(!answered[idx]){{alert('Please select an answer.');return;}}
  if(idx<QS.length-1){{idx++;render();}} else finish();
}};
document.getElementById('prevBtn').onclick=()=>{{ if(idx>0){{idx--;render();}} }};
function finish(){{
  let correct=0; QS.forEach((q,i)=>{{ if(picks[i]===q.answer) correct++; }});
  const total=QS.length; const pct=Math.round(correct/total*100);
  quiz.classList.add('hidden'); done.classList.remove('hidden');
  document.getElementById('doneBadge').textContent=STATE_DATA.name;
  document.getElementById('score').textContent=`${{correct}} / ${{total}}`;
  document.getElementById('verdict').textContent = pct>=80 ? `${{pct}}% correct. You're in the passing range — nice work!` : `${{pct}}% correct. Keep studying the handbook and try again.`;
}}
document.getElementById('retryBtn').onclick=()=>{{ idx=0; picks=new Array(QS.length).fill(-1); answered=new Array(QS.length).fill(false); done.classList.add('hidden'); quiz.classList.remove('hidden'); render(); }};
document.getElementById('homeBtn').onclick=()=>{{ window.location.href='/'; }};

/* Deep-link to a question: /dmv/ny/#q5 */
function gotoHash(){{ const h=location.hash.match(/^#q(\d+)$/); if(h){{ const n=parseInt(h[1],10); if(n>=1 && n<=QS.length){{ idx=n-1; render(); document.getElementById('q'+n)?.scrollIntoView(); }} }} }}
window.addEventListener('hashchange', gotoHash);
render(); gotoHash();
</script>
<script>
/* Theme toggle */
const themeBtn=document.getElementById('themeBtn');
function applyTheme(t){{document.documentElement.setAttribute('data-theme',t); themeBtn.textContent = t==='dark' ? '☀️ Light' : '🌙 Dark'; try{{localStorage.setItem('dmvTheme',t);}}catch(e){{}} }}
let savedTheme='light'; try{{savedTheme=localStorage.getItem('dmvTheme')||'light';}}catch(e){{}} applyTheme(savedTheme);
themeBtn.onclick=()=>applyTheme(document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark');
</script>
<script>
function googleTranslateElementInit(){{ new google.translate.TranslateElement({{pageLanguage:'en', includedLanguages:'es,zh,ar,fr,tr,vi,ko,ru,ht', layout:google.translate.TranslateElement.InlineLayout.SIMPLE}},'google_translate_element'); }}
</script>
<script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
</body>
</html>'''

for k in STATES:
    d = os.path.join(OUT, k)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w") as f:
        f.write(page_html(k))
    print("wrote dmv/%s/index.html" % k)

print("DONE. Total states:", len(STATES))
