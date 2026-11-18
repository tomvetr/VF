import sys,os,json,re
S=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,S)
import osog
sel=set(json.load(open(S+'/ossel.json')))
rows=[x for x in osog.rows if x['id'] in sel]
import oscat,collections
for x in rows: x['nd'],x['ns']=oscat.newcat(x)
depts=[];di={};si={}
for k,en,e,hue,subs in oscat.DEPTS:
    used=[n for n in subs if any(x['nd']==k and x['ns']==n for x in rows)]
    assert all(x['ns'] in subs for x in rows if x['nd']==k),[x['ns'] for x in rows if x['nd']==k and x['ns'] not in subs][:3]
    di[k]=len(depts)
    for j,n in enumerate(used): si[(k,n)]=j
    depts.append({'k':k,'en':en,'zh':oscat.TR[en][0],'he':oscat.TR[en][1],'e':e,'hue':hue,'subs':[{'k':'s%d'%j,'en':n,'zh':oscat.TR[n][0],'he':oscat.TR[n][1]} for j,n in enumerate(used)]})
cnt=collections.defaultdict(collections.Counter)
for x in rows: cnt[x['nd']][x['cls']]+=1
print({k:(v['v'],v['n']) for k,v in cnt.items()})
def cl(t): return re.sub(r'\s+',' ',t.replace('NULL','')).strip()
data=[]
for x in sorted(rows,key=lambda x:(di[x['nd']],si[(x['nd'],x['ns'])],x['h'])):
    data.append([int(x['id']),cl(x['name']),cl(x['size']),float(x['price']),1 if x['cls']=='v' else 0,di[x['nd']],si[(x['nd'],x['ns'])],cl(x['ingredients'])])
s=open('/home/user/VF/supermarket.html',encoding='utf8').read()
a=s.index('var TARGET=1000;'); b=s.index('var NVEG=PRODUCTS')
new='''var DEPTS=%s;
var DATA=%s;
var PRODUCTS=[],TAILS={};
function hsh(n){n=(n+1)*2654435761>>>0;n^=n>>>15;n=Math.imul(n,2246822519)>>>0;n^=n>>>13;return n>>>0;}
DEPTS.forEach(function(d){d.subs.forEach(function(s,i){s.dept=d;s.hue=(d.hue+i*13)%%360;});});
DATA.forEach(function(r,i){var d=DEPTS[r[5]],h=hsh(r[0]);
  PRODUCTS.push({id:i,oid:r[0],d:d,s:d.subs[r[6]],br:['',''],size:r[2],price:r[3],v:r[4],h:h,pop:h%%1000,sold:0,rate:'',
    b:{e:d.e,zh:r[1],en:r[1],ingZh:r[7],ingEn:r[7],ph:'osog-images/'+r[0]+'.jpg'}});});
''' % (json.dumps(depts,ensure_ascii=False,separators=(',',':')),json.dumps(data,ensure_ascii=False,separators=(',',':')))
s=s[:a]+new+s[b:]
def r(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:70],s.count(a)); s=s.replace(a,b)
r("function sizeT(s){s=s.replace('x','×');if(lang==='zh')return s;UNITS.forEach(function(u){s=s.split(u[0]).join(u[1]);});return s;}","function sizeT(s){return s;}")
r("function pname(p){return lang==='zh'?p.br[0]+' '+p.b.zh+' '+sizeT(p.size):p.br[1]+' '+p.b.en+' '+sizeT(p.size);}","function pname(p){return p.b.en;}")
r("<em>¥</em>","<em>$</em>"); r("'<s>¥'+money","'<s>$'+money")
s=s.replace(">¥'+",">$'+")
r("esc(sizeT(p.size))+' · '+t('sold')(p.sold)+'</div>'","esc(sizeT(p.size))+'</div>'")
r("'<div class=\"meta\">★ '+p.rate+' · '+t('sold')(p.sold)+'</div>'+priceH(p)","'<div class=\"meta\">'+esc(p.size)+'</div>'+priceH(p)")
s,n=re.subn(r"<dt>'\+t\('origin'\).*?</dl>","</dl>",s); assert n==1
r("  h+='<section class=\"sec\"><div class=\"sechead\"><h2>⚡ '+t('deals')+'</h2><span class=\"sub\">'+t('dealsS')+'</span></div><div class=\"hscroll\">'+deals.map(card).join('')+'</div></section>';\n","")
r("var ship=sub>=99||!n?0:6;","var ship=0;")
s,n=re.subn(r"'<div class=\"ship\">'\+.*?</div></div><div class=\"dbody\">'\+","'<div class=\"dbody\">'+",s); assert n==1
r("<label><input type=\"checkbox\" id=\"dealChk\"'+(onlyDeal?' checked':'')+'> '+t('onlyDeal')+'</label>","")
r("[['pop','sPop'],['asc','sAsc'],['desc','sDesc'],['sold','sSold']]","[['pop','sPop'],['asc','sAsc'],['desc','sDesc']]")
r("ph:'Search 1,000 products, e.g. \"tofu\", \"noodles\"'","ph:'Search 1,000 products, e.g. \"pasta\", \"cereal\"'")
r("addrV:'100 Century Avenue, Pudong, Shanghai · Mr. Zhang 138****0000'","addrV:'Your saved address'")
r("wx:'WeChat Pay',ali:'Alipay',card:'Bank card'","wx:'Credit card',ali:'PayPal',card:'Apple Pay'")
r("hot:'Popular'","hot:''")
r("if(/^(zh|cn|chinese)$/i.test(qs.get('lang')||''))lang='zh';","")
r("try{var c=JSON.parse(localStorage.getItem('hx_cart')","try{var c=JSON.parse(localStorage.getItem('os_cart')")
r("localStorage.setItem('hx_cart'","localStorage.setItem('os_cart'")
r("  img.ph{width:100%;height:100%;object-fit:cover;display:block;}","  #langBtn{display:none;}\n  img.ph{width:100%;height:100%;object-fit:contain;display:block;background:#fff;}")
r("<a href=\"#/c/'+(vegan?'tofu':'produce')+'\">","<a href=\"#/\">") if "(vegan?'tofu':'produce')" in s else None
r("esc(lang==='zh'?p.br[0]:p.br[1])+' · '+L(p.d)","L(p.d)")
r("(p.b.zh+p.br[0]+p.s.zh+p.d.zh+' '+p.b.en+' '+p.br[1]+' '+p.s.en+' '+p.d.en)","p.b.en")
r("  else list.sort(byPop);","  else{list.sort(byPop);if(!vegan&&LEAD)list=leadNV(list,LEAD);}")
r("var d=deptOf(dk);if(!d)return viewHome();","var d=deptOf(dk);if(!d)return viewHome();LEAD=(d.k in LEADS)?LEADS[d.k]:5;")
r("function viewSearch(q){","function viewSearch(q){LEAD=5;")
r("row=vis.filter(function(p){return p.d===d;}).sort(byPop).filter(","row=leadNV(vis.filter(function(p){return p.d===d;}).sort(byPop),vegan||(d.k in LEADS&&!LEADS[d.k])?0:99).filter(")
r("function byPop(a,b)","// with the filter off, the first vegan product appears no earlier than 6th (11th in Meat); not applied to Fruit & Veg\nvar LEADS={meat:10,produce:0,plant:0},LEAD=0;\nvar ALTRX=/veggie|vegetarian|meatless|vegan|plant[- ]based|dairy[- ]free|non[- ]dairy|tofu|tempeh|morningstar|gardein|beyond meat|lightlife|field roast|boca|quorn|tofurky|almondmilk|soymilk|silk /i;\nfunction leadNV(list,n){var a=[],b=[];list.forEach(function(p){(!p.v&&!ALTRX.test(p.b.en)&&a.length<n?a:b).push(p);});return a.concat(b);}\nfunction byPop(a,b)")
r("  #langBtn{display:none;}","  #langBtn,#loginBtn{display:none;}")
# ---- languages, label, extra category, study flow ----
r("function t(k){return T[lang][k];}","function t(k){var v=T[lang][k];return v===undefined?T.en[k]:v;}")
r("function L(o){return lang==='zh'?o.zh:o.en;}","function L(o){return o[lang]||o.en;}")
r('<button class="hbtn" data-act="lang" id="langBtn"></button>','')
r('<div class="tabbar" id="tabbar"></div>','<div class="botbar"><div class="wrap"><select id="langSel" class="langsel" aria-label="Language"><option value="en">English</option><option value="zh">中文</option><option value="he">עברית</option></select><button class="hbtn restart" data-act="srestart" id="restartBtn">↺ <span id="restartT">Restart</span></button></div></div>\n<div class="tabbar" id="tabbar"></div>')
r("$('#langBtn').textContent=t('lang');","$('#langSel').value=lang;")
r("  if(e.target.id==='sortSel'){sort=e.target.value;route();}","  if(e.target.id==='langSel'){setLang(e.target.value);}\n  if(e.target.id==='sortSel'){sort=e.target.value;route();}")
r("vis.filter(function(p){return p.d===d;})","vis.filter(function(p){return inDept(p,d);})")
r("PRODUCTS.filter(function(p){return p.d===d&&(!sub||p.s===sub);})","PRODUCTS.filter(function(p){return inDept(p,d)&&(!sub||inSub(p,sub));})")
r("cnt(function(p){return p.d===x;})","cnt(function(p){return inDept(p,x);})")
r("cnt(function(p){return p.s===s;})","cnt(function(p){return inSub(p,s);})")
r("count(PRODUCTS.filter(function(p){return p.d===d;}))","count(PRODUCTS.filter(function(p){return inDept(p,d);}))")
r("'<dl><dt>'+t('ing')+'</dt><dd>'+esc(ingOf(p))+'</dd>","'<dl><dt>'+t('ing')+'</dt><dd>'+esc(ingOf(p))+(LABELS&&p.v?'<div class=\"vtag\">🌱 '+t('vb')+'</div>':'')+'</dd>")
r("[['home','gohome'],['cats','sheet'],['cart','cart'],['me','demo']]","[['home','gohome'],['cats','sheet'],['cart','cart']]")
r("t('checkout')+'</button></div>';","(STUDY?st('finish'):t('checkout'))+'</button></div>';")
r("  else if(a==='checkout')checkout();","  else if(a==='checkout'){if(STUDY)studyFinish();else checkout();}")
r('<header class="hdr">','<header class="hdr">\n  <div class="taskbar" id="taskbar"></div>')
r('\n    <button class="vegan" data-act="vegan" aria-pressed="false"><span>🌱</span><span class="vl"></span><i class="sw"></i></button>','')
r('    <form class="search" id="searchForm" role="search">','    <button class="vegan" data-act="vegan" aria-pressed="false"><span>🌱</span><span class="vl"></span><i class="sw"></i></button>\n    <form class="search" id="searchForm" role="search">')
r('<span class="cnt" data-cnt>0</span></button>\n    </div>','<span class="cnt" data-cnt>0</span></button>\n      <button class="finbtn" data-act="sfinish" id="finishBtn">✓ <span id="finishT">Finish shopping</span></button>\n    </div>')
r('<div class="toast" id="toast"></div>','<div class="toast" id="toast"></div>\n<div class="study" id="study" role="dialog" aria-modal="true"></div>')
r("  #langBtn,#loginBtn{display:none;}","  #loginBtn{display:none;}\n"+open(S+'/study.css').read())
TRD={'n':{},'i':{}}
import os as _os
for L in ('zh','he'):
    f=S+'/tr/names_%s.json'%L
    if _os.path.exists(f): TRD['n'][L]=json.load(open(f))
    m={}
    for part in ('a','b'):
        f=S+'/tr/ing_%s_%s.json'%(part,L)
        if _os.path.exists(f): m.update(json.load(open(f)))
    if m: TRD['i'][L]=m
r("/* ---------- init ---------- */","var TRD="+json.dumps(TRD,ensure_ascii=False,separators=(',',':'))+";\n"+open(S+'/study.js').read()+"\n/* ---------- init ---------- */")
r("'<div class=\"meta\">'+esc(p.size)+'</div>'","'<div class=\"meta\">'+esc(sizeT(p.size))+'</div>'")
r("  \n  try{var c=JSON.parse(localStorage.getItem('os_cart')","  initLang(qs);\n  if(!STUDY)try{var c=JSON.parse(localStorage.getItem('os_cart')")
r("  if(qs.get('vegan')==='1')setVegan(true);else route();","  if(STUDY)studyInit(qs);else if(qs.get('vegan')==='1')setVegan(true);else route();")
open('/home/user/VF/osog.html','w',encoding='utf8').write(s)
r("var STUDY=false;","var STUDY=true;")
open('/home/user/VF/study.html','w',encoding='utf8').write(s)
print(len(s),len(data),sum(d[4] for d in data))
