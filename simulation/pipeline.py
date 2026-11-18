"""Synthetic-participant pilot: prompt building, survey input, answer validation.

  python3 pipeline.py task-prompts  <run_dir> P01 P02 ...   # write prompts/<pid>_task.md
  python3 pipeline.py survey-input  <run_dir> P01 ...       # write prompts/<pid>_survey_input.md + _survey.md
  python3 pipeline.py save-survey   <run_dir> P01 ...       # validate raw/<pid>.json -> synthetic_store/<pid>.json
"""
import json, os, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SHOP = os.path.join(HERE, "bin", "shop")
PERSONAS = {p["id"]: p for p in json.load(open(os.path.join(HERE, "personas.json")))}
ITEMS = json.load(open(os.path.join(HERE, "survey_items.json")))
VERSION_DESC = {"control": "Regular store (no vegan tools)", "filter": "Store with a vegan filter",
                "label": "Store with vegan labels", "category": "Store with a vegan category"}


def task_prompts(run, pids):
    os.makedirs(os.path.join(run, "prompts"), exist_ok=True)
    tpl = open(os.path.join(HERE, "prompts", "task_agent.md")).read()
    for pid in pids:
        txt = tpl.replace("{PROFILE}", PERSONAS[pid]["profile"]).replace("{SHOP}", SHOP).replace("{PID}", pid)
        open(os.path.join(run, "prompts", f"{pid}_task.md"), "w").write(txt)
        print(os.path.join(run, "prompts", f"{pid}_task.md"))


def load_log(run, pid):
    f = os.path.join(run, "logs", f"{pid}.jsonl")
    return [json.loads(l) for l in open(f)] if os.path.exists(f) else []


def summarize(run, pid):
    """A plain-language record of what this participant saw and did (their own log only)."""
    log = load_log(run, pid)
    out = json.load(open(os.path.join(run, "outcomes", f"{pid}.json"))) if os.path.exists(os.path.join(run, "outcomes", f"{pid}.json")) else {}
    lines = []
    cur = None
    for r in log:
        st = r.get("state") or {}
        store = st.get("store") or ((st.get("step") or 0) + 1 if "step" in st else None)
        if st.get("phase") == "task" and store != cur:
            cur = store
            lines.append(f"\nStore {store}: {VERSION_DESC.get(st.get('version'), st.get('version'))}")
        c = r.get("cmd")
        if c == "search":
            lines.append(f"  - You searched for \"{r.get('arg')}\".")
        elif c == "click" and r.get("target"):
            t = r["target"]
            if st.get("phase") == "task" or (r.get("toast")):
                lines.append(f"  - You clicked \"{t[:60]}\".")
        elif c in ("skip_store", "quit"):
            lines.append(f"  - You chose to {'skip this store' if c == 'skip_store' else 'leave the study'}.")
        if r.get("toast"):
            lines.append(f"    The site showed: \"{r['toast']}\"")
        if r.get("event") == "store_budget":
            lines.append("  - You ran out of time in this store and it was ended for you.")
    for s in out.get("stores", []):
        lines.append(f"\nResult in store {s['store_index']} ({VERSION_DESC.get(s['version'])}): "
                     f"{'you found all items' if s['outcome'] == 'completed' else 'you did not finish (' + s['outcome'].replace('_', ' ') + ')'}; "
                     f"{s.get('mistakes') or 0} non-vegan product(s) refused; about {s['steps']} actions.")
    p = (out.get("survey_params") or {})
    eases = {k: p.get(f"{k}_ease") for k in "cfa"}
    if any(eases.values()):
        lines.append("You rated how easy it was (1-5): " + ", ".join(f"{VERSION_DESC[{'c': 'control', 'f': 'filter', 'a': p.get('alt', 'label')}[k]]}: {v or 'no answer'}" for k, v in eases.items()))
    if out.get("ended_by") != "completed":
        lines.append(f"\nThe shopping part ended because: {out.get('ended_by', 'unknown').replace('_', ' ')}.")
    return "\n".join(lines).strip(), out


def resolve_items(alt):
    a = ITEMS["display_logic"]["alt_text"][alt or "label"]
    txt = json.dumps(ITEMS["items"], ensure_ascii=False).replace("{ALT_STORE}", a["store"]).replace("{ALT_TOOL}", a["tool"])
    items = json.loads(txt)
    asked = [i for i in items if not i.get("pilot_status")]
    return asked


def survey_input(run, pids):
    tpl = open(os.path.join(HERE, "prompts", "survey_agent.md")).read()
    os.makedirs(os.path.join(run, "raw"), exist_ok=True)
    for pid in pids:
        rec, out = summarize(run, pid)
        alt = (out.get("survey_params") or {}).get("alt") or ("label" if PERSONAS[pid]["group"] == "A" else "category")
        items = resolve_items(alt)
        q = []
        for i in items:
            s = f"{i['id']}. {i['text']}" + ("" if i.get("required") else " (optional)")
            if i["type"] in ("single", "rank"):
                s += "\n   Options: " + " | ".join(i["options"])
            if i["type"] == "grid":
                s += f"\n   Answer each row twice: \"filter\" = {i['columns'][0]}, \"alt\" = {i['columns'][1]}. Scale {i['scale'][0]}-{i['scale'][1]}."
                s += "".join(f"\n   {r['id']}. {r['text']}" for r in i["rows"])
            if i["type"] == "multi_scale":
                s += f"\n   ({i['anchors']})" + "".join(f"\n   {r['id']}. {r['text']}" for r in i["rows"])
            if i["type"] in ("scale", "slider"):
                s += f"\n   Scale {i['scale'][0]}-{i['scale'][1]} ({i.get('anchors', '')})"
            q.append(s)
        body = (f"# WHO YOU ARE\n{PERSONAS[pid]['profile']}\n\n# WHAT YOU SAW AND DID IN THE STUDY\n{rec}\n\n"
                f"# SURVEY QUESTIONS\n" + "\n\n".join(q) + "\n")
        fin = os.path.join(run, "prompts", f"{pid}_survey_input.md")
        open(fin, "w").write(body)
        prm = tpl.replace("{INPUT}", fin).replace("{OUTPUT}", os.path.join(run, "raw", f"{pid}.json"))
        open(os.path.join(run, "prompts", f"{pid}_survey.md"), "w").write(prm)
        print(os.path.join(run, "prompts", f"{pid}_survey.md"))


def validate(ans, items):
    """Return (clean answers, list of problems). Enforces types, ranges, required items and display logic."""
    probs, clean = [], {}
    for it in items:
        if it["type"] in ("grid", "multi_scale"):
            for r in it["rows"]:
                v = ans.get(r["id"], {})
                a = v.get("answer") if isinstance(v, dict) else v
                if it["type"] == "grid":
                    if a is None:
                        continue
                    for col in ("filter", "alt"):
                        x = (a or {}).get(col)
                        if x is not None and not (isinstance(x, (int, float)) and 1 <= x <= 5):
                            probs.append(f"{r['id']}.{col} out of range: {x}")
                elif a is not None and not (isinstance(a, (int, float)) and 1 <= a <= 5):
                    probs.append(f"{r['id']} out of range: {a}")
                clean[r["id"]] = {"answer": a, "reason": (v.get("reason") if isinstance(v, dict) else None)}
            continue
        v = ans.get(it["id"])
        a = v.get("answer") if isinstance(v, dict) else v
        if a in (None, "") and it.get("required"):
            probs.append(f"{it['id']} required but missing")
        if a not in (None, ""):
            if it["type"] == "single" and a not in it["options"]:
                probs.append(f"{it['id']} answer not an option: {a!r}")
            if it["type"] == "rank":
                if not isinstance(a, dict) or sorted(a.values()) != [1, 2, 3] or set(a) != set(it["options"]):
                    probs.append(f"{it['id']} not a valid ranking: {a!r}")
            if it["type"] in ("scale", "slider", "number"):
                lo, hi = it.get("scale", [1900, 2026])
                if not isinstance(a, (int, float)) or not lo <= a <= hi:
                    probs.append(f"{it['id']} out of range: {a!r}")
        clean[it["id"]] = {"answer": a, "reason": (v.get("reason") if isinstance(v, dict) else None)}
    extra = set(ans) - set(clean)
    if extra:
        probs.append(f"unexpected keys: {sorted(extra)}")
    return clean, probs


def save_survey(run, pids, model_label=None):
    os.makedirs(os.path.join(run, "synthetic_store"), exist_ok=True)
    for pid in pids:
        rawf = os.path.join(run, "raw", f"{pid}.json")
        outf = os.path.join(run, "outcomes", f"{pid}.json")
        out = json.load(open(outf)) if os.path.exists(outf) else {}
        alt = (out.get("survey_params") or {}).get("alt") or ("label" if PERSONAS[pid]["group"] == "A" else "category")
        try:
            ans = json.load(open(rawf))
        except Exception as e:
            print(pid, "INVALID JSON:", e)
            continue
        clean, probs = validate(ans, resolve_items(alt))
        rec = {"synthetic": True, "pid": pid, "saved_at": datetime.datetime.utcnow().isoformat() + "Z",
               "model": model_label or PERSONAS[pid]["model"], "hidden_fields": out.get("survey_params"),
               "answers": clean, "validation_problems": probs,
               "not_asked": [i["id"] + ": " + i["pilot_status"] for i in ITEMS["items"] if i.get("pilot_status")]}
        json.dump(rec, open(os.path.join(run, "synthetic_store", f"{pid}.json"), "w"), indent=1, ensure_ascii=False)
        print(pid, "saved", "problems:" if probs else "ok", probs or "")


if __name__ == "__main__":
    cmd, run, *pids = sys.argv[1:]
    run = os.path.abspath(run)
    {"task-prompts": task_prompts, "survey-input": survey_input, "save-survey": save_survey}[cmd](run, pids)
