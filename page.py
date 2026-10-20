HTML = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tap Race</title>
<style>
:root{--bg:#0a0b1a;--card:rgba(255,255,255,.05);--line:rgba(255,255,255,.1);--txt:#e8eaff;--mut:#8b90b8;--a:#7c5cff;--b:#22d3ee;--g:#10b981;--r:#f43f5e;--y:#fbbf24}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;color:var(--txt);background:var(--bg);overflow-x:hidden}
.bg{position:fixed;inset:0;z-index:-1;background:radial-gradient(60% 50% at 15% 0%,rgba(124,92,255,.35),transparent),radial-gradient(50% 40% at 90% 10%,rgba(34,211,238,.22),transparent),radial-gradient(50% 50% at 50% 110%,rgba(244,63,94,.18),transparent)}
.bg:after{content:"";position:absolute;inset:0;background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:44px 44px;opacity:.25;mask-image:radial-gradient(70% 60% at 50% 30%,#000,transparent)}
.app{max-width:1020px;margin:0 auto;padding:24px 16px 40px}
header{display:flex;align-items:baseline;gap:14px;margin-bottom:22px;flex-wrap:wrap}
.logo{font-size:30px;font-weight:900;letter-spacing:3px}
.logo span{background:linear-gradient(90deg,var(--a),var(--b));-webkit-background-clip:text;background-clip:text;color:transparent}
.tag{color:var(--mut);font-size:14px}
.grid{display:grid;grid-template-columns:1fr 320px;gap:18px}
@media(max-width:800px){.grid{grid-template-columns:1fr}}
.panel{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:22px;backdrop-filter:blur(14px);box-shadow:0 20px 60px rgba(0,0,0,.35)}
h2{margin:0 0 4px;font-size:26px}
h3{margin:0 0 14px;font-size:17px}
.sub{color:var(--mut);margin:0 0 18px}
input,select{font:inherit;color:var(--txt);background:rgba(0,0,0,.35);border:1px solid var(--line);border-radius:12px;padding:13px 14px;outline:none;transition:.15s;width:100%}
input:focus,select:focus{border-color:var(--a);box-shadow:0 0 0 3px rgba(124,92,255,.25)}
select{width:auto}
#code{text-transform:uppercase;letter-spacing:6px;font-weight:700;text-align:center}
.btn{font:inherit;font-weight:700;color:#fff;border:0;border-radius:12px;padding:13px 18px;cursor:pointer;background:rgba(255,255,255,.1);transition:.15s;white-space:nowrap}
.btn:hover{transform:translateY(-2px);filter:brightness(1.15)}
.btn:active{transform:translateY(0)}
.btn.primary{background:linear-gradient(135deg,var(--a),#5b8cff);box-shadow:0 8px 24px rgba(124,92,255,.4)}
.btn.green{background:linear-gradient(135deg,var(--g),#06b6d4);box-shadow:0 8px 24px rgba(16,185,129,.35)}
.btns{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0}
@media(max-width:480px){.btns{grid-template-columns:1fr}}
.or{display:flex;align-items:center;gap:12px;color:var(--mut);font-size:13px;margin:18px 0}
.or:before,.or:after{content:"";flex:1;height:1px;background:var(--line)}
.join{display:grid;grid-template-columns:1fr auto;gap:10px}
#msg,#msg2{color:var(--r);min-height:20px;margin:10px 0 0;font-size:14px}
.hide{display:none!important}
.center{text-align:center}
.bar{display:flex;gap:10px;align-items:center;margin-bottom:18px;flex-wrap:wrap}
.pill{font:inherit;font-weight:700;font-size:14px;color:var(--txt);background:rgba(255,255,255,.08);border:1px solid var(--line);border-radius:999px;padding:7px 14px}
button.pill{cursor:pointer}
button.pill:hover{border-color:var(--a)}
.bar .pill:last-child{margin-left:auto;color:var(--mut)}
.chips{list-style:none;padding:0;margin:0 0 16px;display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}
.chips li{display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.06);border:1px solid var(--line);border-radius:12px;padding:8px 10px;animation:in .3s}
.chips li span{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-weight:600}
.chips em{font-style:normal;font-size:11px;color:var(--mut);text-transform:uppercase;letter-spacing:1px}
.av{display:inline-grid;place-items:center;width:30px;height:30px;border-radius:50%;font-style:normal;font-weight:800;font-size:13px;color:#fff;flex:none}
.hint{color:var(--mut);text-align:center;padding:10px}
.hint:before{content:"";display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--b);margin-right:8px;animation:blink 1s infinite}
.hostbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:6px}
.cd{font-size:130px;font-weight:900;line-height:1;background:linear-gradient(135deg,var(--a),var(--b));-webkit-background-clip:text;background-clip:text;color:transparent;animation:pulse 1s infinite}
.top{display:flex;align-items:center;gap:14px;margin-bottom:10px}
#tl{font-size:34px;font-weight:800;font-variant-numeric:tabular-nums;min-width:90px}
#tl.warn{color:var(--r);animation:pulse .6s infinite}
.sc{margin-left:auto;text-align:right}
.sc small{display:block;color:var(--mut);font-size:12px;text-transform:uppercase;letter-spacing:2px}
#score{font-size:38px;font-weight:900;display:inline-block;transition:transform .1s}
#score.bump{transform:scale(1.25);color:var(--y)}
.prog{height:8px;border-radius:99px;background:rgba(255,255,255,.08);overflow:hidden;margin-bottom:14px}
.prog i{display:block;height:100%;width:100%;background:linear-gradient(90deg,var(--b),var(--a));transition:width .25s linear}
#arena{position:relative;height:380px;border-radius:16px;overflow:hidden;background:radial-gradient(circle at 50% 50%,rgba(124,92,255,.12),rgba(0,0,0,.35));border:1px solid var(--line);touch-action:manipulation;user-select:none}
#tgt{position:absolute;width:84px;height:84px;border-radius:50%;border:0;cursor:pointer;left:calc(50% - 42px);top:150px;font-size:24px;font-weight:900;color:#fff;background:radial-gradient(circle at 30% 30%,#ffe08a,var(--y) 40%,#f97316);box-shadow:0 0 0 6px rgba(251,191,36,.2),0 0 40px rgba(251,191,36,.6);transition:left .12s ease-out,top .12s ease-out,transform .08s;animation:float 1.6s ease-in-out infinite}
#tgt:active{transform:scale(.88)}
.pop{position:absolute;font-weight:900;font-size:22px;color:var(--y);pointer-events:none;animation:up .6s ease-out forwards}
.trophy{font-size:60px;animation:float 2s ease-in-out infinite}
#win{font-size:30px;font-weight:900;margin:4px 0 18px;background:linear-gradient(90deg,var(--y),#fb7185);-webkit-background-clip:text;background-clip:text;color:transparent}
.podium{display:flex;justify-content:center;align-items:flex-end;gap:10px;margin:8px 0 14px}
.step{display:flex;flex-direction:column;align-items:center;gap:4px;width:30%;max-width:130px}
.step b{font-size:14px;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.step span{color:var(--mut);font-weight:700}
.blk{width:100%;border-radius:10px 10px 0 0;display:grid;place-items:center;font-size:24px;font-weight:900;background:linear-gradient(180deg,rgba(124,92,255,.7),rgba(124,92,255,.15))}
.s0 .blk{height:100px;background:linear-gradient(180deg,rgba(251,191,36,.8),rgba(251,191,36,.15))}
.s1 .blk{height:70px}
.s2 .blk{height:48px;background:linear-gradient(180deg,rgba(244,114,70,.7),rgba(244,114,70,.12))}
#you{color:var(--mut);margin:6px 0 14px}
#lb{list-style:none;padding:0;margin:0;display:grid;gap:7px}
#lb li{position:relative;display:flex;align-items:center;gap:10px;padding:9px 10px;border-radius:12px;background:rgba(255,255,255,.05);overflow:hidden;animation:in .25s}
#lb li .fill{position:absolute;left:0;top:0;bottom:0;background:linear-gradient(90deg,rgba(124,92,255,.35),transparent);transition:width .5s}
#lb li>*{position:relative}
#lb li.me{outline:1.5px solid var(--b);background:rgba(34,211,238,.1)}
#lb .rk{width:26px;text-align:center;font-weight:800;color:var(--mut)}
#lb .nm{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-weight:600}
#lb b{font-variant-numeric:tabular-nums}
.empty{color:var(--mut);text-align:center;padding:16px 0}
#mine{margin:12px 0 0;text-align:center;color:var(--b);font-weight:700}
@keyframes pulse{50%{transform:scale(1.08)}}
@keyframes float{50%{translate:0 -6px}}
@keyframes blink{50%{opacity:.2}}
@keyframes in{from{opacity:0;transform:translateY(6px)}}
@keyframes up{to{opacity:0;transform:translateY(-50px) scale(1.4)}}
</style></head>
<body>
<div class="bg"></div>
<div class="app">
<header><div class="logo">TAP<span>RACE</span></div><div class="tag">Fast fingers. Live leaderboard.</div></header>
<main class="grid">
<section class="panel">
<div id="home">
<h2>Ready to race?</h2>
<p class="sub">Pick a name and jump in.</p>
<input id="name" placeholder="Your name" maxlength="16" autocomplete="off">
<div class="btns"><button class="btn primary" onclick="create(false)">Create room</button><button class="btn green" onclick="create(true)">Play solo vs bots</button></div>
<div class="or">or join a friend</div>
<div class="join"><input id="code" placeholder="CODE" maxlength="5" autocomplete="off"><button class="btn" onclick="join()">Join</button></div>
<p id="msg"></p>
</div>
<div id="room" class="hide">
<div class="bar"><button class="pill" id="rc" onclick="copyCode()"></button><span class="pill" id="info"></span></div>
<div id="lobby"><h3>Lobby</h3><ul id="pl" class="chips"></ul><div id="wait" class="hint">Waiting for host to start</div></div>
<div id="count" class="hide center"><h3>Get ready</h3><div id="cd" class="cd"></div></div>
<div id="play" class="hide">
<div class="top"><div id="tl"></div><div class="sc"><small>Score</small><span id="score">0</span></div></div>
<div class="prog"><i id="pf"></i></div>
<div id="arena"><button id="tgt" onclick="tap()">+1</button></div>
</div>
<div id="done" class="hide center"><div class="trophy">🏆</div><div id="win"></div><div id="pod" class="podium"></div><p id="you"></p></div>
<div id="host" class="hostbar hide"><select id="dur"><option value="60">1 minute</option><option value="300">5 minutes</option></select><button class="btn primary" onclick="start()">Start game</button></div>
<p id="msg2"></p>
</div>
</section>
<aside class="panel"><h3>🏆 Top 10</h3><ol id="lb"></ol><div id="empty" class="empty">No players yet</div><p id="mine"></p></aside>
</main>
</div>
<script>
const $=id=>document.getElementById(id);
const S={code:"",name:"",token:"",solo:false,pending:0,fly:0,off:0,st:null,busy:false};
const hue=n=>{let h=0;for(const c of n)h=(h*31+c.charCodeAt(0))%360;return h};
const av=n=>`<i class="av" style="background:hsl(${hue(n)} 65% 50%)">${n[0].toUpperCase()}</i>`;
const medal=i=>["🥇","🥈","🥉"][i]||i+1;
async function api(p,b){
  const r=await fetch("/api/"+p,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(b)});
  const j=await r.json().catch(()=>({}));
  if(!r.ok)throw new Error(j.error||"Server error");
  return j;
}
function enter(j){
  Object.assign(S,{code:j.code,name:j.name,token:j.token||"",solo:!!j.solo});
  $("home").classList.add("hide");
  $("room").classList.remove("hide");
  $("rc").textContent=S.solo?"🤖 Solo vs bots":"Room "+S.code+"  ⧉";
  poll();
  setInterval(poll,800);
  setInterval(render,200);
}
function copyCode(){if(!S.solo&&navigator.clipboard){navigator.clipboard.writeText(S.code);$("rc").textContent="Copied ✓";setTimeout(()=>$("rc").textContent="Room "+S.code+"  ⧉",1200)}}
async function create(solo){try{enter(await api("create",{name:$("name").value,solo}))}catch(e){$("msg").textContent=e.message}}
async function join(){try{enter(await api("join",{name:$("name").value,code:$("code").value}))}catch(e){$("msg").textContent=e.message}}
async function start(){
  try{await api("start",{code:S.code,token:S.token,duration:+$("dur").value});$("msg2").textContent="";poll()}
  catch(e){$("msg2").textContent=e.message}
}
async function poll(){
  if(S.busy)return;
  S.busy=true;
  const c=S.pending;
  S.pending=0;
  S.fly=c;
  try{
    const s=await api("sync",{code:S.code,name:S.name,clicks:c});
    S.off=s.now-Date.now()/1000;
    S.st=s;
    board(s);
  }catch(e){S.pending+=c}
  S.fly=0;
  S.busy=false;
  render();
}
function board(s){
  const mx=Math.max(1,s.top.length?s.top[0].score:1);
  $("empty").classList.toggle("hide",s.top.length>0);
  $("lb").innerHTML=s.top.map((p,i)=>`<li class="${p.name===S.name?"me":""}"><div class="fill" style="width:${p.score/mx*100}%"></div><span class="rk">${medal(i)}</span>${av(p.name)}<span class="nm">${p.name}</span><b>${p.score}</b></li>`).join("");
  $("mine").textContent=s.me.rank>10?`You: #${s.me.rank} · ${s.me.score}`:"";
}
const fmt=x=>{x=Math.max(0,Math.ceil(x));return Math.floor(x/60)+":"+String(x%60).padStart(2,"0")};
function render(){
  const s=S.st;
  if(!s)return;
  const t=Date.now()/1000+S.off;
  let m="lobby";
  if(s.start_at)m=t<s.start_at?"count":t<s.end_at?"play":"done";
  for(const k of["lobby","count","play","done"])$(k).classList.toggle("hide",k!==m);
  $("host").classList.toggle("hide",!(S.token&&(m==="lobby"||m==="done")));
  $("wait").classList.toggle("hide",!!S.token);
  $("info").textContent=s.solo?"vs "+(s.players.length-1)+" bots":s.players.length+"/25 players";
  $("pl").innerHTML=s.players.map(n=>`<li>${av(n)}<span>${n}</span><em>${n===s.host?"host":s.solo?"bot":""}</em></li>`).join("");
  if(m==="count")$("cd").textContent=Math.max(1,Math.ceil(s.start_at-t));
  if(m==="play"){
    const left=s.end_at-t;
    $("tl").textContent=fmt(left);
    $("tl").classList.toggle("warn",left<=10);
    $("pf").style.width=Math.max(0,left/s.duration*100)+"%";
    $("score").textContent=s.me.score+S.pending+S.fly;
  }
  if(m==="done"){
    $("win").textContent=s.winner?`${s.winner.name} wins · ${s.winner.score}`:"";
    $("pod").innerHTML=[1,0,2].filter(i=>s.top[i]).map(i=>`<div class="step s${i}">${av(s.top[i].name)}<b>${s.top[i].name}</b><span>${s.top[i].score}</span><div class="blk">${i+1}</div></div>`).join("");
    $("you").textContent=`Your result: #${s.me.rank} · ${s.me.score} pts`;
  }
}
function tap(){
  const s=S.st;
  if(!s)return;
  const t=Date.now()/1000+S.off;
  if(!s.start_at||t<s.start_at||t>=s.end_at)return;
  S.pending++;
  const a=$("arena"),b=$("tgt");
  const p=document.createElement("span");
  p.className="pop";
  p.textContent="+1";
  p.style.left=b.offsetLeft+30+"px";
  p.style.top=b.offsetTop+"px";
  a.appendChild(p);
  setTimeout(()=>p.remove(),600);
  b.style.left=Math.random()*(a.clientWidth-84)+"px";
  b.style.top=Math.random()*(a.clientHeight-84)+"px";
  const sc=$("score");
  sc.classList.add("bump");
  setTimeout(()=>sc.classList.remove("bump"),100);
  render();
}
</script>
</body></html>'''
