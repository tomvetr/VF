import csv,collections,re,json,hashlib
csv.field_size_limit(10**9)
R='/home/user/open-science-online-grocery/online-grocery/db/seeds/base/'
cats=list(csv.reader(open(R+'categories.csv',encoding='latin-1')))[1:]
CN={};SN={}
for c in cats:
    CN[c[0]]=c[1];SN[(c[0],c[2])]=c[3]
rows=list(csv.DictReader(open(R+'products.csv',encoding='utf8',errors='replace')))
PLANT=r"(coconut|almond|soy|soya|oat|rice|cashew|hemp|pea|flax|macadamia|hazelnut|walnut|peanut|cocoa|cacao|shea|nut|seed|sunflower|apple|pumpkin|mango|sesame|pecan|pistachio)"
NV=r"\b(milk|milkfat|buttermilk|cream|butter|butterfat|whey|casein|caseinate|caseinates|lactose|lactalbumin|cheese|cheeses|yogurt|yoghurt|ghee|egg|eggs|albumen|albumin|honey|gelatin|gelatine|beef|pork|chicken|turkey|bacon|ham|lamb|veal|meat|sausage|pepperoni|salami|fish|anchovy|anchovies|tuna|salmon|cod|shrimp|crab|clam|clams|oyster|oysters|lobster|scallop|scallops|lard|tallow|suet|carmine|cochineal|shellac|beeswax|lanolin|isinglass|collagen|bonito|duck|venison|prosciutto|chorizo|sardines|mackerel|tilapia|pollock|squid|mussels|krill|rennet|parmesan|cheddar|mozzarella|romano|sour cream|half and half)\b"
AMB=r"(mono-? ?(and|&|-)? ?di-?glycerides|monoglycerides|diglycerides|\benzymes?\b|stearic|stearate|stearoyl|vitamin d\b|vitamin d3|cholecalciferol|l-cysteine|cysteine|omega-3|confectioner'?s glaze|resinous glaze|glycerin|glycerol|lactic acid esters|natural flavou?rs?|artificial flavou?rs?|\bsugar\b|bone char|lactylate|polysorbate|datem)"
STRICT_AMB=r"(mono-? ?(and|&|-)? ?di-?glycerides|monoglycerides|diglycerides|\benzymes?\b|stearic|stearate|stearoyl|vitamin d\b|vitamin d3|cholecalciferol|l-cysteine|cysteine|omega-3|confectioner'?s glaze|resinous glaze|lactylate|polysorbate|datem|glycerin)"
def clean(t):
    t=t.lower()
    t=re.sub(r"(may contain|manufactured (in|on)|made (in|on) (a|shared|equipment)|processed (in|on)|produced (in|on)|packaged (in|on)|packed (in|on)|facility|shared equipment)[^.]*\.?"," ",t)
    t=re.sub(PLANT+r"[\s-]*(milk|butter|cream|meat|cheese|yogurt)"," plantx ",t)
    t=re.sub(r"cream of tartar|creamed|non-?dairy|dairy-?free|egg-?free|milk-?free|meatless|eggplant|butternut|butterhead|butter beans?|butter lettuce|milk thistle|cream soda flavor"," ",t)
    return t
def classify(x):
    ing=x['ingredients'].strip(); c=x['categoryId']; sub=x['subcategoryOrder']
    if ing in('','NULL'):
        if c=='1' and sub in('1','2','4'): return 'v'
        if c=='2': return 'n'
        return '?'
    t=clean(ing)
    if re.search(NV,t): return 'n'
    if re.search(STRICT_AMB,t): return '?'
    return 'v'
def hk(x): return int(hashlib.md5(x['id'].encode()).hexdigest()[:8],16)
for x in rows:
    x['cls']=classify(x); x['h']=hk(x)
if __name__=='__main__':
    by=collections.defaultdict(collections.Counter)
    for x in rows: by[x['categoryId']][x['cls']]+=1
    for c in sorted(by): print(c,CN[c],dict(by[c]))
    import random; random.seed(3)
    for cls in 'vn':
        print('=====',cls)
        for x in random.sample([x for x in rows if x['cls']==cls and x['ingredients'].strip() not in('','NULL')],14):
            print('-',x['name'],'|',x['ingredients'][:170].replace('\n',' '))
