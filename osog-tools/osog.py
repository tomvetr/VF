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
    t=re.sub(r"cream of tartar|creamed|oyster mushrooms?|oyster crackers?|chicken of the woods|hen of the woods|duck sauce|non-?dairy|dairy-?free|egg-?free|milk-?free|meatless|eggplant|butternut|butterhead|butter beans?|butter lettuce|milk thistle|cream soda flavor"," ",t)
    return t
MARK=r"(vegan|plant[- ]based|dairy[- ]free|non[- ]?dairy|meatless|meat[- ]free|veggie|vegetarian|soy|almond|coconut|cashew|oat|rice|tofu|chik|chick'n|imitation|flavou?r)"
NAMENV=NV[:-3]+r"|hot dogs?|franks?|wieners?|jerky|steaks?|ribs?|wings?|burgers?|meatballs?|bologna|pastrami|bratwurst|kielbasa|liverwurst|spam|pate|caviar|herring|trout|catfish|flounder|haddock|halibut|sole|mahi|swordfish|calamari|crawfish|ice cream|gelato|custard|pudding|mayo|mayonnaise|ranch|alfredo|caesar|marshmallows?|jell-?o|nougat|caramel|toffee|fudge|latte|cappuccino|mocha|creamer|queso|feta|brie|gouda|provolone|ricotta|swiss|colby|jack|asiago|gorgonzola|cream cheese|cottage|kefir|eggnog|quiche|omelet|frittata)\b"
def classify(x):
    ing=x['ingredients'].strip(); c=x['categoryId']; sub=x['subcategoryOrder']; ss=x['subsubcategoryOrder']
    name=clean(x['name']+' '+x.get('description','')[:0]); marker=re.search(MARK,x['name'].lower())
    if ing in('','NULL'):
        if c=='1' and sub in('1','2','4'): return 'v'
        return '?'
    t=clean(ing)
    if x['id'] in ('13342',): return '?'
    if re.search(r"caution|not for use|do not feed|not suitable|warning|keep refrigerated|directions|www\.|call 1-",ing.lower()): return '?'
    if re.search(NV,t): return 'n'
    if re.search(r"crabmeat|lunchmeat|nutmeat",t): return '?'
    if (c=='2' and sub=='2') or (c=='6' and sub=='1') or (c=='9' and sub=='3'): return '?'   # animal product whose listed ingredients omit the animal part
    if re.search(r"caution|not for use|warning|keep refrigerated|directions|www\.|call 1-",ing.lower()) or (',' not in ing and len(ing)>60): return '?'
    if re.search(r"glycerol|gum base",t): return '?'
    if re.search(STRICT_AMB,t): return '?'
    if len(ing)<25 and c!='1' and ',' not in ing and not marker: pass
    if re.search(NAMENV,name):
        if (c=='6' and sub=='1') or (c=='9' and sub=='3'): return 'n'
        return '?'
    if c=='2' and sub=='1' and ss!='9' and not marker: return '?'
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
