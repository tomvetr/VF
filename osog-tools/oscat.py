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
