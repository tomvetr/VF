"""Generate synthetic persona profiles from the explicit distributions in config.json.

Usage: python3 personas.py [--n N] [--out personas.json]
"""
import json, random, argparse, os
HERE = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(HERE, "config.json")))

def draw(rng, dist):
    r, acc = rng.random(), 0.0
    for k, p in dist.items():
        acc += p
        if r < acc:
            return k
    return list(dist)[-1]

AGE_RANGE = {"18-24": (18, 24), "25-34": (25, 34), "35-49": (35, 49), "50-64": (50, 64), "65+": (65, 78)}
LIT = {"low": "I'm not very comfortable with websites and apps. I read slowly, I don't always know what icons mean, and I usually don't notice small buttons or menus.",
       "medium": "I use websites and apps every day, but I don't explore features unless I need them.",
       "high": "I'm very comfortable online. I scan pages quickly, use search and filters, and try buttons to see what they do."}
PAT = {"low": "I'm impatient. If something takes too long or is confusing I get annoyed and give up quickly.",
       "medium": "I'm reasonably patient, but I don't like wasting time.",
       "high": "I'm patient and careful. I'd rather read the details than make a mistake."}
DIET = {"omnivore": "I eat meat and dairy and don't think much about it.",
        "flexitarian": "I eat meat, but less than I used to.",
        "vegetarian": "I don't eat meat or fish, but I eat eggs and dairy.",
        "vegan": "I'm vegan: no meat, fish, dairy, eggs or honey.",
        "other": "I follow my own mix of diet rules (I avoid some foods for personal reasons)."}
MOT = {"I am vegan myself": "A vegan filter would matter to me because I check labels every time I shop.",
       "I cook for a vegan friend or family member": "Someone close to me is vegan, so I sometimes have to shop vegan for them and find it hard.",
       "curious, might try eating less meat": "I'm curious about eating more plant-based food, but I don't know much about it.",
       "health reasons": "I'm interested in plant-based products mainly for health reasons.",
       "skeptical, no real interest": "Honestly, I'm skeptical about vegan products and don't see why a supermarket needs special features for them."}
FREQ = {"never": "I have never bought groceries online.", "less than once a month": "I buy groceries online occasionally, less than once a month.",
        "1-3 times a month": "I buy groceries online a few times a month.", "once a week or more": "I buy groceries online every week."}
LANGN = {"en": "English", "zh": "Chinese (Mandarin)", "he": "Hebrew"}
DEV = {"phone": "I'm doing this on my phone.", "desktop": "I'm doing this on my laptop."}
# What this person knows about ingredients, and how carefully they read (makes agents less "perfect")
def knowledge(p):
    if p["diet"] == "vegan":
        return "I know the hidden animal ingredients, like whey, casein, gelatin, albumin, carmine and lard."
    if p["filter_motivation"] == "I cook for a vegan friend or family member":
        return "My friend told me the basics (no meat, fish, dairy, eggs or honey), but I don't recognise ingredient names like whey, casein or albumin."
    if p["diet"] == "vegetarian":
        return "I know meat, fish, milk and eggs aren't vegan, but I'm not sure about ingredients like whey, casein, gelatin or albumin, or whether honey counts."
    return "I only know the obvious things: meat, fish, milk and eggs. Words like whey, casein, gelatin or albumin don't mean anything to me, and I'm not sure whether honey counts."
def reading(p):
    if p["digital_literacy"] == "low" or p["patience"] == "low":
        return "I usually go by a product's name and picture, and at most glance at the first few ingredients. I often miss small print and sometimes tap the wrong thing."
    if p["patience"] == "high" and p["digital_literacy"] == "high":
        return "I read ingredient lists carefully, but I can still misread or overlook something."
    return "I read the start of an ingredient list, not every word, and sometimes I miss things."

def make(n, seed):
    rng = random.Random(seed)
    D = cfg["distributions"]
    ps = []
    for i in range(n):
        p = {k: draw(rng, D[k]) for k in ["diet", "age_band", "digital_literacy", "online_grocery_frequency", "filter_motivation", "patience", "device", "language", "gender"]}
        # keep diet and motivation coherent: only vegans say "I am vegan myself", and vegans aren't skeptical
        if p["diet"] == "vegan":
            p["filter_motivation"] = "I am vegan myself"
        elif p["filter_motivation"] == "I am vegan myself":
            while p["filter_motivation"] == "I am vegan myself":
                p["filter_motivation"] = draw(rng, D["filter_motivation"])
        lo, hi = AGE_RANGE[p["age_band"]]
        p["age"] = rng.randint(lo, hi)
        p["birth_year"] = 2026 - p["age"]
        ps.append(p)
    # enforce minimum counts for hard-to-serve personas (overwrite random others)
    for rule, m in cfg["minimum_counts"].items():
        key, val = rule.split("=", 1)
        have = [p for p in ps if p[key] == val]
        others = [p for p in ps if p[key] != val and p["diet"] != "vegan"]
        rng.shuffle(others)
        for p in others[: max(0, m - len(have))]:
            p[key] = val
    n_sec = round(n * cfg["models"]["secondary_share"])
    sec_idx = set(rng.sample(range(n), n_sec))
    out = []
    for i, p in enumerate(ps):
        pid = "P%02d" % (i + 1)
        p["id"] = pid
        p["group"] = "A" if i % 2 == 0 else "B"
        p["model"] = "secondary" if i in sec_idx else "primary"
        p["profile"] = " ".join([
            f"I'm a {p['age']}-year-old {p['gender']}. My first language is {LANGN[p['language']]}.",
            DIET[p["diet"]], MOT[p["filter_motivation"]], FREQ[p["online_grocery_frequency"]],
            LIT[p["digital_literacy"]], PAT[p["patience"]], knowledge(p), reading(p), DEV[p["device"]]])
        out.append(p)
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=cfg["n_personas"])
    ap.add_argument("--out", default=os.path.join(HERE, "personas.json"))
    a = ap.parse_args()
    ps = make(a.n, cfg["seed"])
    json.dump(ps, open(a.out, "w"), indent=1, ensure_ascii=False)
    print(f"wrote {len(ps)} personas to {a.out}")
