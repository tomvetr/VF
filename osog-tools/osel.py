import sys,os,json,collections,io,time,urllib.request,concurrent.futures as cf
S=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,S+'/pylib'); sys.path.insert(0,S)
from PIL import Image
import osog
Q={'1':(60,15),'2':(45,145),'3':(28,82),'4':(32,98),'5':(32,88),'6':(26,74),'7':(30,95),'8':(20,30),'9':(30,70)}
PRIOR={'1':(lambda x:x['subcategoryOrder']=='5',12),'3':(lambda x:x['subcategoryOrder']=='1' and x['subsubcategoryOrder'] in('1','2','3'),16),'9':(lambda x:x['subcategoryOrder']=='4' and x['subsubcategoryOrder']=='6',15)}
OUT='/home/user/VF/osog-images'
badf=S+'/osbad.json'; bad=set(json.load(open(badf))) if os.path.exists(badf) else set()
def fetch(x):
    dst=f"{OUT}/{x['id']}.jpg"
    if os.path.exists(dst): return True
    try:
        d=urllib.request.urlopen(urllib.request.Request(x['awsImageUrl'],headers={'User-Agent':'research-demo/1.0'}),timeout=30).read()
        im=Image.open(io.BytesIO(d)); 
        if min(im.size)<150: raise Exception('small')
        im=im.convert('RGBA'); bg=Image.new('RGBA',im.size,'white'); bg.alpha_composite(im); im=bg.convert('RGB')
        w,h=im.size; m=max(w,h); sq=Image.new('RGB',(m,m),'white'); sq.paste(im,((m-w)//2,(m-h)//2))
        sq.resize((360,360),Image.LANCZOS).save(dst,quality=78,optimize=True); return True
    except Exception as e:
        return False
def pick():
    sel=[]
    for c,(nv,nn) in Q.items():
        for cls,n in (('v',nv),('n',nn)):
            pool=[x for x in osog.rows if x['categoryId']==c and x['cls']==cls and x['id'] not in bad and x['name'].strip()]
            if cls=='v' and c in PRIOR:
                f,cap=PRIOR[c]; pr=sorted([x for x in pool if f(x)],key=lambda x:x['h'])[:cap]
                sel+=pr; n-=len(pr); pool=[x for x in pool if not f(x)]
            g=collections.defaultdict(list)
            for x in pool: g[(x['subcategoryOrder'],x['subsubcategoryOrder'])].append(x)
            for k in g: g[k].sort(key=lambda x:x['h'])
            tot=len(pool); n=min(n,tot)
            quota={k:n*len(v)/tot for k,v in g.items()}
            base={k:min(len(g[k]),max(1 if n>=len(g) else 0,int(q))) for k,q in quota.items()}
            ks=sorted(g,key=lambda k:-(quota[k]-int(quota[k])))
            i=0
            while sum(base.values())<n:
                k=ks[i%len(ks)]; i+=1
                if base[k]<len(g[k]): base[k]+=1
            while sum(base.values())>n:
                k=max(base,key=lambda k:base[k]); base[k]-=1
            for k in g: sel+=g[k][:base[k]]
    return sel
for rnd in range(8):
    sel=pick(); todo=[x for x in sel if not os.path.exists(f"{OUT}/{x['id']}.jpg")]
    if not todo: break
    with cf.ThreadPoolExecutor(6) as ex: res=list(ex.map(fetch,todo))
    nb=[x['id'] for x,ok in zip(todo,res) if not ok]; bad|=set(nb); json.dump(sorted(bad),open(badf,'w'))
    print('round',rnd,'fetched',len(todo)-len(nb),'bad',len(nb),flush=True)
sel=pick(); keep={x['id'] for x in sel}
for f in os.listdir(OUT):
    if f[:-4] not in keep: os.remove(f"{OUT}/{f}")
json.dump([x['id'] for x in sel],open(S+'/ossel.json','w'))
print(len(sel),sum(x['cls']=='v' for x in sel),len(os.listdir(OUT)))
