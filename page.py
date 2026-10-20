HTML = r'''<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tap Race</title>
<style>
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,sans-serif;background:#0f172a;color:#e2e8f0}
.wrap{max-width:980px;margin:0 auto;padding:16px;display:grid;grid-template-columns:1fr 300px;gap:16px}
@media(max-width:760px){.wrap{grid-template-columns:1fr}}
.card{background:#1e293b;border-radius:12px;padding:16px}
h1,h2,h3{margin:0 0 12px}
input,select,button{font:inherit;padding:10px 12px;border-radius:8px;border:1px solid #475569;background:#0f172a;color:inherit}
button{cursor:pointer;background:#6366f1;border:0;color:#fff}
.row{display:flex;gap:8px;margin-bottom:10px;flex-wrap:wrap;align-items:center}
.hide{display:none}
.center{text-align:center}
.big{font-size:64px;font-weight:700}
#arena{position:relative;height:340px;background:#0f172a;border-radius:12px;overflow:hidden;touch-action:manipulation}
#tgt{position:absolute;width:80px;height:80px;border-radius:50%;background:#f59e0b;font-size:26px;left:calc(50% - 40px);top:130px;padding:0}
ol,ul{list-style:none;padding:0;margin:0}
li{display:flex;justify-content:space-between;padding:6px 8px;border-radius:6px}
li.me{background:#334155}
#msg,#msg2{color:#f87171}
</style></head>
<body>
<div class="wrap">
<div class="card">
<div id="home">
<h1>Tap Race</h1>
<div class="row"><input id="name" placeholder="Your name" maxlength="16"></div>
<div class="row"><button onclick="create(false)">Create room</button><button onclick="create(true)" style="background:#10b981">Play solo vs bots</button></div>
<div class="row"><input id="code" placeholder="Room code" maxlength="5" style="text-transform:uppercase"><button onclick="join()">Join</button></div>
<p id="msg"></p>
</div>
<div id="room" class="hide">
<div class="row"><h2 id="rc" style="margin:0"></h2><span id="info" style="margin-left:auto"></span></div>
<div id="lobby"><h3>Lobby</h3><ul id="pl"></ul><p id="wait">Waiting for host to start...</p></div>
<div id="count" class="hide center"><h3>Starting in</h3><div id="cd" class="big"></div></div>
<div id="play" class="hide">
<div class="row"><b id="tl"></b><b style="margin-left:auto">Score: <span id="score">0</span></b></div>
<div id="arena"><button id="tgt" onclick="tap()">+1</button></div>
</div>
<div id="done" class="hide center"><h3>Game over</h3><div id="win" class="big" style="font-size:36px"></div><p id="you"></p></div>
<div id="host" class="hide row"><select id="dur"><option value="60">1 min</option><option value="300">5 min</option></select><button onclick="start()">Start game</button></div>
<p id="msg2"></p>
</div>
</div>
<div class="card"><h3>Top 10</h3><ol id="lb"></ol><p id="mine"></p></div>
</div>
<script>
const $=id=>document.getElementById(id);
const S={code:"",name:"",token:"",pending:0,fly:0,off:0,st:null,busy:false};
async function api(p,b){
  const r=await fetch("/api/"+p,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(b)});
  const j=await r.json().catch(()=>({}));
  if(!r.ok)throw new Error(j.error||"Server error");
  return j;
}
function enter(j){
  Object.assign(S,{code:j.code,name:j.name,token:j.token||""});
  $("home").classList.add("hide");
  $("room").classList.remove("hide");
  S.solo=!!j.solo;
  $("rc").textContent=j.solo?"Solo vs bots":"Room "+S.code;
  poll();
  setInterval(poll,800);
  setInterval(render,200);
}
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
  $("lb").innerHTML=s.top.map((p,i)=>`<li class="${p.name===S.name?"me":""}"><span>${i+1}. ${p.name}</span><b>${p.score}</b></li>`).join("");
  $("mine").textContent=s.me.rank>10?`You: #${s.me.rank} - ${s.me.score}`:"";
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
  $("pl").innerHTML=s.players.map(n=>`<li><span>${n}</span><span>${n===s.host?"host":s.solo?"bot":""}</span></li>`).join("");
  if(m==="count")$("cd").textContent=Math.ceil(s.start_at-t);
  if(m==="play"){
    $("tl").textContent=fmt(s.end_at-t);
    $("score").textContent=s.me.score+S.pending+S.fly;
  }
  if(m==="done"){
    $("win").textContent=s.winner?`${s.winner.name} wins - ${s.winner.score}`:"";
    $("you").textContent=`You: #${s.me.rank} - ${s.me.score}`;
  }
}
function tap(){
  const s=S.st;
  if(!s)return;
  const t=Date.now()/1000+S.off;
  if(!s.start_at||t<s.start_at||t>=s.end_at)return;
  S.pending++;
  const a=$("arena"),b=$("tgt");
  b.style.left=Math.random()*(a.clientWidth-80)+"px";
  b.style.top=Math.random()*(a.clientHeight-80)+"px";
  render();
}
</script>
</body></html>'''
