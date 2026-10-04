#!/usr/bin/env python3
"""Builds the Full Spectrum bootcamp as one self-contained index.html."""
import json, pathlib

BASE = pathlib.Path.home() / "workspace" / "full-spectrum-bootcamp"
CONTENT = BASE / "content"

def blob(name):
    data = json.load(open(CONTENT / name, encoding="utf-8"))
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

SUBS = {
    "__TECHNICAL__": blob("technical.json"),
    "__SITUATIONAL__": blob("situational.json"),
    "__COGNITIVE__": blob("cognitive.json"),
    "__BEHAVIORAL__": blob("behavioral.json"),
    "__WORKSTYLE__": blob("workstyle.json"),
}

TPL = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<meta name="color-scheme" content="dark" />
<title>Full Spectrum — Job Assessment Prep Bootcamp</title>
<style>
:root{
  --bg:#0a0e14; --surface:#101722; --surface-2:#16202f; --ink:#e9f1f4; --muted:#93a4b8;
  --line:#223046; --line-strong:#33465f; --accent:#3ddc97; --accent-ink:#052e1e;
  --accent-soft:rgba(61,220,151,.10); --signal:#fbbf24; --danger:#f87171;
  --nav:#0c1219; --nav-ink:#eaf3f0; --code:#060b11; --code-ink:#b9f5d8;
  --shadow:0 16px 50px rgba(0,0,0,.45); --radius:14px;
  --font:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --mono:ui-monospace,"SF Mono","Cascadia Mono",Menlo,Consolas,"Liberation Mono",monospace;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font);line-height:1.55}
button,input{font:inherit} button{cursor:pointer}
a{color:var(--accent);text-underline-offset:3px}
.shell{max-width:1440px;margin:auto;min-height:100vh}
.topbar{position:sticky;top:0;z-index:20;background:rgba(12,18,25,.94);backdrop-filter:blur(12px);color:var(--nav-ink);display:flex;align-items:center;justify-content:space-between;gap:10px;padding:11px clamp(16px,4vw,44px);border-bottom:1px solid var(--line)}
.brand{font:700 13px var(--mono);letter-spacing:.08em;color:var(--accent);white-space:nowrap}
.nav{display:flex;gap:5px;flex-wrap:wrap;align-items:center}
.nav button{border:0;background:transparent;color:#a9bfce;padding:9px 13px;border-radius:8px;font-size:13px;font-weight:700}
.nav button.active,.nav button:hover{background:rgba(255,255,255,.09);color:#fff}
.nav a.navlink{color:#a9bfce;text-decoration:none;padding:9px 13px;border-radius:8px;font-size:13px;font-weight:700;border:1px dashed var(--line-strong)}
.nav a.navlink:hover{color:#fff;border-color:var(--accent)}
.session-pill{display:flex;align-items:center;gap:9px;font:600 11px var(--mono);color:#8fa3b8;white-space:nowrap}
.dot{width:8px;height:8px;background:var(--accent);border-radius:50%;box-shadow:0 0 0 4px rgba(61,220,151,.14)}
main{padding-bottom:60px}
.view{display:none} .view.active{display:block}
.hero{background:var(--nav);color:var(--nav-ink);padding:clamp(42px,7vw,92px) clamp(20px,6vw,86px) 38px;display:grid;grid-template-columns:minmax(0,1.2fr) minmax(290px,.8fr);gap:clamp(28px,6vw,72px);align-items:end;position:relative;overflow:hidden;border-bottom:1px solid var(--line)}
.hero:after{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(61,220,151,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(61,220,151,.06) 1px,transparent 1px);background-size:30px 30px;mask-image:linear-gradient(to left,#000,transparent 72%);-webkit-mask-image:linear-gradient(to left,#000,transparent 72%);pointer-events:none}
.hero-copy,.hero-panel{position:relative;z-index:1}
.kicker{font:600 12px var(--mono);color:var(--accent);letter-spacing:.06em;margin:0 0 18px}
.hero h1{font-size:clamp(40px,6.5vw,84px);line-height:.98;letter-spacing:-.05em;margin:0 0 24px;max-width:900px}
.hero h1 span{color:var(--accent)}
.lede{font-size:clamp(16px,2vw,21px);color:#b9c9d6;max-width:720px;margin:0 0 28px}
.cta-row{display:flex;gap:10px;flex-wrap:wrap}
.btn{border:1px solid var(--line-strong);background:var(--surface-2);color:var(--ink);padding:11px 16px;border-radius:9px;font-weight:800;display:inline-flex;align-items:center;gap:8px;text-decoration:none}
.btn.primary{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.btn.secondary{background:transparent;color:#eafff5;border-color:#3c5068}
.btn.small{padding:8px 11px;font-size:13px}
.btn.ghost{background:transparent}
.btn:disabled{opacity:.45;cursor:not-allowed}
.btn:focus-visible,.nav button:focus-visible,.choice:focus-visible,.evidence-btn:focus-visible,.q-toggle:focus-visible{outline:3px solid var(--signal);outline-offset:2px}
.hero-panel{border:1px solid var(--line-strong);background:rgba(255,255,255,.04);padding:20px;border-radius:16px}
.mission-label{display:flex;justify-content:space-between;gap:12px;font:500 12px var(--mono);color:#8fa3b8;border-bottom:1px solid var(--line);padding-bottom:12px}
.mission-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px 12px;padding-top:18px}
.metric strong{font-size:26px;display:block;line-height:1.1;color:#fff}
.metric span{font-size:12px;color:#8fa3b8}
.wrap{max-width:1280px;margin:auto;padding:clamp(24px,4vw,52px) clamp(16px,4vw,44px)}
.status-strip{background:var(--surface);border-bottom:1px solid var(--line);display:grid;grid-template-columns:1.2fr 1fr 1fr;gap:0}
.status-cell{padding:18px 24px;border-right:1px solid var(--line)}
.status-cell:last-child{border:0}
.status-label{font:600 11px var(--mono);color:var(--muted);margin-bottom:5px}
.status-value{font-size:19px;font-weight:800}
.bar{height:7px;background:var(--surface-2);border-radius:99px;margin-top:10px;overflow:hidden}
.bar i{display:block;height:100%;width:0;background:var(--accent);transition:width .35s ease}
.section-head{display:flex;align-items:end;justify-content:space-between;gap:22px;margin-bottom:22px}
.section-head h2{margin:0;font-size:clamp(28px,4vw,44px);letter-spacing:-.04em;line-height:1}
.section-head p{max-width:570px;margin:0;color:var(--muted)}
.eyebrow{font:600 11px var(--mono);color:var(--accent);letter-spacing:.06em;margin:0 0 8px}
.readiness-grid{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(280px,.7fr);gap:20px}
.panel{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow)}
.next-panel{padding:24px}
.next-panel h3{font-size:26px;line-height:1.15;margin:8px 0 10px}
.next-panel p{color:var(--muted);font-size:14px;margin:0 0 16px}
.lab-meta{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}
.tag{font:600 11px var(--mono);padding:5px 8px;border-radius:99px;background:var(--surface-2);color:var(--muted);border:1px solid var(--line)}
.tag.hot{background:rgba(251,191,36,.12);color:var(--ink);border-color:rgba(251,191,36,.5)}
.mastery{padding:22px}
.mastery h3{margin:0 0 14px;font-size:18px}
.skill-row{display:grid;grid-template-columns:118px 1fr 40px;gap:9px;align-items:center;margin:11px 0;font-size:12px}
.skill-row .bar{margin:0}
.skill-row b{text-align:right;font:600 11px var(--mono)}
.filter-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.filter{border:1px solid var(--line);background:var(--surface);color:var(--muted);border-radius:99px;padding:7px 11px;font-size:12px;font-weight:700}
.filter.active{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
.lab-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.lab-card{background:var(--surface);border:1px solid var(--line);border-radius:11px;padding:17px;display:flex;flex-direction:column;min-height:196px;text-align:left;color:var(--ink);appearance:none;width:100%}
.lab-card:hover{border-color:var(--accent)}
.lab-card h3{font-size:16px;line-height:1.25;margin:10px 0 7px}
.lab-card p{font-size:12px;color:var(--muted);margin:0 0 13px}
.lab-card .lab-footer{margin-top:auto;display:flex;justify-content:space-between;align-items:center;gap:8px}
.score-badge{font:600 11px var(--mono);color:var(--muted)}
.score-badge.done{color:var(--accent)}
.reset-row{margin-top:22px;display:flex;justify-content:flex-end}
.workbench-shell{display:grid;grid-template-columns:280px minmax(0,1fr);min-height:calc(100vh - 60px)}
.lab-rail{background:var(--nav);padding:22px 15px;border-right:1px solid var(--line)}
.lab-rail h2{font-size:16px;margin:0 8px 16px;color:var(--nav-ink)}
.rail-list{display:flex;flex-direction:column;gap:4px;max-height:calc(100vh - 140px);overflow-y:auto}
.rail-item{border:0;background:transparent;color:#9db4c6;text-align:left;padding:10px;border-radius:8px;font-size:12px;display:flex;gap:9px;align-items:flex-start;width:100%}
.rail-item:hover,.rail-item.active{background:rgba(255,255,255,.07);color:#fff}
.rail-item .st{font:700 11px var(--mono);flex:none;width:18px;text-align:center}
.rail-item .st.done{color:var(--accent)}
.rail-item b{display:block;color:inherit;font-size:12px;line-height:1.3}
.rail-item span{font:500 10px var(--mono);color:#7d93a8}
.workbench{padding:clamp(18px,4vw,42px);max-width:1050px;width:100%;margin:0 auto}
.wb-head{display:flex;justify-content:space-between;gap:18px;align-items:flex-start;margin-bottom:18px}
.wb-head h1{margin:3px 0 8px;font-size:clamp(27px,4vw,46px);line-height:1.02;letter-spacing:-.03em}
.wb-head p{margin:0;color:var(--muted);max-width:700px}
.timer{font:600 18px var(--mono);border:1px solid var(--line);background:var(--surface);padding:10px 12px;border-radius:8px;white-space:nowrap}
.timer.warn{color:var(--signal);border-color:var(--signal)}
.task-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(240px,.45fr);gap:14px}
.brief,.objective{padding:20px}
.brief h2,.objective h2,.evidence h2,.decision h2{font-size:14px;margin:0 0 12px;color:var(--ink)}
.brief p{margin:0 0 10px;color:var(--muted);font-size:14px}
.brief p:last-child{margin-bottom:0}
.objective ol{padding-left:20px;margin:0;font-size:13px;color:var(--muted)}
.objective li+li{margin-top:7px}
.evidence{margin-top:14px;padding:20px}
.command-row{display:flex;gap:7px;flex-wrap:wrap}
.evidence-btn{border:1px solid var(--line-strong);background:var(--surface-2);color:var(--ink);border-radius:7px;padding:8px 10px;font:600 11px var(--mono)}
.evidence-btn.ran{border-color:var(--accent);color:var(--accent);opacity:.55}
.terminal{background:var(--code);color:var(--code-ink);min-height:170px;border-radius:9px;padding:16px;margin-top:12px;font:400 12px/1.65 var(--mono);white-space:pre-wrap;overflow-wrap:anywhere;border:1px solid var(--line)}
.prompt{color:var(--accent)}
.terminal .dim{color:#5f7a8c}
.ev-block{margin-bottom:14px}
.ev-block:last-child{margin-bottom:0}
.decision{margin-top:14px;padding:20px}
.choices{display:grid;gap:8px}
.choice{border:1px solid var(--line-strong);background:var(--surface);color:var(--ink);padding:12px 14px;border-radius:8px;text-align:left;font-size:13px;width:100%}
.choice:hover,.choice.selected{border-color:var(--accent);background:var(--accent-soft)}
.choice.correct{border-color:var(--accent);background:var(--accent-soft)}
.choice.wrong{border-color:var(--danger);background:rgba(248,113,113,.08)}
.choice:disabled{cursor:default}
.feedback{display:none;margin-top:14px;padding:14px;border-radius:8px;background:var(--surface-2);font-size:13px;border:1px solid var(--line)}
.feedback.show{display:block}
.feedback.ok{border-color:var(--accent)}
.feedback.no{border-color:var(--danger)}
.feedback strong{display:block;margin-bottom:6px;font-size:14px}
.feedback.ok strong{color:var(--accent)}
.feedback.no strong{color:var(--danger)}
.action-row{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-top:14px;align-items:center}
.hint{font-size:12px;color:var(--muted);border:0;background:transparent;text-decoration:underline}
.hint-text{display:none;margin-top:10px;padding:10px 12px;border-left:3px solid var(--signal);background:rgba(251,191,36,.07);font-size:12px;color:var(--ink);border-radius:0 8px 8px 0}
.hint-text.show{display:block}
.why{border-top:1px solid var(--line);margin-top:12px;padding-top:12px;color:var(--muted)}
.sim-hero{padding:clamp(28px,5vw,64px);background:var(--nav);color:var(--nav-ink);display:grid;grid-template-columns:1fr 350px;gap:40px;align-items:center;border-bottom:1px solid var(--line)}
.sim-hero h1{font-size:clamp(38px,6vw,72px);line-height:.98;letter-spacing:-.045em;margin:0 0 18px}
.sim-hero h1 span{color:var(--accent)}
.sim-hero p{color:#b9c9d6;font-size:16px;max-width:680px}
.sim-box{padding:22px;border:1px solid var(--line-strong);border-radius:14px;background:rgba(255,255,255,.03)}
.sim-box strong{color:#fff}
.sim-box ul{padding-left:18px;color:#b9c9d6;font-size:13px;margin:10px 0 0}
.sim-box li+li{margin-top:6px}
.sim-plan{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.sim-stage{padding:20px}
.sim-stage .minutes{font:700 24px var(--mono);color:var(--accent)}
.sim-stage h3{margin:8px 0 6px;font-size:16px}
.sim-stage p{font-size:12px;color:var(--muted);margin:0}
.sim-active-head{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:16px}
.sim-progress{font:600 12px var(--mono);color:var(--muted)}
.verdict{padding:26px;text-align:center;margin-bottom:18px}
.verdict h2{margin:6px 0 8px;font-size:clamp(28px,4vw,44px);letter-spacing:-.04em}
.verdict p{color:var(--muted);max-width:640px;margin:0 auto}
.score-table{width:100%;border-collapse:collapse;font-size:13px;margin-top:6px}
.score-table th,.score-table td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line)}
.score-table th{font:600 11px var(--mono);color:var(--muted)}
.score-table td:last-child,.score-table th:last-child{text-align:right}
.guide-layout{display:grid;grid-template-columns:230px minmax(0,1fr);gap:28px}
.guide-nav{position:sticky;top:76px;align-self:start;display:flex;flex-direction:column;gap:4px}
.guide-nav button{border:0;background:transparent;text-align:left;color:var(--muted);padding:9px;border-radius:7px;font-size:13px;font-weight:600}
.guide-nav button.active,.guide-nav button:hover{background:var(--surface-2);color:var(--ink)}
.guide-content h1{font-size:clamp(32px,4.5vw,56px);letter-spacing:-.045em;margin:0 0 14px;line-height:1.02}
.guide-content h2{font-size:24px;border-bottom:1px solid var(--line);padding-bottom:10px;margin:34px 0 16px}
.guide-content p.lede2{color:var(--muted);max-width:720px}
.star-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:18px}
.star-card{padding:20px}
.star-card .letter{font:800 22px var(--mono);color:var(--accent)}
.star-card h3{margin:8px 0 8px;font-size:17px}
.star-card p{color:var(--muted);font-size:13px;margin:0}
.tips{margin-top:18px;padding:20px}
.tips h3{margin:0 0 10px;font-size:16px}
.tips ul{margin:0;padding-left:20px;color:var(--muted);font-size:13px}
.tips li+li{margin-top:7px}
.qbank{margin-top:8px;display:grid;gap:10px}
.q-item{border:1px solid var(--line);border-radius:11px;background:var(--surface);overflow:hidden}
.q-toggle{width:100%;border:0;background:transparent;color:var(--ink);text-align:left;padding:15px 17px;display:flex;justify-content:space-between;gap:12px;align-items:center;font-size:14px;font-weight:700}
.q-toggle .qcat{flex:none;font:600 10px var(--mono);color:var(--accent);border:1px solid var(--line-strong);border-radius:99px;padding:4px 9px}
.q-toggle .chev{color:var(--muted);flex:none}
.q-body{display:none;padding:0 17px 17px;font-size:13px}
.q-item.open .q-body{display:block}
.q-item.open .chev{transform:rotate(180deg);display:inline-block}
.q-body h4{font:700 11px var(--mono);color:var(--accent);letter-spacing:.05em;margin:16px 0 6px}
.q-body h4:first-child{margin-top:4px}
.q-body p{color:var(--muted);margin:0 0 6px}
.q-body ul{margin:0 0 6px;padding-left:20px;color:var(--muted)}
.q-body li+li{margin-top:5px}
.ws-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
.ws-card{padding:22px}
.ws-card h3{margin:0 0 10px;font-size:18px}
.ws-card p{color:var(--muted);font-size:13px;margin:0 0 8px}
.ws-card ul{margin:10px 0 0;padding-left:20px;color:var(--muted);font-size:13px}
.ws-card li+li{margin-top:6px}
.modal-wrap{position:fixed;inset:0;background:rgba(0,0,0,.66);z-index:50;display:none;place-items:center;padding:18px}
.modal-wrap.show{display:grid}
.modal{max-width:560px;width:100%;background:var(--surface);border:1px solid var(--line-strong);border-radius:15px;padding:24px;box-shadow:var(--shadow)}
.modal h2{font-size:26px;margin:0 0 10px;letter-spacing:-.03em}
.modal p{color:var(--muted);font-size:14px}
.modal .action-row{justify-content:flex-end}
.toast{position:fixed;right:18px;bottom:18px;z-index:60;background:var(--ink);color:var(--bg);padding:11px 14px;border-radius:8px;font-size:12px;font-weight:700;transform:translateY(90px);opacity:0;transition:.25s;max-width:min(90vw,420px)}
.toast.show{transform:none;opacity:1}
.empty-note{color:var(--muted);font-size:13px;padding:18px;border:1px dashed var(--line-strong);border-radius:10px;text-align:center}
@media(max-width:1080px){.lab-grid{grid-template-columns:repeat(2,1fr)}.sim-plan{grid-template-columns:repeat(2,1fr)}}
@media(max-width:980px){.workbench-shell{grid-template-columns:1fr}.lab-rail{padding:12px;border-right:0;border-bottom:1px solid var(--line)}.lab-rail h2{display:none}.rail-list{flex-direction:row;overflow-x:auto;max-height:none;scrollbar-width:none}.rail-item{min-width:200px}.sim-hero{grid-template-columns:1fr}.guide-layout{grid-template-columns:1fr}.guide-nav{position:static;flex-direction:row;overflow-x:auto}.guide-nav button{white-space:nowrap}.status-strip{grid-template-columns:repeat(2,1fr)}.status-cell:nth-child(2){border-right:0}.star-grid,.ws-grid{grid-template-columns:1fr}}
@media(max-width:720px){.topbar{align-items:flex-start;gap:8px;flex-wrap:wrap}.session-pill{display:none}.brand{width:100%}.nav{width:100%;display:grid;grid-template-columns:repeat(3,1fr)}.nav button,.nav a.navlink{padding:8px 4px;font-size:11px;text-align:center}.hero{grid-template-columns:1fr;padding-top:44px}.status-strip{grid-template-columns:1fr}.status-cell{border-right:0;border-bottom:1px solid var(--line)}.status-cell:last-child{border-bottom:0}.readiness-grid,.task-grid{grid-template-columns:1fr}.lab-grid{grid-template-columns:1fr}.section-head{display:block}.section-head p{margin-top:10px}.wb-head{display:block}.timer{display:inline-block;margin-top:12px}.sim-plan{grid-template-columns:1fr}.mission-grid{grid-template-columns:repeat(2,1fr)}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}
</style>
</head>
<body>
<div class="shell">
<header class="topbar">
  <div class="brand">◈ FULL SPECTRUM</div>
  <nav class="nav" aria-label="Primary">
    <button class="active" data-view="dashboard">Mission</button>
    <button data-view="workbench">Drill bench</button>
    <button data-view="simulation">3-hour run</button>
    <button data-view="behavioral">Behavioral</button>
    <button data-view="workstyle">Work style</button>
    <a class="navlink" href="./chat.html">AI Practice Companion →</a>
  </nav>
  <div class="session-pill"><span class="dot"></span><span>PROGRESS SAVED ON THIS DEVICE</span></div>
</header>
<main>
<section class="view active" id="view-dashboard">
  <div class="hero">
    <div class="hero-copy">
      <p class="kicker">ADAPTIVE DRILL • SCENARIO SIMULATION • INTERVIEW CRAFT</p>
      <h1>Full Spectrum.<br><span>Annihilate any assessment.</span></h1>
      <p class="lede">Sixty-four scored scenarios across fifteen technical, situational, and cognitive domains, twenty behavioral questions with model answers, six work-style guides, and a 180-minute full-spectrum simulation. The drill queue hunts your weakest domain first — readiness is earned, not assumed.</p>
      <div class="cta-row">
        <button class="btn primary" id="startAdaptive">Begin adaptive drill →</button>
        <button class="btn secondary" id="gotoSim">See the 180-minute plan</button>
      </div>
    </div>
    <aside class="hero-panel" aria-label="Mission profile">
      <div class="mission-label"><span>MISSION PROFILE</span><span id="readinessLabel">BASELINE</span></div>
      <div class="mission-grid">
        <div class="metric"><strong>64</strong><span>scored scenarios</span></div>
        <div class="metric"><strong>20</strong><span>behavioral questions</span></div>
        <div class="metric"><strong>6</strong><span>work-style guides</span></div>
        <div class="metric"><strong>180</strong><span>simulation minutes</span></div>
      </div>
    </aside>
  </div>
  <div class="status-strip">
    <div class="status-cell"><div class="status-label">OVERALL READINESS</div><div class="status-value" id="overallPct">0%</div><div class="bar"><i id="overallBar"></i></div></div>
    <div class="status-cell"><div class="status-label">SCENARIOS CLEARED</div><div class="status-value"><span id="clearedCount">0</span> / 64</div><div class="bar"><i id="clearedBar"></i></div></div>
    <div class="status-cell"><div class="status-label">NEXT PRIORITY</div><div class="status-value" id="nextPriority">—</div><div class="bar"><i id="nextBar"></i></div></div>
  </div>
  <div class="wrap">
    <div class="section-head"><div><p class="eyebrow">ADAPTIVE QUEUE</p><h2>Your next rep</h2></div><p>Every miss raises a domain's priority; every cleared scenario lowers it. The queue always serves your weakest domain's unmastered scenarios first. Progress persists on this device.</p></div>
    <div class="readiness-grid">
      <article class="panel next-panel" id="nextPanel"></article>
      <aside class="panel mastery"><h3>Mastery by domain</h3><div id="masteryRows"></div></aside>
    </div>
  </div>
  <div class="wrap" style="padding-top:6px">
    <div class="section-head"><div><p class="eyebrow">SCENARIO LIBRARY</p><h2>Train the whole spectrum</h2></div><p>Fifteen domains, three assessment families. Filter to a domain to drill it in isolation, or let the adaptive queue decide.</p></div>
    <div class="filter-row" id="filters"></div>
    <div class="lab-grid" id="labGrid"></div>
    <div class="reset-row"><button class="btn small ghost" id="resetProgress">Reset all progress</button></div>
  </div>
</section>

<section class="view" id="view-workbench">
  <div class="workbench-shell">
    <aside class="lab-rail"><h2>Drill queue</h2><div class="rail-list" id="railList"></div></aside>
    <div class="workbench">
      <div class="wb-head">
        <div><p class="eyebrow" id="wbEyebrow">DOMAIN</p><h1 id="wbTitle">Scenario</h1><p id="wbDesc"></p></div>
        <div class="timer" id="benchTimer">00:00</div>
      </div>
      <div class="task-grid">
        <section class="panel brief"><h2>Brief</h2><p id="wbSituation"></p></section>
        <section class="panel objective"><h2>Objectives</h2><ol id="wbObjectives"></ol></section>
      </div>
      <section class="panel evidence"><h2>Gather evidence</h2><div class="command-row" id="evidenceButtons"></div><div class="terminal" id="terminal"><span class="dim">Open each evidence source before deciding. Read first; act second.</span></div></section>
      <section class="panel decision"><h2 id="decisionPrompt">Decision</h2><div class="choices" id="choices"></div>
        <div class="hint-text" id="hintText"></div>
        <div class="feedback" id="feedback"></div>
        <div class="action-row">
          <button class="hint" id="hintBtn">Request a hint</button>
          <div style="display:flex;gap:8px">
            <button class="btn small ghost" id="skipItem">Skip →</button>
            <button class="btn small primary" id="submitChoice" disabled>Commit decision</button>
            <button class="btn small primary" id="nextItem" style="display:none">Next →</button>
          </div>
        </div>
      </section>
    </div>
  </div>
</section>

<section class="view" id="view-simulation">
  <div id="simLanding">
    <div class="sim-hero">
      <div><p class="kicker">FINAL EVOLUTION</p><h1>180 minutes.<br><span>Twelve incidents.</span></h1><p>Twelve scenarios auto-selected across all fifteen domains, weighted toward your weakest areas. The clock runs in real time, hints are disabled, and every evidence source you open costs two simulated minutes. One decision per incident — final.</p>
        <div class="cta-row"><button class="btn primary" id="openSim">Stage the simulation →</button></div>
      </div>
      <aside class="sim-box"><strong>Exam protocol</strong><ul><li>180:00 countdown, real time</li><li>12 incidents across all domains</li><li>Weakest domains get the most reps</li><li>No hints, one commit per incident</li><li>Each evidence source costs 2:00</li><li>Per-domain score breakdown at the end</li></ul></aside>
    </div>
    <div class="wrap">
      <div class="section-head"><div><p class="eyebrow">TIME BUDGET</p><h2>A deliberate three-hour shape</h2></div><p>A pacing plan for the full run — orient fast, spend the middle diagnosing, reserve the end for validation.</p></div>
      <div class="sim-plan">
        <article class="panel sim-stage"><span class="minutes">15m</span><h3>Orient</h3><p>Read every brief. Note impact, scope, and what changed. Do not touch anything yet.</p></article>
        <article class="panel sim-stage"><span class="minutes">45m</span><h3>Triage</h3><p>Stabilize the bleeding: restore service with the smallest reversible change.</p></article>
        <article class="panel sim-stage"><span class="minutes">45m</span><h3>Diagnose</h3><p>Work the evidence. Separate layers — link, name resolution, identity, policy, application.</p></article>
        <article class="panel sim-stage"><span class="minutes">45m</span><h3>Judge</h3><p>Situational and behavioral calls: prioritize, communicate, escalate correctly.</p></article>
        <article class="panel sim-stage"><span class="minutes">20m</span><h3>Validate</h3><p>Prove the fix works and nothing else broke. Check your weakest answers again.</p></article>
        <article class="panel sim-stage"><span class="minutes">10m</span><h3>Brief</h3><p>State cause, action, evidence, and residual risk for each incident.</p></article>
      </div>
    </div>
  </div>
  <div id="simActive" style="display:none">
    <div class="wrap">
      <div class="sim-active-head">
        <div><p class="eyebrow">FULL-SPECTRUM SIMULATION</p><div class="sim-progress" id="simProgress">INCIDENT 1 / 12</div></div>
        <div style="display:flex;gap:10px;align-items:center">
          <div class="timer" id="simTimer">180:00</div>
          <button class="btn small ghost" id="endSimEarly">End run</button>
        </div>
      </div>
      <div class="wb-head">
        <div><p class="eyebrow" id="simEyebrow">DOMAIN</p><h1 id="simTitle">Incident</h1><p id="simDesc"></p></div>
      </div>
      <div class="task-grid">
        <section class="panel brief"><h2>Brief</h2><p id="simSituation"></p></section>
        <section class="panel objective"><h2>Objectives</h2><ol id="simObjectives"></ol></section>
      </div>
      <section class="panel evidence"><h2>Gather evidence <span style="font-weight:400;color:var(--muted);font-size:12px">— each source costs 2:00</span></h2><div class="command-row" id="simEvidenceButtons"></div><div class="terminal" id="simTerminal"><span class="dim">Evidence costs time. Open what you need; skip what you don't.</span></div></section>
      <section class="panel decision"><h2 id="simPrompt">Decision</h2><div class="choices" id="simChoices"></div>
        <div class="feedback" id="simFeedback"></div>
        <div class="action-row"><span style="font-size:12px;color:var(--muted)">Hints disabled during the simulation.</span>
          <div style="display:flex;gap:8px">
            <button class="btn small primary" id="simSubmit" disabled>Commit decision</button>
            <button class="btn small primary" id="simNext" style="display:none">Next incident →</button>
          </div>
        </div>
      </section>
    </div>
  </div>
  <div id="simResults" style="display:none"><div class="wrap" id="simResultsBody"></div></div>
</section>

<section class="view" id="view-behavioral">
  <div class="wrap">
    <div class="guide-layout">
      <nav class="guide-nav" aria-label="Behavioral sections">
        <button class="active" data-bsec="b-star">The STAR method</button>
        <button data-bsec="b-delivery">Delivery</button>
        <button data-bsec="b-bank">Question bank (20)</button>
      </nav>
      <article class="guide-content" id="behavioralContent"></article>
    </div>
  </div>
</section>

<section class="view" id="view-workstyle">
  <div class="wrap">
    <div class="section-head"><div><p class="eyebrow">WORK-STYLE ASSESSMENTS</p><h2>How to answer honestly — and well</h2></div><p>Work-style and personality screens reward consistency and authenticity, not gaming. Six short guides.</p></div>
    <div class="ws-grid" id="wsGrid"></div>
  </div>
</section>
</main>
</div>

<div class="modal-wrap" id="simModal" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
  <div class="modal"><p class="eyebrow">FINAL EVOLUTION</p><h2 id="modalTitle">Start the 3-hour run?</h2><p>The clock starts at 180:00. Twelve incidents are staged across all fifteen domains, weighted toward your weakest areas. Hints are disabled, each decision is final, and every evidence source costs two minutes. Progress is saved on this device.</p><div class="action-row"><button class="btn ghost" id="cancelSim">Not yet</button><button class="btn primary" id="startSim">Start simulation</button></div></div>
</div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>
(function(){
'use strict';
var TECHNICAL = __TECHNICAL__;
var SITUATIONAL = __SITUATIONAL__;
var COGNITIVE = __COGNITIVE__;
var BEHAVIORAL = __BEHAVIORAL__;
var WORKSTYLE = __WORKSTYLE__;

var SCEN = TECHNICAL.concat(SITUATIONAL, COGNITIVE);
var BY_ID = {};
SCEN.forEach(function(s){ BY_ID[s.id] = s; });
var DOMAINS = [];
SCEN.forEach(function(s){ if (DOMAINS.indexOf(s.domain) < 0) DOMAINS.push(s.domain); });
var TOTAL = SCEN.length;
var LS_KEY = 'fsb-progress-v1';

function el(id){ return document.getElementById(id); }
function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function pad(n){ return (n < 10 ? '0' : '') + n; }
function fmtClock(sec){ sec = Math.max(0, sec); return Math.floor(sec/60) + ':' + pad(sec % 60); }
function shuffle(a){ var r = a.slice(); for (var i = r.length - 1; i > 0; i--){ var j = Math.floor(Math.random() * (i + 1)); var t = r[i]; r[i] = r[j]; r[j] = t; } return r; }

function loadProg(){ try { return JSON.parse(localStorage.getItem(LS_KEY)) || {}; } catch(e){ return {}; } }
var prog = loadProg();
function saveProg(){ try { localStorage.setItem(LS_KEY, JSON.stringify(prog)); } catch(e){} }
function recordResult(id, correct){ var r = prog[id] || {a:0, c:0}; r.a++; if (correct) r.c++; prog[id] = r; saveProg(); }
function cleared(id){ return !!(prog[id] && prog[id].c > 0); }
function attempted(id){ return !!prog[id]; }
function domainItems(d){ return SCEN.filter(function(s){ return s.domain === d; }); }
function domainCleared(d){ return domainItems(d).filter(function(s){ return cleared(s.id); }).length; }
function mastery(d){ var items = domainItems(d); return items.length ? domainCleared(d) / items.length : 0; }
function answeredCount(d){ return domainItems(d).filter(function(s){ return attempted(s.id); }).length; }
function weakestFirst(){
  return DOMAINS.slice().sort(function(a, b){
    var dm = mastery(a) - mastery(b);
    if (dm !== 0) return dm;
    var da = answeredCount(a) - answeredCount(b);
    if (da !== 0) return da;
    return a < b ? -1 : 1;
  });
}
function overallPct(){ return Math.round(100 * SCEN.filter(function(s){ return cleared(s.id); }).length / TOTAL); }
function clearedCount(){ return SCEN.filter(function(s){ return cleared(s.id); }).length; }
function buildQueue(onlyDomain){
  var order = weakestFirst().filter(function(d){ return !onlyDomain || d === onlyDomain; });
  var q = [];
  order.forEach(function(d){
    var items = domainItems(d);
    var unm = shuffle(items.filter(function(s){ return !cleared(s.id); }));
    var mst = shuffle(items.filter(function(s){ return cleared(s.id); }));
    unm.concat(mst).forEach(function(s){ q.push(s.id); });
  });
  return q;
}

var toastTimer = null;
function toast(msg){
  var t = el('toast'); t.textContent = msg; t.classList.add('show');
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(function(){ t.classList.remove('show'); }, 2600);
}

var VIEWS = ['dashboard','workbench','simulation','behavioral','workstyle'];
function showView(v){
  VIEWS.forEach(function(x){ el('view-' + x).classList.toggle('active', x === v); });
  var btns = document.querySelectorAll('.nav button[data-view]');
  for (var i = 0; i < btns.length; i++) btns[i].classList.toggle('active', btns[i].getAttribute('data-view') === v);
  if (v === 'dashboard') renderDashboard();
  window.scrollTo(0, 0);
}
var navBtns = document.querySelectorAll('.nav button[data-view]');
for (var ni = 0; ni < navBtns.length; ni++){
  (function(b){ b.addEventListener('click', function(){ showView(b.getAttribute('data-view')); }); })(navBtns[ni]);
}

/* ---------------- Dashboard ---------------- */
var activeFilter = null;
function statusFor(id){ return cleared(id) ? 'done' : (attempted(id) ? 'seen' : 'new'); }

function renderDashboard(){
  var pct = overallPct(), cc = clearedCount();
  el('overallPct').textContent = pct + '%';
  el('overallBar').style.width = pct + '%';
  el('clearedCount').textContent = cc;
  el('clearedBar').style.width = Math.round(100 * cc / TOTAL) + '%';
  el('readinessLabel').textContent = pct >= 85 ? 'ASSESSMENT-READY' : (pct >= 60 ? 'DEVELOPING' : (pct > 0 ? 'WARMING UP' : 'BASELINE'));

  var weak = weakestFirst()[0];
  var wm = Math.round(100 * mastery(weak));
  el('nextPriority').textContent = weak + ' · ' + wm + '%';
  el('nextBar').style.width = wm + '%';

  var rows = weakestFirst().map(function(d){
    var m = Math.round(100 * mastery(d));
    return '<div class="skill-row"><span>' + esc(d) + '</span><div class="bar"><i style="width:' + m + '%"></i></div><b>' + m + '%</b></div>';
  });
  el('masteryRows').innerHTML = rows.join('');

  var q = buildQueue();
  var nextId = q.length ? q[0] : null;
  var np = el('nextPanel');
  if (nextId){
    var s = BY_ID[nextId];
    np.innerHTML = '<p class="eyebrow">YOUR NEXT REP</p><h3>' + esc(s.title) + '</h3>' +
      '<div class="lab-meta"><span class="tag hot">' + esc(s.domain) + ' · weakest</span><span class="tag">~' + s.mins + ' min</span><span class="tag">' + statusFor(s.id).toUpperCase() + '</span></div>' +
      '<p>' + esc(s.desc) + '</p>' +
      '<button class="btn primary" id="nextRepBtn">Start this scenario →</button>';
    el('nextRepBtn').addEventListener('click', function(){ startDrill(null, s.id); });
  } else {
    np.innerHTML = '<p class="eyebrow">YOUR NEXT REP</p><h3>Queue complete.</h3><p>Every scenario is cleared. Run the 180-minute simulation to prove it under pressure.</p><button class="btn primary" id="nextRepBtn">Stage the simulation →</button>';
    el('nextRepBtn').addEventListener('click', function(){ showView('simulation'); });
  }

  var chips = ['<button class="filter' + (activeFilter ? '' : ' active') + '" data-f="">All domains</button>'].concat(
    DOMAINS.map(function(d){
      return '<button class="filter' + (activeFilter === d ? ' active' : '') + '" data-f="' + esc(d) + '">' + esc(d) + '</button>';
    })
  );
  el('filters').innerHTML = chips.join('');
  var fbtns = el('filters').querySelectorAll('.filter');
  for (var i = 0; i < fbtns.length; i++){
    (function(b){ b.addEventListener('click', function(){
      activeFilter = b.getAttribute('data-f') || null; renderDashboard();
    }); })(fbtns[i]);
  }

  var list = SCEN.filter(function(s){ return !activeFilter || s.domain === activeFilter; });
  if (!list.length){
    el('labGrid').innerHTML = '<div class="empty-note">No scenarios in this filter.</div>';
    return;
  }
  el('labGrid').innerHTML = list.map(function(s){
    var st = statusFor(s.id);
    var badge = st === 'done' ? '<span class="score-badge done">✓ CLEARED</span>' : (st === 'seen' ? '<span class="score-badge">ATTEMPTED</span>' : '<span class="score-badge">NEW</span>');
    return '<button class="lab-card" data-id="' + esc(s.id) + '"><span class="tag">' + esc(s.domain) + '</span><h3>' + esc(s.title) + '</h3><p>' + esc(s.desc) + '</p>' +
      '<div class="lab-footer"><span class="score-badge">~' + s.mins + ' MIN</span>' + badge + '</div></button>';
  }).join('');
  var cards = el('labGrid').querySelectorAll('.lab-card');
  for (var k = 0; k < cards.length; k++){
    (function(c){ c.addEventListener('click', function(){ startDrill(activeFilter, c.getAttribute('data-id')); }); })(cards[k]);
  }
}

el('startAdaptive').addEventListener('click', function(){ startDrill(null, null); });
el('gotoSim').addEventListener('click', function(){ showView('simulation'); });

var resetArmed = false, resetTimer = null;
el('resetProgress').addEventListener('click', function(){
  var btn = el('resetProgress');
  if (!resetArmed){
    resetArmed = true; btn.textContent = 'Click again to confirm reset';
    resetTimer = setTimeout(function(){ resetArmed = false; btn.textContent = 'Reset all progress'; }, 4000);
    return;
  }
  clearTimeout(resetTimer); resetArmed = false; btn.textContent = 'Reset all progress';
  try { localStorage.removeItem(LS_KEY); } catch(e){}
  prog = {};
  renderDashboard(); toast('Progress cleared. Fresh start.');
});

/* ---------------- Workbench (adaptive drill) ---------------- */
var bench = { queue: [], idx: 0, selected: -1, submitted: false, t0: 0, timerId: null };

function startDrill(domain, startId){
  bench.queue = buildQueue(domain);
  if (!bench.queue.length){ toast('No scenarios available.'); return; }
  bench.idx = startId ? Math.max(0, bench.queue.indexOf(startId)) : 0;
  showView('workbench');
  renderBench();
}

function renderRail(){
  var html = bench.queue.map(function(id, i){
    var s = BY_ID[id];
    var st = cleared(id) ? '<span class="st done">✓</span>' : (attempted(id) ? '<span class="st">•</span>' : '<span class="st">○</span>');
    return '<button class="rail-item' + (i === bench.idx ? ' active' : '') + '" data-i="' + i + '">' + st +
      '<span style="flex:1"><b>' + esc(s.title) + '</b><span>' + esc(s.domain) + ' · ~' + s.mins + 'm</span></span></button>';
  }).join('');
  el('railList').innerHTML = html;
  var items = el('railList').querySelectorAll('.rail-item');
  for (var i = 0; i < items.length; i++){
    (function(b){ b.addEventListener('click', function(){ bench.idx = parseInt(b.getAttribute('data-i'), 10); renderBench(); }); })(items[i]);
  }
}

function renderBench(){
  var item = BY_ID[bench.queue[bench.idx]];
  if (!item) return;
  bench.selected = -1; bench.submitted = false;
  if (bench.timerId) clearInterval(bench.timerId);

  el('wbEyebrow').textContent = item.domain.toUpperCase() + ' · ~' + item.mins + ' MIN · ' + (bench.idx + 1) + ' / ' + bench.queue.length;
  el('wbTitle').textContent = item.title;
  el('wbDesc').textContent = item.desc;
  el('wbSituation').textContent = item.situation;
  el('wbObjectives').innerHTML = item.objectives.map(function(o){ return '<li>' + esc(o) + '</li>'; }).join('');
  el('decisionPrompt').textContent = item.prompt || 'Choose the best next action';

  el('evidenceButtons').innerHTML = item.evidence.map(function(p, i){
    return '<button class="evidence-btn" data-i="' + i + '">' + esc(p[0]) + '</button>';
  }).join('');
  el('terminal').innerHTML = '<span class="dim">Open each evidence source before deciding. Read first; act second.</span>';
  var ebtns = el('evidenceButtons').querySelectorAll('.evidence-btn');
  for (var e = 0; e < ebtns.length; e++){
    (function(b){ b.addEventListener('click', function(){
      var p = item.evidence[parseInt(b.getAttribute('data-i'), 10)];
      b.classList.add('ran'); b.disabled = true;
      var term = el('terminal');
      if (term.querySelector('.dim')) term.innerHTML = '';
      term.innerHTML += '<div class="ev-block"><span class="prompt">$ ' + esc(p[0]) + '</span>\n' + esc(p[1]) + '</div>';
    }); })(ebtns[e]);
  }

  el('choices').innerHTML = item.choices.map(function(c, i){
    return '<button class="choice" data-i="' + i + '">' + esc(c) + '</button>';
  }).join('');
  var cbtns = el('choices').querySelectorAll('.choice');
  for (var c = 0; c < cbtns.length; c++){
    (function(b){ b.addEventListener('click', function(){
      if (bench.submitted) return;
      bench.selected = parseInt(b.getAttribute('data-i'), 10);
      for (var j = 0; j < cbtns.length; j++) cbtns[j].classList.remove('selected');
      b.classList.add('selected');
      el('submitChoice').disabled = false;
    }); })(cbtns[c]);
  }

  el('hintText').classList.remove('show'); el('hintText').textContent = '';
  var hintBtn = el('hintBtn'); hintBtn.style.display = '';
  hintBtn.onclick = function(){
    el('hintText').textContent = item.hint;
    el('hintText').classList.add('show');
    hintBtn.style.display = 'none';
  };

  var fb = el('feedback'); fb.className = 'feedback'; fb.innerHTML = '';
  var sub = el('submitChoice'); sub.disabled = true; sub.style.display = '';
  el('nextItem').style.display = 'none';
  el('skipItem').style.display = '';
  renderRail();

  bench.t0 = Date.now();
  el('benchTimer').textContent = '00:00';
  bench.timerId = setInterval(function(){ el('benchTimer').textContent = fmtClock(Math.floor((Date.now() - bench.t0) / 1000)); }, 1000);
}

el('submitChoice').addEventListener('click', function(){
  var item = BY_ID[bench.queue[bench.idx]];
  if (bench.submitted || bench.selected < 0) return;
  bench.submitted = true;
  var ok = bench.selected === item.answer;
  recordResult(item.id, ok);

  var cbtns = el('choices').querySelectorAll('.choice');
  for (var j = 0; j < cbtns.length; j++){
    cbtns[j].disabled = true;
    var ji = parseInt(cbtns[j].getAttribute('data-i'), 10);
    if (ji === item.answer) cbtns[j].classList.add('correct');
    else if (ji === bench.selected) cbtns[j].classList.add('wrong');
  }
  var fb = el('feedback');
  fb.className = 'feedback show ' + (ok ? 'ok' : 'no');
  fb.innerHTML = '<strong>' + (ok ? 'Correct.' : 'Not quite — the best answer is highlighted above.') + '</strong>' +
    '<div>' + esc(item.why) + '</div>';
  el('submitChoice').style.display = 'none';
  el('skipItem').style.display = 'none';
  el('hintBtn').style.display = 'none';
  el('nextItem').style.display = '';
  renderRail();
});

el('nextItem').addEventListener('click', function(){
  bench.idx++;
  if (bench.idx >= bench.queue.length){
    toast('Queue complete — rebuilding around your weakest domains.');
    var weak = weakestFirst()[0];
    bench.queue = buildQueue();
    bench.idx = 0;
  }
  renderBench();
});
el('skipItem').addEventListener('click', function(){
  bench.idx = (bench.idx + 1) % bench.queue.length;
  renderBench();
});
/* ---------------- Simulation ---------------- */
var sim = null;

function pickSimItems(){
  var order = weakestFirst().slice(0, 12);
  return order.map(function(d){
    var items = domainItems(d);
    var unm = items.filter(function(s){ return !cleared(s.id); });
    var pool = unm.length ? unm : items;
    return pool[Math.floor(Math.random() * pool.length)].id;
  });
}

function verdict(p){
  if (p >= 85) return ['ASSESSMENT-READY', 'You are operating at a hireable level across the full spectrum. Keep the weakest domains warm with short drills.'];
  if (p >= 70) return ['NEARLY READY', 'Strong foundation with a few soft spots. Drill the domains below 70% until they clear, then run the simulation again.'];
  if (p >= 50) return ['DEVELOPING', 'The instincts are forming but the gaps are real. Work the adaptive drill queue daily, weakest domain first.'];
  return ['FOUNDATIONS FIRST', 'Too many misses across too many domains. Slow down: drill one domain at a time in the library before re-running the simulation.'];
}

el('openSim').addEventListener('click', function(){ el('simModal').classList.add('show'); });
el('cancelSim').addEventListener('click', function(){ el('simModal').classList.remove('show'); });
el('simModal').addEventListener('click', function(e){ if (e.target === el('simModal')) el('simModal').classList.remove('show'); });

el('startSim').addEventListener('click', function(){
  el('simModal').classList.remove('show');
  sim = { items: pickSimItems(), idx: 0, answers: {}, remaining: 180 * 60, timerId: null, selected: -1, submitted: false };
  el('simLanding').style.display = 'none';
  el('simResults').style.display = 'none';
  el('simActive').style.display = '';
  showView('simulation');
  renderSimItem();
  sim.timerId = setInterval(function(){
    sim.remaining--;
    if (sim.remaining <= 0){ endSim(true); return; }
    var t = el('simTimer');
    t.textContent = fmtClock(sim.remaining);
    t.classList.toggle('warn', sim.remaining < 600);
  }, 1000);
});

function renderSimItem(){
  var item = BY_ID[sim.items[sim.idx]];
  if (!item) return;
  sim.selected = -1; sim.submitted = false;
  el('simProgress').textContent = 'INCIDENT ' + (sim.idx + 1) + ' / ' + sim.items.length;
  el('simEyebrow').textContent = item.domain.toUpperCase() + ' · ~' + item.mins + ' MIN';
  el('simTitle').textContent = item.title;
  el('simDesc').textContent = item.desc;
  el('simSituation').textContent = item.situation;
  el('simObjectives').innerHTML = item.objectives.map(function(o){ return '<li>' + esc(o) + '</li>'; }).join('');
  el('simPrompt').textContent = item.prompt || 'Choose the best next action';

  el('simEvidenceButtons').innerHTML = item.evidence.map(function(p, i){
    return '<button class="evidence-btn" data-i="' + i + '">' + esc(p[0]) + '</button>';
  }).join('');
  el('simTerminal').innerHTML = '<span class="dim">Evidence costs time. Open what you need; skip what you don\'t.</span>';
  var ebtns = el('simEvidenceButtons').querySelectorAll('.evidence-btn');
  for (var e = 0; e < ebtns.length; e++){
    (function(b){ b.addEventListener('click', function(){
      if (sim.submitted) return;
      var p = item.evidence[parseInt(b.getAttribute('data-i'), 10)];
      b.classList.add('ran'); b.disabled = true;
      var term = el('simTerminal');
      if (term.querySelector('.dim')) term.innerHTML = '';
      term.innerHTML += '<div class="ev-block"><span class="prompt">$ ' + esc(p[0]) + '</span>\n' + esc(p[1]) + '</div>';
      sim.remaining = Math.max(1, sim.remaining - 120);
      el('simTimer').textContent = fmtClock(sim.remaining);
      toast('Evidence opened — 2:00 deducted.');
    }); })(ebtns[e]);
  }

  el('simChoices').innerHTML = item.choices.map(function(c, i){
    return '<button class="choice" data-i="' + i + '">' + esc(c) + '</button>';
  }).join('');
  var cbtns = el('simChoices').querySelectorAll('.choice');
  for (var c = 0; c < cbtns.length; c++){
    (function(b){ b.addEventListener('click', function(){
      if (sim.submitted) return;
      sim.selected = parseInt(b.getAttribute('data-i'), 10);
      for (var j = 0; j < cbtns.length; j++) cbtns[j].classList.remove('selected');
      b.classList.add('selected');
      el('simSubmit').disabled = false;
    }); })(cbtns[c]);
  }
  var fb = el('simFeedback'); fb.className = 'feedback'; fb.innerHTML = '';
  el('simSubmit').disabled = true; el('simSubmit').style.display = '';
  el('simNext').style.display = 'none';
}

el('simSubmit').addEventListener('click', function(){
  var item = BY_ID[sim.items[sim.idx]];
  if (sim.submitted || sim.selected < 0) return;
  sim.submitted = true;
  var ok = sim.selected === item.answer;
  sim.answers[item.id] = ok;
  recordResult(item.id, ok);

  var cbtns = el('simChoices').querySelectorAll('.choice');
  for (var j = 0; j < cbtns.length; j++){
    cbtns[j].disabled = true;
    var ji = parseInt(cbtns[j].getAttribute('data-i'), 10);
    if (ji === item.answer) cbtns[j].classList.add('correct');
    else if (ji === sim.selected) cbtns[j].classList.add('wrong');
  }
  var fb = el('simFeedback');
  fb.className = 'feedback show ' + (ok ? 'ok' : 'no');
  fb.innerHTML = '<strong>' + (ok ? 'Correct.' : 'Missed — best answer highlighted.') + '</strong><div>' + esc(item.why) + '</div>';
  el('simSubmit').style.display = 'none';
  el('simNext').style.display = '';
  el('simNext').textContent = (sim.idx + 1 >= sim.items.length) ? 'See results →' : 'Next incident →';
});

el('simNext').addEventListener('click', function(){
  sim.idx++;
  if (sim.idx >= sim.items.length){ endSim(false); return; }
  renderSimItem();
  window.scrollTo(0, 0);
});

el('endSimEarly').addEventListener('click', function(){ endSim(false); });

function endSim(timedOut){
  if (!sim) return;
  if (sim.timerId) clearInterval(sim.timerId);
  var answered = Object.keys(sim.answers);
  var perDomain = {};
  DOMAINS.forEach(function(d){ perDomain[d] = {c: 0, t: 0}; });
  answered.forEach(function(id){
    var s = BY_ID[id];
    perDomain[s.domain].t++;
    if (sim.answers[id]) perDomain[s.domain].c++;
  });
  var totalC = answered.reduce(function(a, id){ return a + (sim.answers[id] ? 1 : 0); }, 0);
  var pct = answered.length ? Math.round(100 * totalC / answered.length) : 0;
  var v = verdict(pct);

  var rows = DOMAINS.filter(function(d){ return perDomain[d].t > 0; })
    .sort(function(a, b){ return (perDomain[a].c / perDomain[a].t) - (perDomain[b].c / perDomain[b].t); })
    .map(function(d){
      var r = perDomain[d];
      var m = Math.round(100 * r.c / r.t);
      return '<tr><td>' + esc(d) + '</td><td>' + r.c + ' / ' + r.t + '</td><td><div class="bar" style="margin:0;min-width:80px"><i style="width:' + m + '%"></i></div></td><td>' + m + '%</td></tr>';
    }).join('');

  el('simActive').style.display = 'none';
  el('simResults').style.display = '';
  el('simResultsBody').innerHTML =
    '<article class="panel verdict"><p class="eyebrow">SIMULATION COMPLETE' + (timedOut ? ' · TIME EXPIRED' : '') + '</p>' +
    '<h2>' + v[0] + '</h2><p>' + v[1] + '</p>' +
    '<p style="font-size:34px;font-weight:800;color:#fff;margin-top:14px">' + totalC + ' / ' + answered.length + ' <span style="font-size:16px;color:var(--muted)">(' + pct + '%)</span></p></article>' +
    '<article class="panel" style="padding:22px"><h3 style="margin:0 0 12px">Score by domain</h3>' +
    '<table class="score-table"><thead><tr><th>Domain</th><th>Score</th><th></th><th style="text-align:right">Pct</th></tr></thead><tbody>' + rows + '</tbody></table></article>' +
    '<div class="cta-row" style="margin-top:18px"><button class="btn primary" id="simDrillWeak">Drill weakest domains →</button><button class="btn secondary" id="simBackMission">Back to mission</button></div>';
  el('simDrillWeak').addEventListener('click', function(){ startDrill(null, null); });
  el('simBackMission').addEventListener('click', function(){
    el('simResults').style.display = 'none';
    el('simLanding').style.display = '';
    showView('dashboard');
  });
  showView('simulation');
  window.scrollTo(0, 0);
  sim = null;
}

/* ---------------- Behavioral guide ---------------- */
function renderBehavioral(){
  var sm = BEHAVIORAL.guide.star_method;
  var order = [['S','Situation', sm.situation], ['T','Task', sm.task], ['A','Action', sm.action], ['R','Result', sm.result]];
  var html = '<section id="b-star"><p class="eyebrow">BEHAVIORAL INTERVIEWS</p><h1>Answer with STAR.</h1>' +
    '<p class="lede2">Behavioral questions are scored on structure, not storytelling flair. The STAR method gives every answer a beginning, a middle, and proof.</p>' +
    '<div class="star-grid">' + order.map(function(x){
      return '<article class="panel star-card"><span class="letter">' + x[0] + '</span><h3>' + x[1] + '</h3><p>' + esc(x[2]) + '</p></article>';
    }).join('') + '</div>';
  if (sm.pro_tips && sm.pro_tips.length){
    html += '<article class="panel tips"><h3>Pro tips</h3><ul>' + sm.pro_tips.map(function(t){ return '<li>' + esc(t) + '</li>'; }).join('') + '</ul></article>';
  }
  html += '</section>';

  var del = BEHAVIORAL.guide.delivery;
  html += '<section id="b-delivery"><h2>Delivery</h2><article class="panel tips"><ul>' +
    del.map(function(t){ return '<li>' + esc(t) + '</li>'; }).join('') + '</ul></article></section>';

  html += '<section id="b-bank"><h2>Question bank — ' + BEHAVIORAL.questions.length + ' questions</h2><p class="lede2">Expand any question for a STAR outline, model points, and pitfalls to avoid.</p><div class="qbank">';
  html += BEHAVIORAL.questions.map(function(q, i){
    var sg = q.star_guide;
    var body = '<h4>SITUATION</h4><p>' + esc(sg.situation) + '</p>' +
      '<h4>TASK</h4><p>' + esc(sg.task) + '</p>' +
      '<h4>ACTION</h4><p>' + esc(sg.action) + '</p>' +
      '<h4>RESULT</h4><p>' + esc(sg.result) + '</p>' +
      '<h4>MODEL POINTS</h4><ul>' + q.model_points.map(function(m){ return '<li>' + esc(m) + '</li>'; }).join('') + '</ul>' +
      '<h4>PITFALLS</h4><ul>' + q.pitfalls.map(function(p){ return '<li>' + esc(p) + '</li>'; }).join('') + '</ul>';
    return '<div class="q-item"><button class="q-toggle" data-i="' + i + '"><span><span class="qcat">' + esc(q.category) + '</span>&nbsp;&nbsp;' + esc(q.question) + '</span><span class="chev">▾</span></button><div class="q-body">' + body + '</div></div>';
  }).join('');
  html += '</div></section>';

  el('behavioralContent').innerHTML = html;
  var toggles = el('behavioralContent').querySelectorAll('.q-toggle');
  for (var i = 0; i < toggles.length; i++){
    (function(b){ b.addEventListener('click', function(){ b.parentElement.classList.toggle('open'); }); })(toggles[i]);
  }
  var navs = document.querySelectorAll('.guide-nav [data-bsec]');
  for (var n = 0; n < navs.length; n++){
    (function(b){ b.addEventListener('click', function(){
      for (var k = 0; k < navs.length; k++) navs[k].classList.remove('active');
      b.classList.add('active');
      var target = el(b.getAttribute('data-bsec'));
      if (target) target.scrollIntoView({behavior: 'smooth', block: 'start'});
    }); })(navs[n]);
  }
}

/* ---------------- Work-style guide ---------------- */
function renderWorkstyle(){
  el('wsGrid').innerHTML = WORKSTYLE.sections.map(function(s){
    var paras = String(s.body).split(/\n\s*\n/).map(function(p){ return '<p>' + esc(p) + '</p>'; }).join('');
    var pts = (s.points && s.points.length) ? '<ul>' + s.points.map(function(p){ return '<li>' + esc(p) + '</li>'; }).join('') + '</ul>' : '';
    return '<article class="panel ws-card"><h3>' + esc(s.heading) + '</h3>' + paras + pts + '</article>';
  }).join('');
}

/* ---------------- Init ---------------- */
renderDashboard();
renderBehavioral();
renderWorkstyle();
})();
</script>
</body>
</html>
"""

for k, v in SUBS.items():
    TPL = TPL.replace(k, v)

OUT = BASE / "index.html"
OUT.write_text(TPL, encoding="utf-8")
print("wrote", OUT, OUT.stat().st_size, "bytes")
