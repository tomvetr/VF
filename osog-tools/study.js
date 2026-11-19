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

/* ---------- extra green "Vegan" department (category version only) ---------- */
var LABELS=false;
function inDept(p,d){return p.d===d||(p.alt&&p.alt.dept===d);}
function inSub(p,s){return p.s===s||p.alt===s;}
var PLANT={k:'plant',en:'Plant-based',zh:'植物基',he:'מבוסס צמחים',e:'🌱',hue:110,subs:[]};
PLANT.subs=[{k:'s0',en:'Dairy alternatives',zh:'乳制品替代品',he:'תחליפי חלב'},{k:'s1',en:'Meat alternatives',zh:'植物肉',he:'תחליפי בשר'}];
PLANT.subs.forEach(function(s,i){s.dept=PLANT;s.hue=110+i*13;});
PRODUCTS.forEach(function(p){if(!p.v)return;
  if(/tofu|tempeh/i.test(p.b.en)||p.d.k==='meat')p.alt=PLANT.subs[1];else if(p.d.k==='dairy')p.alt=PLANT.subs[0];});

/* ---------- study flow ---------- */
var STUDY=false;
var REQUIRE_ALL=false; // true = participants must add all list items before 'Finish shopping' works
var SURVEY_URL='https://survey.zohopublic.eu/zs/9fCd5d';
var ST={
en:{introT:'Online shopping study',
 intro:['In this study you will shop in an online supermarket three times. Each time, the store works a little differently.',
  'Imagine a vegan friend is coming to stay with you. Each time you will get a short shopping list: add one vegan product for each item to your cart. Vegan means no meat, fish, dairy, eggs or honey. Click a product to see its ingredients.',
  'When all four items are in your cart, the store closes automatically. After each store you will answer one quick question, and at the end a short survey. It takes about 10–15 minutes.',
  'Your answers are anonymous. By continuing, you agree to take part.'],
 start:'Start',taskT:function(n){return 'Store '+n+' of 3';},
 control:'No vegan tools: check the ingredient list on each product page.',ctype:'Regular store',ftype:'Store with a vegan filter',ltype:'Store with vegan labels',ktype:'Store with a vegan category',task:'Your task: find one vegan product for each item:',vlist:'Vegan shopping list:',slist:'Shopping list:',offL:function(){return 'This product is not on your shopping list.';},close:'Close',notV:function(){return 'This product is not vegan.';},needAll:function(h,n){return 'Add all '+n+' items on your list to the cart first ('+h+' of '+n+' so far).';},
 filter:'Turn on the filter to see only vegan products.',
 label:'Vegan products have a “Vegan” label under the ingredient list on the product page.',
 category:'The “Plant-based” category has vegan milk and meat alternatives.',
 listP:'Buy one vegan product for each item:',go:'Go to the store',finish:'Checkout',finishedT:'Finished!',mist:'Mistakes',
 confirm:function(h,n){return 'You haven\'t found all the items on your list yet ('+h+' of '+n+' found). Are you sure you want to check out?';},keep:'Keep shopping',fin:'Checkout',
 q1:'How easy was it to find the items on your list?',q1a:'Very difficult',q1b:'Very easy',
 q2:'How sure are you that everything in your cart is vegan?',q2a:'Not sure at all',q2b:'Completely sure',
 next:'Continue',doneT:'Thank you!',doneP:'You have finished shopping. Now please answer a short survey.',doneB:'Continue to the survey',restart:'Restart',skip:'Skip store',restartQ:'Start the study again from the beginning?',
 bar:function(n){return 'Store '+n+' of 3 · Shopping list:';}},
zh:{introT:'网上购物研究',
 intro:['在本研究中，你将在一家网上超市购物三次。每一次，超市的功能都会略有不同。',
  '想象一位纯素食的朋友要来你家住几天。每次你会拿到一份简短的购物清单：请为清单上的每一项各选一件纯素商品加入购物车。纯素是指不含肉、鱼、奶制品、蛋或蜂蜜。点击商品即可查看配料表。',
  '四件商品都加入购物车后，购物会自动结束。每家店购物结束后有一个简单问题，最后还有一份简短问卷。全程约需 10–15 分钟。',
  '你的回答是匿名的。继续即表示你同意参加本研究。'],
 start:'开始',taskT:function(n){return '第 '+n+' 家店（共 3 家）';},
 control:'没有纯素工具：请在每件商品的详情页查看配料表。',ctype:'普通超市',ftype:'带纯素筛选的超市',ltype:'带纯素标签的超市',ktype:'带纯素分类的超市',task:'任务：为每一项找到一件纯素商品：',vlist:'纯素购物清单：',slist:'购物清单：',offL:function(){return '这件商品不在你的购物清单上。';},close:'关闭',notV:function(){return '这件商品不是纯素的。';},needAll:function(h,n){return '请先把清单上的全部 '+n+' 项加入购物车（目前 '+h+'/'+n+'）。';},
 filter:'打开筛选，只显示纯素商品。',
 label:'纯素商品的详情页上，配料表下方有“纯素”标签。',
 category:'“植物基”分类里有纯素的植物奶和植物肉。',
 listP:'请为每一项各买一件纯素商品：',go:'进入超市',finish:'结账',finishedT:'完成了！',mist:'错误',
 confirm:function(h,n){return '你还没有找到清单上的所有商品（已找到 '+n+' 项中的 '+h+' 项）。确定要结账吗？';},keep:'继续购物',fin:'结账',
 q1:'找到清单上的商品有多容易？',q1a:'非常困难',q1b:'非常容易',
 q2:'你有多确定购物车里的所有商品都是纯素的？',q2a:'完全不确定',q2b:'完全确定',
 next:'继续',doneT:'谢谢！',doneP:'购物已完成。接下来请填写一份简短问卷。',doneB:'前往问卷',restart:'重新开始',skip:'跳过本店',restartQ:'要从头重新开始吗？',
 bar:function(n){return '第 '+n+'/3 家店 · 购物清单：';}},
he:{introT:'מחקר קנייה אונליין',
 intro:['במחקר הזה תעשו קניות בסופרמרקט אונליין שלוש פעמים. בכל פעם החנות עובדת קצת אחרת.',
  'דמיינו שחבר טבעוני מגיע להתארח אצלכם. בכל פעם תקבלו רשימת קניות קצרה: הוסיפו לעגלה מוצר טבעוני אחד לכל פריט ברשימה. טבעוני פירושו ללא בשר, דגים, מוצרי חלב, ביצים או דבש. לחצו על מוצר כדי לראות את רשימת הרכיבים.',
  'כשכל ארבעת הפריטים יהיו בעגלה, הקנייה תסתיים אוטומטית. אחרי כל חנות תופיע שאלה קצרה אחת, ובסוף שאלון קצר. משך ההשתתפות כ-10–15 דקות.',
  'התשובות שלכם אנונימיות. המשך ההשתתפות מהווה הסכמה להשתתף במחקר.'],
 start:'התחלה',taskT:function(n){return 'חנות '+n+' מתוך 3';},
 control:'אין כלים טבעוניים: בדקו את רשימת הרכיבים בעמוד של כל מוצר.',ctype:'חנות רגילה',ftype:'חנות עם פילטר טבעוני',ltype:'חנות עם תוויות טבעוני',ktype:'חנות עם קטגוריה טבעונית',task:'המשימה: מצאו מוצר טבעוני אחד לכל פריט:',vlist:'רשימת קניות טבעונית:',slist:'רשימת קניות:',offL:function(){return 'המוצר הזה לא נמצא ברשימת הקניות.';},close:'סגירה',notV:function(){return 'המוצר הזה אינו טבעוני.';},needAll:function(h,n){return 'הוסיפו קודם לעגלה את כל '+n+' הפריטים ברשימה (עד כה '+h+' מתוך '+n+').';},
 filter:'הפעילו את הפילטר כדי לראות רק מוצרים טבעוניים.',
 label:'למוצרים טבעוניים יש תווית "טבעוני" מתחת לרשימת הרכיבים בעמוד המוצר.',
 category:'בקטגוריית "מבוסס צמחים" יש תחליפי חלב ובשר טבעוניים.',
 listP:'קנו מוצר טבעוני אחד לכל פריט:',go:'כניסה לחנות',finish:'לקופה',finishedT:'סיימתם!',mist:'טעויות',
 confirm:function(h,n){return 'עדיין לא מצאתם את כל הפריטים ברשימה (נמצאו '+h+' מתוך '+n+'). אתם בטוחים שאתם רוצים לעבור לקופה?';},keep:'המשך קנייה',fin:'לקופה',
 q1:'עד כמה היה קל למצוא את הפריטים ברשימה?',q1a:'קשה מאוד',q1b:'קל מאוד',
 q2:'עד כמה אתם בטוחים שכל המוצרים בעגלה טבעוניים?',q2a:'בכלל לא בטוח/ה',q2b:'בטוח/ה לגמרי',
 next:'המשך',doneT:'תודה!',doneP:'סיימתם את הקניות. עכשיו נשמח שתענו על שאלון קצר.',doneB:'מעבר לשאלון',restart:'התחלה מחדש',skip:'דילוג על החנות',restartQ:'להתחיל את המחקר מחדש מההתחלה?',
 bar:function(n){return 'חנות '+n+'/3 · רשימת קניות:';}}};
function st(k){var v=ST[lang][k];return v===undefined?ST.en[k]:v;}
function secIs(p,n){return p.s.en===n;}
var ITEMS={
 milk:{en:'<b>Vegan</b> milk',zh:'<b>纯素</b>牛奶',he:'חלב <b>טבעוני</b>',m:function(p){return secIs(p,'Milk');}},
 sausages:{en:'<b>Vegan</b> sausage',zh:'<b>纯素</b>香肠',he:'נקניק <b>טבעוני</b>',m:function(p){return secIs(p,'Sausages, Burgers & Deli')&&/sausage|dog|frank|link|brat|chorizo|kielbasa|andouille|wiener/i.test(p.b.en);}},
 bread:{en:'<b>Vegan</b> bread',zh:'<b>纯素</b>面包',he:'לחם <b>טבעוני</b>',m:function(p){return secIs(p,'Bread')||(p.d.k==='bakery'&&/\bpita\b|\bbread\b/i.test(p.b.en));}},
 chocolate:{en:'<b>Vegan</b> chocolate',zh:'<b>纯素</b>巧克力',he:'שוקולד <b>טבעוני</b>',m:function(p){return (secIs(p,'Candy, Gum & Mints')||secIs(p,'Baking'))&&/chocolate|cacao/i.test(p.b.en);}},
 yogurt:{en:'<b>Vegan</b> yogurt',zh:'<b>纯素</b>酸奶',he:'יוגורט <b>טבעוני</b>',m:function(p){return secIs(p,'Yogurt');}},
 burgers:{en:'<b>Vegan</b> burger',zh:'<b>纯素</b>汉堡肉饼',he:'המבורגר <b>טבעוני</b>',m:function(p){return /burger|patt(y|ies)/i.test(p.b.en)&&!/\bbuns?\b|helper/i.test(p.b.en);}},
 cookies:{en:'<b>Vegan</b> cookies',zh:'<b>纯素</b>曲奇饼干',he:'עוגיות <b>טבעוניות</b>',m:function(p){return secIs(p,'Cookies');}},
 cereal:{en:'<b>Vegan</b> cereal',zh:'<b>纯素</b>麦片',he:'דגני בוקר <b>טבעוניים</b>',m:function(p){return secIs(p,'Breakfast & Cereal');}},
 creamer:{en:'<b>Vegan</b> creamer',zh:'<b>纯素</b>奶精',he:'מלבין <b>טבעוני</b>',m:function(p){return /creamer/i.test(p.b.en);}},
 bacon:{en:'<b>Vegan</b> bacon',zh:'<b>纯素</b>培根',he:'בייקון <b>טבעוני</b>',m:function(p){return /bacon/i.test(p.b.en);}},
 crackers:{en:'<b>Vegan</b> crackers',zh:'<b>纯素</b>咸饼干',he:'קרקרים <b>טבעוניים</b>',m:function(p){return secIs(p,'Crackers');}},
 bars:{en:'<b>Vegan</b> granola bar',zh:'<b>纯素</b>燕麦棒',he:'חטיף גרנולה <b>טבעוני</b>',m:function(p){return secIs(p,'Bars');}}};
var TERMS={"milk": {"en": "milk", "zh": "牛奶", "he": "חלב"}, "sausages": {"en": "sausage", "zh": "香肠", "he": "נקניק"}, "bread": {"en": "bread", "zh": "面包", "he": "לחם"}, "chocolate": {"en": "chocolate", "zh": "巧克力", "he": "שוקולד"}, "yogurt": {"en": "yogurt", "zh": "酸奶", "he": "יוגורט"}, "burgers": {"en": "burger", "zh": "汉堡", "he": "המבורגר"}, "cookies": {"en": "cookie", "zh": "曲奇", "he": "עוגיות"}, "cereal": {"en": "cereal", "zh": "麦片", "he": "דגני בוקר"}, "creamer": {"en": "creamer", "zh": "奶精", "he": "מלבין"}, "bacon": {"en": "bacon", "zh": "培根", "he": "בייקון"}, "crackers": {"en": "cracker", "zh": "饼干", "he": "קרקרים"}, "bars": {"en": "granola bar", "zh": "燕麦棒", "he": "חטיף גרנולה"}};
var LISTS=[['milk','sausages','bread','chocolate'],['yogurt','burgers','cookies','cereal'],['creamer','bacon','crackers','bars']];
var TYPE={control:'ctype',filter:'ftype',label:'ltype',category:'ktype'};
var VK={control:'c',filter:'f',label:'a',category:'a'};
var SS=null,TASK=null,AUTO=null,TEST=false;
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
  TEST=qs.get('reset')==='1'||qs.get('test')==='1';
  if(qs.get('reset')==='1'){try{localStorage.removeItem('vf_study');}catch(e){}}
  try{SS=JSON.parse(localStorage.getItem('vf_study')||'null');}catch(e){SS=null;}
  if(!SS){var g=(qs.get('group')||'').toUpperCase();if(g!=='A'&&g!=='B')g=Math.random()<0.5?'A':'B';var alt=g==='A'?'label':'category';
    SS={pid:qs.get('pid')||qs.get('id')||('p'+Date.now().toString(36)+Math.random().toString(36).slice(2,6)),group:g,alt:alt,
        order:shuffle(['control','filter',alt]),lists:shuffle([0,1,2]),step:0,phase:'intro',res:{},t0:Date.now()};ssave();}
  if(SS.phase==='task'||SS.phase==='q')SS.phase='brief';
  applyVersion(curVer());
  studyRender();
}
function studyRender(){
  var box=$('#study'),bar=$('#taskbar'),h='';var rt=document.getElementById('restartT');if(rt)rt.textContent=st('skip');var rb=document.getElementById('restartBtn');if(rb)rb.style.display=(TEST&&SS.phase!=='intro'&&SS.phase!=='done')?'':'none';var ft=document.getElementById('finishT');if(ft)ft.textContent=st('finish');var fs=document.getElementById('finishS');if(fs)fs.textContent=st('fin');document.querySelectorAll('.finS2').forEach(function(e){e.textContent=st('fin');});document.documentElement.classList.add('intask');document.documentElement.classList.toggle('inshop',SS.phase==='task');
  if(true){
    var got=covered(false);
    bar.innerHTML='<div class="wrap tb"><div class="tb1"><span class="tbs">'+st('taskT')(SS.step+1)+'</span><span class="tbx"><b>'+st(TYPE[curVer()])+'</b> — '+st(curVer())+'</span>'+STATS()+'</div><div class="tb2"><span class="tbl"><span class="tbll">'+st('vlist')+'</span><span class="tbls">'+st('slist')+'</span></span>'+curList().map(function(k){var ok=got.indexOf(k)>=0;return '<button class="ti'+(ok?' ok':'')+'" data-act="slist" data-k="'+k+'">'+(ok?'✓ ':'')+L(ITEMS[k])+'</button>';}).join('')+STATS()+'</div></div>';
    bar.classList.add('show');if(SS.phase==='task'){box.classList.remove('show');return;}}
  var langSel='<div class="lang"><select class="langsel" onchange="setLang(this.value)">'+[['en','English'],['zh','中文'],['he','עברית']].map(function(o){return '<option value="'+o[0]+'"'+(lang===o[0]?' selected':'')+'>'+o[1]+'</option>';}).join('')+'</select></div>';
  if(SS.phase==='intro')h=langSel+'<h2>'+st('introT')+'</h2>'+st('intro').map(function(x){return '<p>'+x+'</p>';}).join('')+'<button class="cta" data-act="sgo" data-to="brief">'+st('start')+'</button>';
  else if(SS.phase==='brief')h=langSel+'<h2>'+st('taskT')(SS.step+1)+'</h2><div class="ver"><b>'+st(TYPE[curVer()])+'</b><br>'+st(curVer())+'</div><p>'+st('task')+'</p><ul>'+curList().map(function(k){return '<li>'+L(ITEMS[k])+'</li>';}).join('')+'</ul><button class="cta" data-act="sgo" data-to="task">'+st('go')+'</button>';
  else if(SS.phase==='confirm')h='<p style="font-size:16px;font-weight:600">'+st('confirm')(covered(true).length,curList().length)+'</p><div class="row2"><button class="cta ghost" data-act="sgo" data-to="task">'+st('keep')+'</button><button class="cta" data-act="sgo" data-to="q">'+st('fin')+'</button></div>';
  else if(SS.phase==='q'){var r=SS.res[VK[curVer()]]||{};
    var sc=function(key,qa,qb,q){return '<div class="q">'+st(q)+'</div><div class="scale">'+[1,2,3,4,5].map(function(n){return '<button data-act="sans" data-k="'+key+'" data-v="'+n+'" class="'+(r[key]===n?'on':'')+'">'+n+'</button>';}).join('')+'</div><div class="scl"><span>'+st(qa)+'</span><span>'+st(qb)+'</span></div>';};
    h='<h2>'+st('finishedT')+'</h2>'+sc('ease','q1a','q1b','q1')+'<button class="cta" data-act="snext"'+(r.ease?'':' disabled')+'>'+st('next')+'</button>';}
  else if(SS.phase==='done')h='<h2>'+st('doneT')+'</h2><p>'+st('doneP')+'</p><button class="cta" data-act="ssurvey">'+st('doneB')+'</button>';
  var was=box.classList.contains('show');box.innerHTML='<div class="sbox'+(was?' swap':'')+'">'+h+'</div>';
  if(!was)requestAnimationFrame(function(){requestAnimationFrame(function(){box.classList.add('show');});});
}
function startTask(){
  TASK={t0:Date.now(),clicks:0,pages:0,searches:0,feature:0,mistakes:0,offlist:0};SS.phase='task';ssave();studyRender();
  if(SS.step===0)setTimeout(introList,320);
  setTimeout(introTool,SS.step===0?900:320);
}
function introTool(){var v=curVer(),sel=v==='filter'?'.hrow .vegan, .mveg .vegan':v==='category'?'#deptbar a[data-k=plant], .depts a[href="#/c/plant"] i, .side>a[href="#/c/plant"]':'';if(!sel)return;
  document.querySelectorAll(sel).forEach(function(x){if(!x.offsetParent)return;x.classList.remove('tooli');void x.offsetWidth;x.classList.add('tooli');setTimeout(function(){x.classList.remove('tooli');},2500);});}
function introList(){var t=document.querySelector('.tb2');if(!t)return;t.classList.remove('intro');void t.offsetWidth;t.classList.add('intro');setTimeout(function(){t.classList.remove('intro');},2600);}
var errT;function hideErr(){clearTimeout(errT);$('#toast').classList.remove('show','err','warn');}
function errToast(m,kind){var e=$('#toast');e.innerHTML='<span class="tmsg"></span><button class="tx" data-act="tclose" aria-label="'+st('close')+'">✕</button>';e.firstChild.textContent=m;
  e.classList.remove('err','warn');e.classList.add('show',kind||'err');clearTimeout(errT);clearTimeout(toastT);errT=setTimeout(hideErr,kind==='warn'?4500:3500);}
function flashList(){var t=document.querySelector('.tb2');if(!t)return;t.classList.remove('flash');void t.offsetWidth;t.classList.add('flash');setTimeout(function(){t.classList.remove('flash');},1600);}
function onList(p){return curList().some(function(k){return ITEMS[k].m(p);});}
function studyFinish(){
  if(SS.phase!=='task')return;
  var h=covered(true).length,n=curList().length;if(REQUIRE_ALL&&h<n){toast(st('needAll')(h,n));return;}
  if(h<n){closeAll();SS.phase='confirm';studyRender();return;}
  endTask();
}
function endTask(){
  var ids=Object.keys(cart),k=VK[curVer()],o=SS.res[k]||{};
  o.list=SS.lists[SS.step]+1;o.pos=SS.step+1;
  if(TASK){o.time=Math.round((Date.now()-TASK.t0)/1000);o.clicks=TASK.clicks;o.pages=TASK.pages;o.search=TASK.searches;o.feature=TASK.feature;}
  o.items=ids.length;o.found=covered(true).length;o.nonvegan=TASK?TASK.mistakes:0;o.offlist=TASK?TASK.offlist:0;
  o.cart=ids.map(function(id){return DATA[id][0];}).join('-');
  hideErr();
  SS.res[k]=o;TASK=null;SS.phase='q';closeAll();ssave();studyRender();
}
function surveyUrl(){
  var q={pid:SS.pid,group:SS.group,alt:SS.alt,order:SS.order.map(function(v){return VK[v];}).join(''),lang:lang,total:SS.t0?Math.round(((SS.doneAt||Date.now())-SS.t0)/1000):''};
  ['c','f','a'].forEach(function(k){var o=SS.res[k]||{};['list','pos','time','clicks','pages','search','feature','items','found','nonvegan','offlist','ease','cart'].forEach(function(f){q[k+'_'+f]=o[f]===undefined?'':o[f];});});
  return SURVEY_URL+'?'+Object.keys(q).map(function(k){return k+'='+encodeURIComponent(q[k]);}).join('&');
}
document.addEventListener('click',function(e){
  if(!STUDY||!SS)return;
  if(TASK&&SS.phase==='task')TASK.clicks++;
  var el=e.target.closest('[data-act]');if(!el)return;var a=el.dataset.act;
  if(a==='slist'){e.stopImmediatePropagation();closeAll();location.hash='#/s/'+encodeURIComponent(L(TERMS[el.dataset.k]));return;}
  if(a==='tclose'){e.stopImmediatePropagation();hideErr();return;}
  if(a==='inc'&&SS.phase==='task'&&!cart[el.dataset.id]){var pr=PRODUCTS[el.dataset.id];
    if(!onList(pr)){e.stopImmediatePropagation();e.preventDefault();if(TASK)TASK.offlist++;errToast(st('offL')(pname(pr)),'warn');flashList();return;}
    if(!pr.v){e.stopImmediatePropagation();e.preventDefault();if(TASK)TASK.mistakes++;updStats();errToast(st('notV')(pname(pr)));return;}}
  if(a==='sgo'){var to=el.dataset.to;
    if(to==='task'){if(SS.phase==='confirm'){SS.phase='task';studyRender();}else startTask();}
    else if(to==='q')endTask();
    else{SS.phase=to;ssave();studyRender();}}
  else if(a==='sfinish')studyFinish();
  else if(a==='sans'){var r=SS.res[VK[curVer()]];r[el.dataset.k]=+el.dataset.v;ssave();
    el.parentNode.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===el);});var nb=document.querySelector('[data-act=snext]');if(nb)nb.disabled=!r.ease;}
  else if(a==='snext'){if(SS.step<2){SS.step++;SS.phase='brief';applyVersion(curVer());}else{SS.phase='done';SS.doneAt=Date.now();}ssave();studyRender();}
  else if(a==='sskip'){clearTimeout(AUTO);AUTO=null;TASK=null;hideErr();closeAll();var o=SS.res[VK[curVer()]]||{};o.skipped=1;SS.res[VK[curVer()]]=o;
    if(SS.step<2){SS.step++;SS.phase='brief';applyVersion(curVer());}else{SS.phase='done';SS.doneAt=Date.now();}ssave();studyRender();}
  else if(a==='srestart'){if(el.dataset.noask||confirm(st('restartQ'))){try{localStorage.removeItem('vf_study');}catch(e){}var u=new URLSearchParams(location.search);u.delete('reset');u.delete('group');var q=u.toString();location.href=location.pathname+(q?'?'+q:'')+'#/';setTimeout(function(){location.reload();},50);}}
  else if(a==='ssurvey'){(window.top||window).location.href=surveyUrl();}
},true);
if(true){
  var _op=openProduct;openProduct=function(id){if(STUDY&&TASK){TASK.pages++;if(LABELS&&PRODUCTS[id].v)TASK.feature++;}_op(id);};
  var _sv=setVegan;setVegan=function(on){if(STUDY&&TASK&&on&&curVer()==='filter')TASK.feature++;_sv(on);};
  var _sq=setQty;setQty=function(id,q){_sq(id,q);if(STUDY&&SS&&SS.phase==='task'){studyRender();if(covered(true).length>=curList().length&&!AUTO){AUTO=setTimeout(function(){AUTO=null;if(SS.phase==='task'&&covered(true).length>=curList().length){closeAll();endTask();}},900);}}};
  $('#searchForm').addEventListener('submit',function(){if(STUDY&&TASK)TASK.searches++;});
  window.addEventListener('hashchange',function(){if(STUDY&&TASK&&curVer()==='category'&&/^#\/c\/plant(\/|$)/.test(location.hash))TASK.feature++;});
}

/* ---------- translated names, ingredients and metric sizes (Chinese / Hebrew) ---------- */
function pname(p){var n=lang!=='en'&&TRD.n[lang]&&TRD.n[lang][p.oid];return n||p.b.en;}
function ingOf(p){var s=p.b.ingEn||'';var d=lang!=='en'&&TRD.i[lang];if(!d)return s;
  var out=s.split(/([,;.()\[\]{}:])/).map(function(t){if(/^[,;.()\[\]{}:]$/.test(t)){if(lang==='zh')return {',':'、',';':'；','.':'。','(':'（',')':'）','[':'【',']':'】','{':'（','}':'）',':':'：'}[t];return t;}
    var k=t.trim().toLowerCase().replace(/\s+/g,' ');if(!k)return t;var v=d[k];if(!v)return t;return (lang==='zh'?'':(/^\s/.test(t)?' ':''))+v;}).join('');
  return lang==='zh'?out.replace(/\s*([、；。（）【】：])\s*/g,'$1'):out;}
function sizeT(s){if(lang==='en'||!s)return s;
  var U=lang==='he'?{g:'גרם',kg:'ק"ג',ml:'מ"ל',l:'ליטר',pc:'יח\''}:{g:'g',kg:'kg',ml:'ml',l:'L',pc:'个'};
  var r=function(v){return (Math.round(v*10)/10).toString();};
  var fmt=function(v,u){if(u==='g'&&v>=1000)return r(v/1000)+' '+U.kg;if(u==='ml'&&v>=1000)return r(v/1000)+' '+U.l;return Math.round(v)+' '+U[u];};
  var pre='',m0=s.match(/^(\d+)\s*(?:-|x|×|ct\b)\s*(?=\d)/i);if(m0)pre=m0[1]+' × ';
  var m;
  if((m=s.match(/(\d+(?:\.\d+)?)\s*(kg|g|ml|lt|l)\b/i))){var u=m[2].toLowerCase(),v=parseFloat(m[1]);if(u==='kg')return pre+fmt(v*1000,'g');if(u==='lt'||u==='l')return pre+fmt(v*1000,'ml');return pre+fmt(v,u);}
  if((m=s.match(/(\d+(?:\.\d+)?)\s*fl\.?\s*oz/i)))return pre+fmt(parseFloat(m[1])*29.57,'ml');
  if((m=s.match(/(\d+(?:\.\d+)?)\s*(?:gl|gal)/i)))return pre+fmt(parseFloat(m[1])*3785,'ml');
  if((m=s.match(/(\d+(?:\.\d+)?)\s*qt/i)))return pre+fmt(parseFloat(m[1])*946,'ml');
  if((m=s.match(/(\d+(?:\.\d+)?)\s*pt\b/i)))return pre+fmt(parseFloat(m[1])*473,'ml');
  if((m=s.match(/(\d+(?:\.\d+)?)\s*oz/i)))return pre+fmt(parseFloat(m[1])*28.35,'g');
  if((m=s.match(/(\d+(?:\.\d+)?)\s*lbs?\b/i)))return pre+fmt(parseFloat(m[1])*453.6,'g');
  if((m=s.match(/^(\d+)\s*(?:each|ct|count|pk|pack|bags?)\b/i)))return m[1]+' '+U.pc;
  return s;}
function viewSearch(q){LEAD=5;
  // words must all match (AND); if nothing matches, any word may match (OR)
  var k=q.toLowerCase().trim();
  var words=k.replace(/(纯素|素食)/g,' $1 ').split(/\s+/).filter(Boolean);
  var syn=function(w){var out=[w];for(var tk in TERMS){var T_=TERMS[tk];if([T_.en,T_.zh,T_.he].some(function(x){return x.toLowerCase()===w;}))out.push(T_.en);}return out;};
  var hay=function(p){return (p.b.en+' '+pname(p)).toLowerCase();};
  var has=function(p,w){var h=hay(p);return syn(w).some(function(a){return h.indexOf(a)>=0;});};
  var all=PRODUCTS.filter(function(p){return has(p,k);});
  if(!all.length&&words.length>1)all=PRODUCTS.filter(function(p){return words.every(function(w){return has(p,w);});});
  if(!all.length&&words.length>1)all=PRODUCTS.filter(function(p){return words.some(function(w){return has(p,w);});});
  // Chinese has no spaces: fall back to 2-character pieces, then single characters
  if(!all.length&&/[\u4e00-\u9fff]/.test(k)){var cj=k.replace(/[^\u4e00-\u9fff]/g,''),bi=[];for(var i=0;i<cj.length-1;i++)bi.push(cj.substr(i,2));
    all=PRODUCTS.filter(function(p){var h=hay(p);return bi.some(function(w){return h.indexOf(w)>=0;});});
    if(!all.length)all=PRODUCTS.filter(function(p){var h=hay(p);return cj.split('').some(function(c){return h.indexOf(c)>=0;});});}
  return '<div class="crumb"><a href="#/">'+t('home')+'</a> › '+t('search')+'</div>'+listView(all,'<h1>'+esc(t('results')(q))+'</h1>','',null);
}

/* ---------- timer and mistake counter in the task bar ---------- */
function STATS(){return '<span class="tbst"><span class="tbt">⏱ <b class="tbTime">'+fmtT(statT())+'</b></span><span class="tbm">'+st('mist')+': <b class="tbMist">'+statM()+'</b></span></span>';}
function curRes(){return (SS&&SS.res[VK[curVer()]])||{};}
function statT(){if(TASK)return (Date.now()-TASK.t0)/1000;var o=curRes();return SS&&SS.phase==='brief'?0:(o.time||0);}
function statM(){if(TASK)return TASK.mistakes;var o=curRes();return SS&&SS.phase==='brief'?0:(o.nonvegan||0);}
function fmtT(s){s=Math.floor(s);return Math.floor(s/60)+':'+('0'+s%60).slice(-2);}
function updStats(){var tt=fmtT(statT()),m=String(statM());document.querySelectorAll('.tbTime').forEach(function(a){a.textContent=tt;});document.querySelectorAll('.tbMist').forEach(function(b){if(b.textContent!==m){b.textContent=m;var w=b.parentNode;w.classList.remove('bump');void w.offsetWidth;w.classList.add('bump');}});}
setInterval(function(){if(STUDY&&TASK)updStats();},500);
