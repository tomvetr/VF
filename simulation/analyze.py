"""Analysis pipeline for the synthetic pilot (also the pipeline to reuse on real data).

  python3 analyze.py <run_dir>
Writes <run_dir>/report/*.csv and report_auto.md.
"""
import json, os, sys, csv, glob, statistics as st, collections, re

HERE = os.path.dirname(os.path.abspath(__file__))
run = os.path.abspath(sys.argv[1])
rep = os.path.join(run, "report"); os.makedirs(rep, exist_ok=True)
P = {p["id"]: p for p in json.load(open(os.path.join(HERE, "personas.json")))}
ITEMS = json.load(open(os.path.join(HERE, "survey_items.json")))["items"]

def wcsv(name, rows, cols):
    with open(os.path.join(rep, name), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); [w.writerow(r) for r in rows]

def med(x):
    x = [v for v in x if v is not None]
    return round(st.median(x), 1) if x else ""

outcomes = {os.path.basename(f)[:-5]: json.load(open(f)) for f in sorted(glob.glob(os.path.join(run, "outcomes", "*.json")))}
logs = {os.path.basename(f)[:-6]: [json.loads(l) for l in open(f)] for f in sorted(glob.glob(os.path.join(run, "logs", "*.jsonl")))}
store = {os.path.basename(f)[:-5]: json.load(open(f)) for f in sorted(glob.glob(os.path.join(run, "synthetic_store", "*.json")))}
pids = sorted(set(outcomes) | set(logs))

# ---------------- tasks ----------------
task_rows, part_rows = [], []
for pid in pids:
    o = outcomes.get(pid, {}); p = P[pid]; sp = o.get("survey_params") or {}
    alt = sp.get("alt") or ("label" if p["group"] == "A" else "category")
    for s in o.get("stores", []):
        k = {"control": "c", "filter": "f"}.get(s["version"], "a")
        task_rows.append({"pid": pid, "model": p["model"], "device": p["device"], "language": p["language"], "literacy": p["digital_literacy"], "patience": p["patience"],
                          "store_index": s["store_index"], "version": s["version"], "outcome": s["outcome"], "success": int(s["outcome"] == "completed"),
                          "steps": s["steps"], "found": s.get("found"), "mistakes": s.get("mistakes"), "offlist": s.get("offlist"),
                          "pages": s.get("pages"), "searches": s.get("searches"), "app_time_s": s.get("app_time_s"),
                          "feature_use": sp.get(f"{k}_feature"), "ease": sp.get(f"{k}_ease")})
    lg = logs.get(pid, [])
    part_rows.append({"pid": pid, "model": p["model"], "group": p["group"], "device": p["device"], "language": p["language"], "diet": p["diet"],
                      "literacy": p["digital_literacy"], "patience": p["patience"], "motivation": p["filter_motivation"],
                      "ended_by": o.get("ended_by", "no outcome (agent stopped early?)"), "steps_total": o.get("steps_total", len(lg)),
                      "wall_s": o.get("wall_s"), "order": sp.get("order", ""), "page_errors": len(o.get("errors", [])),
                      "failed_actions": sum(1 for r in lg if r.get("ok") is False), "stuck_events": sum(1 for r in lg if r.get("stuck")),
                      "survey_saved": pid in store})
wcsv("tasks.csv", task_rows, list(task_rows[0]) if task_rows else ["pid"])
wcsv("participants.csv", part_rows, list(part_rows[0]) if part_rows else ["pid"])

by_v = collections.defaultdict(list)
for r in task_rows: by_v[r["version"]].append(r)
task_sum = []
for v in ["control", "filter", "label", "category"]:
    rs = by_v.get(v, [])
    if not rs: continue
    task_sum.append({"version": v, "n": len(rs), "success_rate": round(sum(r["success"] for r in rs) / len(rs), 2),
                     "median_steps": med([r["steps"] for r in rs]), "median_steps_success": med([r["steps"] for r in rs if r["success"]]),
                     "mean_mistakes": round(st.mean([r["mistakes"] or 0 for r in rs]), 2), "mean_offlist": round(st.mean([r["offlist"] or 0 for r in rs]), 2),
                     "median_app_time_s": med([r["app_time_s"] for r in rs]), "mean_ease": round(st.mean([float(r["ease"]) for r in rs if r["ease"]]), 2) if any(r["ease"] for r in rs) else "",
                     "outcomes": dict(collections.Counter(r["outcome"] for r in rs))})
wcsv("task_summary.csv", task_sum, ["version", "n", "success_rate", "median_steps", "median_steps_success", "mean_mistakes", "mean_offlist", "median_app_time_s", "mean_ease", "outcomes"])

# where agents got stuck
stuck = []
for pid, lg in logs.items():
    for r in lg:
        why = None
        if r.get("stuck"): why = "same screen repeated"
        elif r.get("ok") is False: why = "action failed: " + (r.get("note") or "")[:80]
        elif r.get("event") in ("store_budget", "participant_skip", "participant_quit", "total_budget"): why = r["event"]
        elif r.get("errors"): why = "page error: " + "; ".join(r["errors"])[:80]
        if why:
            stv = r.get("state") or {}
            stuck.append({"pid": pid, "step": r.get("step"), "store": stv.get("store") or (stv.get("step", -1) + 1), "version": stv.get("version"), "phase": stv.get("phase"),
                          "why": why, "last_cmd": r.get("cmd"), "arg": r.get("arg"), "screenshot": r.get("screenshot")})
wcsv("stuck_points.csv", stuck, ["pid", "step", "store", "version", "phase", "why", "last_cmd", "arg", "screenshot"])

# ---------------- survey ----------------
long, reasons = [], []
for pid, rec in store.items():
    alt = (rec.get("hidden_fields") or {}).get("alt", "")
    for k, v in rec["answers"].items():
        a = v.get("answer")
        if isinstance(a, dict):
            for kk, vv in a.items():
                long.append({"pid": pid, "alt": alt, "item": k, "sub": kk, "value": vv, "model": rec["model"]})
        else:
            long.append({"pid": pid, "alt": alt, "item": k, "sub": "", "value": a, "model": rec["model"]})
        reasons.append({"pid": pid, "item": k, "answer": json.dumps(a, ensure_ascii=False), "reason": v.get("reason") or ""})
wcsv("survey_long.csv", long, ["pid", "alt", "item", "sub", "value", "model"])
wcsv("survey_reasons.csv", reasons, ["pid", "item", "answer", "reason"])

items = collections.defaultdict(list)
for r in long:
    if r["value"] is None or r["value"] == "": continue
    items[(r["item"], r["sub"])].append(r["value"])
summ = []
for (it, sub), vals in sorted(items.items()):
    num = all(isinstance(v, (int, float)) for v in vals)
    cnt = collections.Counter(vals if num else [str(v) for v in vals])
    top_share = cnt.most_common(1)[0][1] / len(vals)
    sd = round(st.pstdev(vals), 2) if num and len(vals) > 1 else ""
    nzv = (top_share >= 0.85) or (num and sd != "" and sd < 0.5 and max(vals) - min(vals) <= 1 and it not in ("Q13",))
    summ.append({"item": it, "sub": sub, "n": len(vals), "mean": round(st.mean(vals), 2) if num else "", "sd": sd,
                 "distribution": "; ".join(f"{k}: {v}" for k, v in sorted(cnt.items(), key=lambda x: str(x[0]))),
                 "top_share": round(top_share, 2), "near_zero_variance": int(nzv and it not in ("Q12", "Q13", "Q2"))})
wcsv("item_summary.csv", summ, ["item", "sub", "n", "mean", "sd", "distribution", "top_share", "near_zero_variance"])

# contradictions
def ans(rec, k):
    v = rec["answers"].get(k, {}); return v.get("answer") if isinstance(v, dict) else v
diet_map = {"omnivore": "Omnivore", "flexitarian": "Flexitarian", "vegetarian": "Vegetarian", "vegan": "Vegan", "other": "Other"}
contra = []
for pid, rec in store.items():
    p = P[pid]; q1, q3, q7, q5, q9, q10 = (ans(rec, k) for k in ("Q1", "Q3", "Q7", "Q5", "Q9", "Q10"))
    if isinstance(q3, dict) and q1 in q3 and q3[q1] != 1:
        contra.append({"pid": pid, "check": "Q1 choice is not ranked 1st in Q3", "detail": f"Q1={q1}; Q3={q3}"})
    if q1 == "Store with a vegan filter":
        rows = [ans(rec, f"Q4{x}") for x in "abcd"]
        if all(isinstance(r, dict) and r.get("alt") is not None and r.get("filter") is not None for r in rows) and sum(r["alt"] for r in rows) > sum(r["filter"] for r in rows):
            contra.append({"pid": pid, "check": "Chose filter store in Q1 but rated the alternative higher in Q4", "detail": json.dumps(rows)})
    if isinstance(q7, (int, float)) and isinstance(q5, (int, float)) and q7 >= 4 and q5 == 0:
        contra.append({"pid": pid, "check": "Likely to use filter (Q7>=4) but says it removes 0% of inconvenience (Q5)", "detail": f"Q7={q7}, Q5={q5}"})
    if q9 and not q9.startswith(diet_map[p["diet"]]):
        contra.append({"pid": pid, "check": "Q9 diet differs from persona diet", "detail": f"persona={p['diet']}, Q9={q9}"})
    if q9 and q9.startswith("Vegan") and q10 == "No":
        contra.append({"pid": pid, "check": "Says vegan (Q9) but never followed a vegan diet (Q10)", "detail": ""})
    # survey vs behaviour: rated a store easiest but failed it
    for t in [r for r in task_rows if r["pid"] == pid and not r["success"]]:
        if isinstance(q3, dict):
            name = {"control": "Regular store", "filter": "Store with a vegan filter"}.get(t["version"], [k for k in q3 if k not in ("Regular store", "Store with a vegan filter")][0] if q3 else "")
            if q3.get(name) == 1:
                contra.append({"pid": pid, "check": "Ranked a store most convenient (Q3) that they did not complete", "detail": f"{t['version']}: {t['outcome']}"})
    for pr in rec.get("validation_problems", []):
        contra.append({"pid": pid, "check": "validation problem", "detail": pr})
wcsv("contradictions.csv", contra, ["pid", "check", "detail"])

# confusing wording themes in free text and reasons
pat = re.compile(r"confus|unclear|not sure|don.t understand|didn.t understand|what (does|do) .* mean|ambiguous|hard to say|depends|which store|weird|strange|no idea", re.I)
themes = [r for r in reasons if pat.search(r["reason"] or "") or (r["item"] == "Q2" and pat.search(r["answer"] or ""))]
wcsv("confusion_flags.csv", themes, ["pid", "item", "answer", "reason"])

# ---------------- analysis pipeline check (planned analyses) ----------------
pipe = []
def within(metric):
    d = collections.defaultdict(dict)
    for r in task_rows: d[r["pid"]][r["version"] if r["version"] in ("control", "filter") else "alt"] = r[metric]
    res = {}
    for other in ("control", "alt"):
        diffs = [v["filter"] - v[other] for v in d.values() if v.get("filter") is not None and v.get(other) is not None]
        if diffs:
            pos = sum(1 for x in diffs if x > 0); neg = sum(1 for x in diffs if x < 0)
            res[other] = f"n={len(diffs)}, mean diff (filter - {other})={round(st.mean(diffs), 2)}, filter lower in {neg}, higher in {pos}"
    return res
for m in ("steps", "mistakes"):
    for k, v in within(m).items(): pipe.append(f"Within-person {m}: filter vs {k}: {v}")
q1 = collections.Counter(ans(r, "Q1") for r in store.values())
pipe.append("Q1 store choice: " + ", ".join(f"{k}: {v}" for k, v in q1.items()))
q5 = [ans(r, "Q5") for r in store.values() if isinstance(ans(r, "Q5"), (int, float))]
if q5: pipe.append(f"Q5 share of convenience barrier removed: mean {round(st.mean(q5),1)}%, median {st.median(q5)}%, range {min(q5)}-{max(q5)} (n={len(q5)})")
for k in ("a", "b", "c"):
    v = [ans(r, f"Q6{k}") for r in store.values() if isinstance(ans(r, f"Q6{k}"), (int, float))]
    if v: pipe.append(f"Q6{k} mean {round(st.mean(v),2)} (n={len(v)})")
by_model = collections.defaultdict(list)
for r in task_rows: by_model[r["model"]].append(r)
for mdl, rs in by_model.items():
    pipe.append(f"Model '{mdl}': {len(set(r['pid'] for r in rs))} participants, success {round(sum(r['success'] for r in rs)/len(rs),2)}, median steps {med([r['steps'] for r in rs])}")
qm = collections.defaultdict(list)
for r in store.values():
    if isinstance(ans(r, "Q5"), (int, float)): qm[r["model"]].append(ans(r, "Q5"))
for mdl, v in qm.items(): pipe.append(f"Model '{mdl}': Q5 mean {round(st.mean(v),1)} (n={len(v)})")

with open(os.path.join(rep, "report_auto.md"), "w") as f:
    f.write(f"# Synthetic pilot – automatic summary\n\nRun: `{run}`  \nParticipants with logs: {len(pids)}; outcomes: {len(outcomes)}; surveys saved: {len(store)}\n\n")
    f.write("## Tasks by store version\n\n| version | n | success | median steps | median steps (successful) | mean mistakes | mean off-list | mean ease | outcomes |\n|---|---|---|---|---|---|---|---|---|\n")
    for t in task_sum:
        f.write(f"| {t['version']} | {t['n']} | {t['success_rate']} | {t['median_steps']} | {t['median_steps_success']} | {t['mean_mistakes']} | {t['mean_offlist']} | {t['mean_ease']} | {t['outcomes']} |\n")
    f.write(f"\n## Stuck / failure points: {len(stuck)} (see stuck_points.csv)\n\n## Survey items\n\n| item | sub | n | mean | sd | top share | near-zero variance |\n|---|---|---|---|---|---|---|\n")
    for s in summ: f.write(f"| {s['item']} | {s['sub']} | {s['n']} | {s['mean']} | {s['sd']} | {s['top_share']} | {'YES' if s['near_zero_variance'] else ''} |\n")
    f.write(f"\n## Contradictions: {len(contra)} (see contradictions.csv)\n\n")
    for c in contra: f.write(f"- {c['pid']}: {c['check']} {c['detail']}\n")
    f.write(f"\n## Possible confusion flags in reasons: {len(themes)} (see confusion_flags.csv)\n\n## Analysis pipeline output\n\n")
    for l in pipe: f.write(f"- {l}\n")
print(open(os.path.join(rep, "report_auto.md")).read())
