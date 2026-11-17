# Regroup OSOG's US aisle layout into simpler departments.
DEPTS=[('meat','Meat, Seafood & Eggs','🥩',6,['Poultry','Red Meat','Sausages, Burgers & Deli','Seafood','Canned Meat & Fish','Eggs']),
 ('dairy','Milk & Dairy','🥛',214,['Milk','Yogurt','Cheese','Butter & Spreads','Cream','Dairy Desserts']),
 ('produce','Fruit & Veg','🥬',112,['Fresh Fruit','Fresh Vegetables','Fresh Herbs','Salads & Packaged Produce']),
 ('bakery','Bakery','🍞',34,['Bread','Buns & Rolls','Tortillas & Flatbread','Breakfast Bakery','Cakes & Desserts']),
 ('pantry','Pantry & Seasoning','🍚',44,['Pasta','Rice, Grains & Beans','Breakfast & Cereal','Baking','Spices','Oils & Vinegar','Sauces & Marinades','Condiments & Dressings','Spreads, Honey & Syrup','World Foods','Canned Vegetables & Beans','Canned Fruit']),
 ('instant','Instant & Frozen','🍜',18,['Instant Meals','Soups & Broth','Frozen Meals & Pizza','Frozen Fruit & Veg','Frozen Breakfast & Snacks','Ice Cream & Frozen Desserts']),
 ('snacks','Snacks','🍪',330,['Chips, Pretzels & Rice Cakes','Crackers','Cookies','Candy, Gum & Mints','Nuts & Dried Fruit','Popcorn','Bars','Dips & Salsa']),
 ('drinks','Drinks','🧃',262,['Water','Flavored & Sparkling Water','Soda','Juice','Bottled Tea','Sport & Energy Drinks','Coffee & Tea','Drink Mixes'])]
import re
MEATLIKE=re.compile(r"burger|sausage|dogs?\b|bacon|meatball|crumbles|strips|tenders|jerky|chick|nugget|patt(y|ies)|franks?|deli slices|ground",re.I)
def alt(x,fallback):
    n=x['name']
    if re.search(r"tofu|tempeh",n,re.I): return 'dairy','Cheese'
    if MEATLIKE.search(n): return 'meat','Sausages, Burgers & Deli'
    return fallback
def dairyfree(x):
    n=x['name'].lower()
    if re.match(r'(goya|iberia|madame|thai kitchen|native forest)',n): return 'pantry','World Foods'
    if 'yogurt' in n: return 'dairy','Yogurt'
    if 'creamer' in n or 'whip' in n: return 'dairy','Cream'
    if 'spread' in n or 'butter' in n or 'margarine' in n: return 'dairy','Butter & Spreads'
    if 'cheese' in n or 'shreds' in n or 'slices' in n: return 'dairy','Cheese'
    return 'dairy','Milk'
def newcat(x):
    c,s,ss=x['categoryId'],x['subcategoryOrder'],x['subsubcategoryOrder']
    nm=x['name'].lower()
    if 'creamer' in nm and c in ('2','4'): return 'dairy','Cream'
    if 'goodbelly' in nm: return 'drinks','Juice'
    if 'fig cake' in nm: return 'snacks','Nuts & Dried Fruit'
    if x.get('cls')=='n' and c in ('2','9') and re.search(r'burger|patt(y|ies)',nm) and not re.search(r'\bbuns?\b|helper',nm): return 'meat','Sausages, Burgers & Deli'
    k=(c,s); 
    if c=='1':
        if s=='5': return ('produce','Fresh Vegetables') if 'mushroom cap' in x['name'].lower() else alt(x,('produce','Salads & Packaged Produce'))
        if s=='3': return {'3':('snacks','Dips & Salsa'),'4':('drinks','Juice')}.get(ss,('produce','Salads & Packaged Produce'))
        return 'produce',{'1':'Fresh Fruit','2':'Fresh Vegetables','4':'Fresh Herbs'}[s]
    if c=='2':
        if s=='2': return 'meat',{'2':'Sausages, Burgers & Deli','3':'Seafood','4':'Poultry','5':'Red Meat'}.get(ss,'Sausages, Burgers & Deli')
        if ss=='9': return dairyfree(x)
        return {'1':('dairy','Cheese'),'2':('dairy','Yogurt'),'3':('dairy','Milk'),'4':('dairy','Cream'),'6':('meat','Eggs'),'7':('dairy','Butter & Spreads'),'8':('dairy','Butter & Spreads'),'9':('dairy','Plant Milk & Dairy-Free'),'10':('dairy','Dairy Desserts')}[ss]
    if c=='3':
        if s=='1': return 'bakery',{'1':'Bread','2':'Tortillas & Flatbread','3':'Buns & Rolls','4':'Breakfast Bakery','5':'Cakes & Desserts'}[ss]
        return 'pantry','Pasta' if ss=='1' else 'Rice, Grains & Beans'
    if c=='4':
        if s=='1': return 'drinks','Coffee & Tea'
        if s=='2': return ('snacks','Bars') if ss=='4' else ('pantry','Breakfast & Cereal')
        return {'3':('pantry','Spices'),'4':('pantry','Rice, Grains & Beans'),'5':('pantry','Baking'),'6':('instant','Instant Meals'),'7':('pantry','Baking')}[s]
    if c=='5':
        if s=='1': return 'pantry',{'2':'Condiments & Dressings','4':'Condiments & Dressings'}.get(ss,'Spreads, Honey & Syrup')
        return 'pantry',{'2':'Condiments & Dressings','3':'Condiments & Dressings','4':'World Foods','5':'Sauces & Marinades','6':'Oils & Vinegar','7':'Baking'}[s]
    if c=='6': return {'1':('meat','Canned Meat & Fish'),'2':('pantry','Canned Vegetables & Beans'),'3':('instant','Soups & Broth'),'4':('pantry','Canned Fruit')}[s]
    if c=='7': return 'snacks',{'1':'Crackers','2':'Candy, Gum & Mints','3':'Cookies','4':'Chips, Pretzels & Rice Cakes','5':'Nuts & Dried Fruit','6':'Popcorn','7':'Dips & Salsa'}[s]
    if c=='8': return 'drinks',{'1':'Bottled Tea','2':'Sport & Energy Drinks','3':'Flavored & Sparkling Water','4':'Juice','5':'Drink Mixes','6':'Soda','7':'Sport & Energy Drinks','8':'Water'}[s]
    if c=='9':
        if s=='1': return 'bakery','Bread'
        if s=='3': return 'meat','Seafood'
        if s=='4': return alt(x,('instant','Frozen Meals & Pizza')) if ss=='6' else ('instant','Frozen Meals & Pizza')
        return 'instant',{'2':'Frozen Breakfast & Snacks','5':'Frozen Fruit & Veg','6':'Frozen Fruit & Veg','7':'Frozen Fruit & Veg','8':'Frozen Breakfast & Snacks','9':'Ice Cream & Frozen Desserts'}[s]

# names in Chinese and Hebrew
TR={'Meat, Seafood & Eggs':('肉类、海鲜和蛋','בשר, דגים וביצים'),'Poultry':('禽肉','עוף'),'Red Meat':('红肉','בשר אדום'),
'Sausages, Burgers & Deli':('香肠、汉堡肉饼和熟食','נקניקים, המבורגרים ומעדנייה'),'Seafood':('海鲜','דגים ופירות ים'),'Canned Meat & Fish':('肉类和鱼类罐头','שימורי בשר ודגים'),'Eggs':('鸡蛋','ביצים'),
'Milk & Dairy':('牛奶和乳制品','חלב ומוצרי חלב'),'Milk':('牛奶','חלב'),'Yogurt':('酸奶','יוגורט'),'Cheese':('奶酪','גבינות'),'Butter & Spreads':('黄油和涂抹酱','חמאה וממרחים'),'Cream':('奶油和奶精','שמנת ומלבינים'),'Dairy Desserts':('乳制甜点','קינוחי חלב'),
'Fruit & Veg':('蔬菜水果','פירות וירקות'),'Fresh Fruit':('新鲜水果','פירות טריים'),'Fresh Vegetables':('新鲜蔬菜','ירקות טריים'),'Fresh Herbs':('新鲜香草','עשבי תיבול'),'Salads & Packaged Produce':('沙拉和包装蔬果','סלטים ותוצרת ארוזה'),
'Bakery':('面包烘焙','מאפייה'),'Bread':('面包','לחם'),'Buns & Rolls':('小面包','לחמניות'),'Tortillas & Flatbread':('薄饼','טורטיות ופיתות'),'Breakfast Bakery':('早餐烘焙','מאפי בוקר'),'Cakes & Desserts':('蛋糕甜点','עוגות וקינוחים'),
'Pantry & Seasoning':('粮油调味','מזווה ותבלינים'),'Pasta':('意大利面','פסטה'),'Rice, Grains & Beans':('米、谷物和豆类','אורז, דגנים וקטניות'),'Breakfast & Cereal':('早餐和麦片','ארוחת בוקר ודגני בוקר'),'Baking':('烘焙原料','אפייה'),'Spices':('香料','תבלינים'),'Oils & Vinegar':('油和醋','שמנים וחומץ'),'Sauces & Marinades':('酱汁和腌料','רטבים ומרינדות'),'Condiments & Dressings':('调味品和沙拉酱','רטבים ותוספות טעם'),'Spreads, Honey & Syrup':('涂抹酱、蜂蜜和糖浆','ממרחים, דבש וסירופ'),'World Foods':('世界美食','מטבחי העולם'),'Canned Vegetables & Beans':('蔬菜和豆类罐头','שימורי ירקות וקטניות'),'Canned Fruit':('水果罐头','שימורי פירות'),
'Instant & Frozen':('方便速食和冷冻','מוכנים וקפואים'),'Instant Meals':('方便餐','ארוחות מהירות הכנה'),'Soups & Broth':('汤和高汤','מרקים'),'Frozen Meals & Pizza':('冷冻餐和比萨','ארוחות קפואות ופיצה'),'Frozen Fruit & Veg':('冷冻蔬果','פירות וירקות קפואים'),'Frozen Breakfast & Snacks':('冷冻早餐和小吃','ארוחות בוקר וחטיפים קפואים'),'Ice Cream & Frozen Desserts':('冰淇淋和冷冻甜点','גלידות וקינוחים קפואים'),
'Snacks':('休闲零食','חטיפים'),'Chips, Pretzels & Rice Cakes':('薯片、椒盐卷饼和米饼','צ\'יפס, בייגלה ופריכיות'),'Crackers':('咸饼干','קרקרים'),'Cookies':('曲奇饼干','עוגיות'),'Candy, Gum & Mints':('糖果和口香糖','ממתקים ומסטיקים'),'Nuts & Dried Fruit':('坚果和果干','אגוזים ופירות יבשים'),'Popcorn':('爆米花','פופקורן'),'Bars':('谷物棒','חטיפי דגנים'),'Dips & Salsa':('蘸酱和莎莎酱','מטבלים וסלסה'),
'Drinks':('酒水饮料','משקאות'),'Water':('饮用水','מים'),'Flavored & Sparkling Water':('风味水和气泡水','מים בטעמים ומוגזים'),'Soda':('汽水','משקאות מוגזים'),'Juice':('果汁','מיצים'),'Bottled Tea':('瓶装茶','תה בבקבוק'),'Sport & Energy Drinks':('运动和能量饮料','משקאות ספורט ואנרגיה'),'Coffee & Tea':('咖啡和茶','קפה ותה'),'Drink Mixes':('冲饮','אבקות לשתייה')}
