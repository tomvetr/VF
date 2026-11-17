# Study adjustments on top of osel.py's selection: make the shopping-list items hard to find without the filter.
import sys,os,json,io,re,urllib.request,concurrent.futures as cf
S=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,S+'/pylib'); sys.path.insert(0,S)
from PIL import Image
import osog,oscat
OUT='/home/user/VF/osog-images'
sel=set(json.load(open(S+'/ossel.json'))); bad=set(json.load(open(S+'/osbad.json')))
R={x['id']:x for x in osog.rows}
for x in osog.rows: x['sec']=oscat.newcat(x)
def cur(f): return sorted([R[i] for i in sel if f(R[i])],key=lambda x:x['h'])
def cand(f): return sorted([x for x in osog.rows if x['id'] not in sel and x['id'] not in bad and x['cls'] in 'vn' and x['name'].strip() and f(x)],key=lambda x:x['h'])
def keep(f,n,prefer=None):
    c=cur(f)
    if prefer: c=sorted(c,key=lambda x:(min([i for i,k in enumerate(prefer) if k in x['name'].lower()] or [99]),x['h']))
    for x in c[n:]: sel.discard(x['id'])
def fill(f,n):
    have=len(cur(f))
    for x in cand(f)[:max(0,n-have)]: sel.add(x['id'])
sec=lambda d,s: (lambda x:x['sec']==(d,s))
V=lambda f:(lambda x:x['cls']=='v' and f(x)); N=lambda f:(lambda x:x['cls']=='n' and f(x))
burger=lambda x:x['sec'][1]=='Sausages, Burgers & Deli' and re.search(r'burger|patt(y|ies)',x['name'].lower())
keep(V(sec('dairy','Milk')),8,['silk soymilk','almond breeze','silk almond','oat','rice dream','so delicious','soy dream','hemp'])
fill(N(sec('dairy','Milk')),40)
keep(V(burger),3); fill(N(burger),12)
keep(V(sec('bakery','Bread')),4); fill(N(sec('bakery','Bread')),25)
fill(N(sec('snacks','Crackers')),17)
fill(V(sec('dairy','Yogurt')),2)
# back to 1,000 products and about 27% vegan
VT=270
nv=sum(1 for i in sel if R[i]['cls']=='v')
big=lambda x:x['sec'] in [('pantry','World Foods'),('instant','Soups & Broth'),('snacks','Candy, Gum & Mints'),('instant','Ice Cream & Frozen Desserts'),('instant','Instant Meals'),('pantry','Condiments & Dressings')]
if nv<VT:
    for x in cand(lambda x:x['cls']=='v' and x['sec'][0] in ('pantry','drinks','snacks') and x['sec'][1] not in ('Crackers','Cookies','Bars'))[:VT-nv]: sel.add(x['id'])
over=len(sel)-1000
for x in cur(N(big))[::-1][:max(0,over)]: sel.discard(x['id'])
def fetch(x):
    dst=f"{OUT}/{x['id']}.jpg"
    if os.path.exists(dst): return True
    try:
        d=urllib.request.urlopen(urllib.request.Request(x['awsImageUrl'],headers={'User-Agent':'research-demo/1.0'}),timeout=30).read()
        im=Image.open(io.BytesIO(d))
        if min(im.size)<150: return False
        im=im.convert('RGBA'); bg=Image.new('RGBA',im.size,'white'); bg.alpha_composite(im); im=bg.convert('RGB')
        w,h=im.size; m=max(w,h); sq=Image.new('RGB',(m,m),'white'); sq.paste(im,((m-w)//2,(m-h)//2))
        sq.resize((360,360),Image.LANCZOS).save(dst,quality=78,optimize=True); return True
    except Exception: return False
todo=[R[i] for i in sel if not os.path.exists(f"{OUT}/{i}.jpg")]
with cf.ThreadPoolExecutor(6) as ex: ok=list(ex.map(fetch,todo))
for x,o in zip(todo,ok):
    if not o: sel.discard(x['id']); bad.add(x['id'])
json.dump(sorted(bad),open(S+'/osbad.json','w'))
for f in os.listdir(OUT):
    if f[:-4] not in sel: os.remove(f"{OUT}/{f}")
json.dump(sorted(sel),open(S+'/ossel.json','w'))
print('total',len(sel),'vegan',sum(1 for i in sel if R[i]['cls']=='v'),'new images',len(todo),'failed',ok.count(False))
