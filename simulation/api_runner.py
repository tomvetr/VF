"""API mode: run synthetic participants through the Anthropic Messages API (needs ANTHROPIC_API_KEY or `ant auth login`).

  python3 api_runner.py <run_dir> P01 P02 ...      (harness must be running: node harness/server.mjs <run_dir>)

Stops before exceeding the dollar cap in config.json -> api_cost_cap_usd (default 5).
Note: current Claude models reject `temperature`, so sampling is left at its default.
"""
import json, os, sys, re, urllib.request
import anthropic

HERE = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(HERE, "config.json")))
sys.path.insert(0, HERE)
import pipeline  # noqa: E402

MODELS = {"primary": "claude-opus-5-5", "secondary": "claude-sonnet-5-5"}
PRICE = {"claude-opus-5-5": (4.0, 20.0), "claude-sonnet-5-5": (2.0, 10.0)}  # $ per 1M input / output tokens
CAP = cfg.get("api_cost_cap_usd", 5.0)
client = anthropic.Anthropic()
spent = 0.0


def call(model, system, messages, max_tokens=2000):
    global spent
    if spent >= CAP:
        raise SystemExit(f"Cost cap ${CAP} reached (spent ~${spent:.2f}); stopping.")
    r = client.messages.create(model=model, max_tokens=max_tokens, system=system, messages=messages,
                               output_config={"effort": "low"})
    pin, pout = PRICE[model]
    spent += r.usage.input_tokens / 1e6 * pin + r.usage.output_tokens / 1e6 * pout
    if r.stop_reason == "refusal":
        return ""
    return "".join(b.text for b in r.content if b.type == "text")


def harness(ep, pid, cmd=None, arg=None):
    body = json.dumps({"pid": pid, "cmd": cmd, "arg": arg}).encode()
    req = urllib.request.Request(f"http://127.0.0.1:{cfg['harness_port']}/{ep}", data=body, method="POST")
    return urllib.request.urlopen(req, timeout=120).read().decode()


def run_participant(run, pid):
    p = pipeline.PERSONAS[pid]
    model = MODELS[p["model"]]
    tpl = open(os.path.join(HERE, "prompts", "task_agent.md")).read().replace("{PROFILE}", p["profile"])
    system = tpl.split("HOW TO USE THE WEBSITE")[0] + (
        "HOW TO USE THE WEBSITE\nEach turn you see the current screen. Reply with exactly one command on the first line, one of:\n"
        "look | click <number> | search <words> | back | home | skip_store | quit\n"
        "Numbers refer to the latest screen only. Do not write anything else.")
    obs = harness("start", pid)
    msgs = []
    for _ in range(cfg["budgets"]["steps_total"] + 5):
        msgs.append({"role": "user", "content": obs})
        msgs = msgs[-30:]  # keep the recent screens only
        if msgs[0]["role"] != "user":
            msgs = msgs[1:]
        out = call(model, system, msgs, 200).strip().splitlines()
        line = out[0].strip() if out else "look"
        msgs.append({"role": "assistant", "content": line})
        m = re.match(r"(look|click|search|back|home|skip_store|quit)\b\s*(.*)", line)
        cmd, arg = (m.group(1), m.group(2) or None) if m else ("look", None)
        obs = harness("act", pid, cmd, arg)
        if "SESSION OVER" in obs:
            break
    if not cfg.get('run_survey', True):
        print(f'{pid} done (survey skipped); spent so far ~${spent:.2f}')
        return
    # survey: fresh call with persona + own log + items
    pipeline.survey_input(run, [pid])
    inp = open(os.path.join(run, "prompts", f"{pid}_survey_input.md")).read()
    instr = open(os.path.join(HERE, "prompts", "survey_agent.md")).read().split("1. Read your input file")[0]
    txt = call(model, instr, [{"role": "user", "content": inp + "\n\nReturn ONLY the JSON object described: keys are question IDs, values {\"answer\": ..., \"reason\": \"...\"}."}], 4000)
    m = re.search(r"\{.*\}", txt, re.S)
    open(os.path.join(run, "raw", f"{pid}.json"), "w").write(m.group(0) if m else "{}")
    pipeline.save_survey(run, [pid], model)
    print(f"{pid} done; spent so far ~${spent:.2f}")


if __name__ == "__main__":
    run = os.path.abspath(sys.argv[1])
    for pid in sys.argv[2:]:
        run_participant(run, pid)
