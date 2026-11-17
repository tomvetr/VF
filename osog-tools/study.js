/* ---------- languages ---------- */
T.he={title:'HEXIAN – סופרמרקט אונליין',logo:'HEXIAN',ph:'חיפוש בין 1,000 מוצרים, למשל "פסטה", "דגני בוקר"',search:'חיפוש',vegan:'פילטר טבעוני',login:'התחברות',cart:'עגלה',
 vnote:function(n){return '🌱 הפילטר הטבעוני פעיל · '+n+' מוצרים עם רכיבים מן החי מוסתרים';},vnoteOff:'כיבוי',home:'בית',cats:'קטגוריות',me:'חשבון',all:'הכול',hot:'',seeAll:'לכל המוצרים',
 items:function(n){return n+' מוצרים';},hidden:function(n){return n+' מוצרים לא טבעוניים הוסתרו';},sort:'מיון',sPop:'מומלץ',sAsc:'מחיר: מהנמוך לגבוה',sDesc:'מחיר: מהגבוה לנמוך',more:'עוד מוצרים',
 results:function(q){return 'תוצאות עבור "'+q+'"';},none:'לא נמצאו מוצרים',noneV:'הפילטר הטבעוני פעיל, ולכן ייתכן שחלק מהמוצרים מוסתרים',tagDeal:'מבצע',tagNew:'חדש',tagOrg:'אורגני',tagOwn:'מותג הבית',vb:'טבעוני',
 add:'הוספה לעגלה',added:function(n){return 'נוסף לעגלה: '+n;},ing:'רכיבים',spec:'גודל',vok:'🌱 טבעוני · הרכיבים נבדקו, ללא רכיבים מן החי',cartT:'העגלה שלך',cartEmpty:'העגלה ריקה',cartEmptyS:'אפשר להתחיל לקנות',goShop:'להתחיל לקנות',
 subtotal:'סכום ביניים',ship:'משלוח',free:'חינם',total:'סה"כ',checkout:'לתשלום',nv:'לא טבעוני',coT:'אישור הזמנה',addr:'כתובת למשלוח',addrV:'הכתובת השמורה שלך',time:'זמן משלוח',timeV:'היום, בהקדם האפשרי',
 pay:'תשלום',wx:'כרטיס אשראי',ali:'PayPal',card:'Apple Pay',demo:'זהו אתר הדגמה: לא תתבצע הזמנה אמיתית ולא יבוצע חיוב.',submit:'ביצוע הזמנה',okT:'הזמנת הדגמה נוצרה',okP:'תודה! זו רק הדגמה.',back:'המשך קנייה',demoToast:'אתר הדגמה: האפשרות אינה זמינה'};
(function(){var z=T.zh;z.title='HEXIAN 网上超市';z.logo='HEXIAN';z.ph='搜索 1000 件商品，如“意面”“麦片”';z.hot='';z.addrV='您保存的地址';z.timeV='今天，尽快送达';z.wx='信用卡';z.ali='PayPal';z.card='Apple Pay';z.demo='这是演示网站：订单不会真实提交，也不会扣款。';})();
function setLang(v){if(!T[v])v='en';lang=v;try{localStorage.setItem('vf_lang',v);}catch(e){}
  document.documentElement.dir=v==='he'?'rtl':'ltr';chrome();route();if(STUDY)studyRender();}
function initLang(qs){var v=(qs.get('lang')||'').toLowerCase();if(!T[v]){try{v=localStorage.getItem('vf_lang')||'';}catch(e){v='';}}
  if(!T[v])v='en';lang=v;document.documentElement.dir=v==='he'?'rtl':'ltr';}

/* ---------- extra "Plant-based" department (category version only) ---------- */
var LABELS=false;
function inDept(p,d){return p.d===d||(p.alt&&p.alt.dept===d);}
function inSub(p,s){return p.s===s||p.alt===s;}
var PLANT={k:'plant',en:'Plant-based',zh:'植物基',he:'מבוסס צמחים',e:'🌱',hue:110,subs:[]};
PLANT.subs=[{k:'s0',en:'Milk & dairy alternatives',zh:'植物奶和乳制品替代品',he:'חלב צמחי ותחליפי חלב'},{k:'s1',en:'Meat alternatives',zh:'植物肉',he:'תחליפי בשר'}];
PLANT.subs.forEach(function(s,i){s.dept=PLANT;s.hue=110+i*13;});
PRODUCTS.forEach(function(p){if(!p.v)return;
  if(/tofu|tempeh/i.test(p.b.en)||p.d.k==='meat')p.alt=PLANT.subs[1];else if(p.d.k==='dairy')p.alt=PLANT.subs[0];});

/* ---------- study flow ---------- */
var STUDY=false;
var SURVEY_URL='https://survey.zohopublic.eu/zs/ZbBff1';
var ST={
en:{introT:'Online shopping study',
 intro:['In this study you will shop in an online supermarket three times. Each time, the store works a little differently.',
  'Imagine a vegan friend is coming to stay with you. Each time you will get a short shopping list: add one vegan product for each item to your cart. Vegan means no meat, fish, dairy, eggs or honey. Click a product to see its ingredients.',
  'When you have everything, press “Finish shopping”. After each store you will answer two quick questions, and at the end a short survey. It takes about 10–15 minutes.',
  'Your answers are anonymous. By continuing, you agree to take part.'],
 start:'Start',taskT:function(n){return 'Store '+n+' of 3';},
 control:'No vegan tools: check the ingredient list on each product page.',ctype:'Regular store',ftype:'Store with a vegan filter',ltype:'Store with vegan labels',ktype:'Store with a vegan category',task:'Your task: find one vegan product for each item:',vlist:'Vegan shopping list: find vegan options for the following items:',
 filter:'Turn on the green 🌱 Vegan filter button next to the search bar to see only vegan products.',
 label:'Vegan products have a “Vegan” label under the ingredient list on the product page.',
 category:'The “Plant-based” department at the end of the menu has vegan milk and meat alternatives.',
 listP:'Buy one vegan product for each item:',go:'Go to the store',finish:'Finish shopping',
 confirm:function(h,n){return 'Your cart covers '+h+' of the '+n+' items on your list. Finish anyway?';},keep:'Keep shopping',fin:'Finish',
 q1:'How easy was it to find the items on your list?',q1a:'Very difficult',q1b:'Very easy',
 q2:'How sure are you that everything in your cart is vegan?',q2a:'Not sure at all',q2b:'Completely sure',
 next:'Continue',doneT:'Thank you!',doneP:'You have finished shopping. Now please answer a short survey.',doneB:'Continue to the survey',restart:'Restart',restartQ:'Start the study again from the beginning?',
 bar:function(n){return 'Store '+n+' of 3 · Shopping list:';}},
zh:{introT:'网上购物研究',
 intro:['在本研究中，你将在一家网上超市购物三次。每一次，超市的功能都会略有不同。',
  '想象一位纯素食的朋友要来你家住几天。每次你会拿到一份简短的购物清单：请为清单上的每一项各选一件纯素商品加入购物车。纯素是指不含肉、鱼、奶制品、蛋或蜂蜜。点击商品即可查看配料表。',
  '买齐后，请点击“完成购物”。每家店购物结束后有两个简单问题，最后还有一份简短问卷。全程约需 10–15 分钟。',
  '你的回答是匿名的。继续即表示你同意参加本研究。'],
 start:'开始',taskT:function(n){return '第 '+n+' 家店（共 3 家）';},
 control:'没有纯素工具：请在每件商品的详情页查看配料表。',ctype:'普通超市',ftype:'带纯素筛选的超市',ltype:'带纯素标签的超市',ktype:'带纯素分类的超市',task:'任务：为每一项找到一件纯素商品：',vlist:'纯素购物清单：请为以下各项找到纯素选项：',
 filter:'打开搜索栏旁边的绿色 🌱“纯素筛选”按钮，即可只显示纯素商品。',
 label:'纯素商品的详情页上，配料表下方有“纯素”标签。',
 category:'菜单最后的“植物基”分类里有纯素的植物奶和植物肉。',
 listP:'请为每一项各买一件纯素商品：',go:'进入超市',finish:'完成购物',
 confirm:function(h,n){return '你的购物车目前覆盖了清单上 '+n+' 项中的 '+h+' 项。仍要结束吗？';},keep:'继续购物',fin:'结束',
 q1:'找到清单上的商品有多容易？',q1a:'非常困难',q1b:'非常容易',
 q2:'你有多确定购物车里的所有商品都是纯素的？',q2a:'完全不确定',q2b:'完全确定',
 next:'继续',doneT:'谢谢！',doneP:'购物已完成。接下来请填写一份简短问卷。',doneB:'前往问卷',restart:'重新开始',restartQ:'要从头重新开始吗？',
 bar:function(n){return '第 '+n+'/3 家店 · 购物清单：';}},
he:{introT:'מחקר קנייה אונליין',
 intro:['במחקר הזה תעשו קניות בסופרמרקט אונליין שלוש פעמים. בכל פעם החנות עובדת קצת אחרת.',
  'דמיינו שחבר טבעוני מגיע להתארח אצלכם. בכל פעם תקבלו רשימת קניות קצרה: הוסיפו לעגלה מוצר טבעוני אחד לכל פריט ברשימה. טבעוני פירושו ללא בשר, דגים, מוצרי חלב, ביצים או דבש. לחצו על מוצר כדי לראות את רשימת הרכיבים.',
  'כשתמצאו את כל הפריטים, לחצו על "סיום קנייה". אחרי כל חנות יופיעו שתי שאלות קצרות, ובסוף שאלון קצר. משך ההשתתפות כ-10–15 דקות.',
  'התשובות שלכם אנונימיות. המשך ההשתתפות מהווה הסכמה להשתתף במחקר.'],
 start:'התחלה',taskT:function(n){return 'חנות '+n+' מתוך 3';},
 control:'אין כלים טבעוניים: בדקו את רשימת הרכיבים בעמוד של כל מוצר.',ctype:'חנות רגילה',ftype:'חנות עם פילטר טבעוני',ltype:'חנות עם תוויות טבעוני',ktype:'חנות עם קטגוריה טבעונית',task:'המשימה: מצאו מוצר טבעוני אחד לכל פריט:',vlist:'רשימת קניות טבעונית: מצאו אפשרויות טבעוניות לפריטים הבאים:',
 filter:'הפעילו את הכפתור הירוק 🌱 "פילטר טבעוני" שליד שורת החיפוש כדי לראות רק מוצרים טבעוניים.',
 label:'למוצרים טבעוניים יש תווית "טבעוני" מתחת לרשימת הרכיבים בעמוד המוצר.',
 category:'במחלקת "מבוסס צמחים" בסוף התפריט יש תחליפי חלב ובשר טבעוניים.',
 listP:'קנו מוצר טבעוני אחד לכל פריט:',go:'כניסה לחנות',finish:'סיום קנייה',
 confirm:function(h,n){return 'העגלה שלכם כוללת '+h+' מתוך '+n+' הפריטים ברשימה. לסיים בכל זאת?';},keep:'המשך קנייה',fin:'סיום',
 q1:'עד כמה היה קל למצוא את הפריטים ברשימה?',q1a:'קשה מאוד',q1b:'קל מאוד',
 q2:'עד כמה אתם בטוחים שכל המוצרים בעגלה טבעוניים?',q2a:'בכלל לא בטוח/ה',q2b:'בטוח/ה לגמרי',
 next:'המשך',doneT:'תודה!',doneP:'סיימתם את הקניות. עכשיו נשמח שתענו על שאלון קצר.',doneB:'מעבר לשאלון',restart:'התחלה מחדש',restartQ:'להתחיל את המחקר מחדש מההתחלה?',
 bar:function(n){return 'חנות '+n+'/3 · רשימת קניות:';}}};
function st(k){var v=ST[lang][k];return v===undefined?ST.en[k]:v;}
function secIs(p,n){return p.s.en===n;}
var ITEMS={
 milk:{en:'<b>Vegan</b> milk',zh:'<b>纯素</b>牛奶',he:'חלב <b>טבעוני</b>',m:function(p){return secIs(p,'Milk');}},
 sausages:{en:'<b>Vegan</b> sausage',zh:'<b>纯素</b>香肠',he:'נקניק <b>טבעוני</b>',m:function(p){return secIs(p,'Sausages, Burgers & Deli')&&/sausage|dog|frank|link|brat|chorizo|kielbasa|andouille|wiener/i.test(p.b.en);}},
 bread:{en:'<b>Vegan</b> bread',zh:'<b>纯素</b>面包',he:'לחם <b>טבעוני</b>',m:function(p){return secIs(p,'Bread');}},
 chocolate:{en:'<b>Vegan</b> chocolate',zh:'<b>纯素</b>巧克力',he:'שוקולד <b>טבעוני</b>',m:function(p){return (secIs(p,'Candy, Gum & Mints')||secIs(p,'Baking'))&&/chocolate|cacao/i.test(p.b.en);}},
 yogurt:{en:'<b>Vegan</b> yogurt',zh:'<b>纯素</b>酸奶',he:'יוגורט <b>טבעוני</b>',m:function(p){return secIs(p,'Yogurt');}},
 burgers:{en:'<b>Vegan</b> burger',zh:'<b>纯素</b>汉堡肉饼',he:'המבורגר <b>טבעוני</b>',m:function(p){return /burger|patt(y|ies)/i.test(p.b.en)&&!/\bbuns?\b|helper/i.test(p.b.en);}},
 cookies:{en:'<b>Vegan</b> cookies',zh:'<b>纯素</b>曲奇饼干',he:'עוגיות <b>טבעוניות</b>',m:function(p){return secIs(p,'Cookies');}},
 cereal:{en:'<b>Vegan</b> cereal',zh:'<b>纯素</b>麦片',he:'דגני בוקר <b>טבעוניים</b>',m:function(p){return secIs(p,'Breakfast & Cereal');}},
 creamer:{en:'<b>Vegan</b> creamer',zh:'<b>纯素</b>奶精',he:'מלבין <b>טבעוני</b>',m:function(p){return /creamer/i.test(p.b.en);}},
 bacon:{en:'<b>Vegan</b> bacon',zh:'<b>纯素</b>培根',he:'בייקון <b>טבעוני</b>',m:function(p){return /bacon/i.test(p.b.en);}},
 crackers:{en:'<b>Vegan</b> crackers',zh:'<b>纯素</b>咸饼干',he:'קרקרים <b>טבעוניים</b>',m:function(p){return secIs(p,'Crackers');}},
 bars:{en:'<b>Vegan</b> granola bar',zh:'<b>纯素</b>燕麦棒',he:'חטיף גרנולה <b>טבעוני</b>',m:function(p){return secIs(p,'Bars');}}};
var LISTS=[['milk','sausages','bread','chocolate'],['yogurt','burgers','cookies','cereal'],['creamer','bacon','crackers','bars']];
var TYPE={control:'ctype',filter:'ftype',label:'ltype',category:'ktype'};
var VK={control:'c',filter:'f',label:'a',category:'a'};
var SS=null,TASK=null;
function shuffle(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),x=a[i];a[i]=a[j];a[j]=x;}return a;}
function ssave(){try{localStorage.setItem('vf_study',JSON.stringify(SS));}catch(e){}}
function curVer(){return SS.order[SS.step];}
function curList(){return LISTS[SS.lists[SS.step]];}
function covered(onlyVegan){var l=curList();return l.filter(function(k){for(var id in cart){var p=PRODUCTS[id];if(ITEMS[k].m(p)&&(!onlyVegan||p.v))return true;}return false;});}
function applyVersion(v){
  document.documentElement.classList.toggle('nofilter',v!=='filter');
  LABELS=v==='label';
  var i=DEPTS.indexOf(PLANT);if(v==='category'&&i<0)DEPTS.push(PLANT);if(v!=='category'&&i>=0)DEPTS.splice(i,1);
  vegan=false;document.documentElement.classList.remove('vg');cart={};badge();closeAll();
  chrome();if(location.hash&&location.hash!=='#/')location.hash='#/';else route();
}
function studyInit(qs){
  document.documentElement.classList.add('instudy');
  if(qs.get('reset')==='1'){try{localStorage.removeItem('vf_study');}catch(e){}}
  try{SS=JSON.parse(localStorage.getItem('vf_study')||'null');}catch(e){SS=null;}
  if(!SS){var g=(qs.get('group')||'').toUpperCase();if(g!=='A'&&g!=='B')g=Math.random()<0.5?'A':'B';var alt=g==='A'?'label':'category';
    SS={pid:qs.get('pid')||qs.get('id')||('p'+Date.now().toString(36)+Math.random().toString(36).slice(2,6)),group:g,alt:alt,
        order:shuffle(['control','filter',alt]),lists:shuffle([0,1,2]),step:0,phase:'intro',res:{}};ssave();}
  if(SS.phase==='task'||SS.phase==='q')SS.phase='brief';
  applyVersion(SS.phase==='intro'?null:curVer());
  studyRender();
}
function studyRender(){
  var box=$('#study'),bar=$('#taskbar'),h='';var rt=document.getElementById('restartT');if(rt)rt.textContent=st('restart');var ft=document.getElementById('finishT');if(ft)ft.textContent=st('finish');document.documentElement.classList.toggle('intask',SS.phase==='task');
  if(SS.phase==='task'){box.classList.remove('show');
    var got=covered(false);
    bar.innerHTML='<div class="wrap tb"><div class="tb1"><span class="tbs">'+st('taskT')(SS.step+1)+'</span><b>'+st(TYPE[curVer()])+'</b> — '+st(curVer())+'</div><div class="tb2"><span class="tbl">'+st('vlist')+'</span>'+curList().map(function(k){var ok=got.indexOf(k)>=0;return '<span class="ti'+(ok?' ok':'')+'">'+(ok?'✓ ':'')+L(ITEMS[k])+'</span>';}).join('')+'</div></div>';
    bar.classList.add('show');return;}
  bar.classList.remove('show');
  var langSel='<div class="lang"><select class="langsel" onchange="setLang(this.value)">'+[['en','English'],['zh','中文'],['he','עברית']].map(function(o){return '<option value="'+o[0]+'"'+(lang===o[0]?' selected':'')+'>'+o[1]+'</option>';}).join('')+'</select></div>';
  if(SS.phase==='intro')h=langSel+'<h2>'+st('introT')+'</h2>'+st('intro').map(function(x){return '<p>'+x+'</p>';}).join('')+'<button class="cta" data-act="sgo" data-to="brief">'+st('start')+'</button>';
  else if(SS.phase==='brief')h=langSel+'<h2>'+st('taskT')(SS.step+1)+'</h2><div class="ver"><b>'+st(TYPE[curVer()])+'</b><br>'+st(curVer())+'</div><p>'+st('task')+'</p><ul>'+curList().map(function(k){return '<li>'+L(ITEMS[k])+'</li>';}).join('')+'</ul><button class="cta" data-act="sgo" data-to="task">'+st('go')+'</button>';
  else if(SS.phase==='confirm')h='<p style="font-size:16px;font-weight:600">'+st('confirm')(covered(false).length,curList().length)+'</p><div class="row2"><button class="cta ghost" data-act="sgo" data-to="task">'+st('keep')+'</button><button class="cta" data-act="sgo" data-to="q">'+st('fin')+'</button></div>';
  else if(SS.phase==='q'){var r=SS.res[VK[curVer()]]||{};
    var sc=function(key,qa,qb,q){return '<div class="q">'+st(q)+'</div><div class="scale">'+[1,2,3,4,5].map(function(n){return '<button data-act="sans" data-k="'+key+'" data-v="'+n+'" class="'+(r[key]===n?'on':'')+'">'+n+'</button>';}).join('')+'</div><div class="scl"><span>'+st(qa)+'</span><span>'+st(qb)+'</span></div>';};
    h='<h2>'+st('taskT')(SS.step+1)+'</h2>'+sc('ease','q1a','q1b','q1')+sc('sure','q2a','q2b','q2')+'<button class="cta" data-act="snext"'+(r.ease&&r.sure?'':' disabled')+'>'+st('next')+'</button>';}
  else if(SS.phase==='done')h='<h2>'+st('doneT')+'</h2><p>'+st('doneP')+'</p><button class="cta" data-act="ssurvey">'+st('doneB')+'</button><button class="cta ghost" style="margin-top:10px" data-act="srestart" data-noask="1">↺ '+st('restart')+'</button>';
  box.innerHTML='<div class="sbox">'+h+'</div>';box.classList.add('show');
}
function startTask(){
  applyVersion(curVer());
  TASK={t0:Date.now(),clicks:0,pages:0,searches:0,feature:0};SS.phase='task';ssave();studyRender();
}
function studyFinish(){
  if(SS.phase!=='task')return;
  if(covered(false).length<curList().length){SS.phase='confirm';studyRender();return;}
  endTask();
}
function endTask(){
  var ids=Object.keys(cart),k=VK[curVer()],o=SS.res[k]||{};
  o.list=SS.lists[SS.step]+1;o.pos=SS.step+1;
  if(TASK){o.time=Math.round((Date.now()-TASK.t0)/1000);o.clicks=TASK.clicks;o.pages=TASK.pages;o.search=TASK.searches;o.feature=TASK.feature;}
  o.items=ids.length;o.found=covered(true).length;o.nonvegan=ids.filter(function(id){return !PRODUCTS[id].v;}).length;
  o.cart=ids.map(function(id){return DATA[id][0];}).join('-');
  SS.res[k]=o;TASK=null;SS.phase='q';closeAll();ssave();studyRender();
}
function surveyUrl(){
  var q={pid:SS.pid,group:SS.group,alt:SS.alt,order:SS.order.map(function(v){return VK[v];}).join(''),lang:lang};
  ['c','f','a'].forEach(function(k){var o=SS.res[k]||{};['list','pos','time','clicks','pages','search','feature','items','found','nonvegan','ease','sure','cart'].forEach(function(f){q[k+'_'+f]=o[f]===undefined?'':o[f];});});
  return SURVEY_URL+'?'+Object.keys(q).map(function(k){return k+'='+encodeURIComponent(q[k]);}).join('&');
}
document.addEventListener('click',function(e){
  if(!STUDY||!SS)return;
  if(TASK&&SS.phase==='task')TASK.clicks++;
  var el=e.target.closest('[data-act]');if(!el)return;var a=el.dataset.act;
  if(a==='sgo'){var to=el.dataset.to;
    if(to==='task'){if(SS.phase==='confirm'){SS.phase='task';studyRender();}else startTask();}
    else if(to==='q')endTask();
    else{SS.phase=to;ssave();studyRender();}}
  else if(a==='sfinish')studyFinish();
  else if(a==='sans'){var r=SS.res[VK[curVer()]];r[el.dataset.k]=+el.dataset.v;ssave();studyRender();}
  else if(a==='snext'){if(SS.step<2){SS.step++;SS.phase='brief';applyVersion(curVer());}else{SS.phase='done';SS.doneAt=Date.now();applyVersion(null);}ssave();studyRender();}
  else if(a==='srestart'){if(el.dataset.noask||confirm(st('restartQ'))){try{localStorage.removeItem('vf_study');}catch(e){}var u=new URLSearchParams(location.search);u.delete('reset');u.delete('group');var q=u.toString();location.href=location.pathname+(q?'?'+q:'')+'#/';setTimeout(function(){location.reload();},50);}}
  else if(a==='ssurvey'){(window.top||window).location.href=surveyUrl();}
},true);
if(true){
  var _op=openProduct;openProduct=function(id){if(STUDY&&TASK){TASK.pages++;if(LABELS&&PRODUCTS[id].v)TASK.feature++;}_op(id);};
  var _sv=setVegan;setVegan=function(on){if(STUDY&&TASK&&on&&curVer()==='filter')TASK.feature++;_sv(on);};
  var _sq=setQty;setQty=function(id,q){_sq(id,q);if(STUDY&&SS&&SS.phase==='task')studyRender();};
  $('#searchForm').addEventListener('submit',function(){if(STUDY&&TASK)TASK.searches++;});
  window.addEventListener('hashchange',function(){if(STUDY&&TASK&&curVer()==='category'&&/^#\/c\/plant(\/|$)/.test(location.hash))TASK.feature++;});
}
