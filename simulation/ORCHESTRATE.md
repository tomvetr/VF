# Running the pilot in subagent mode (no API key)

Claude Code runs each synthetic participant as a separate subagent. The subagent gets **only** its
persona and the participant instructions (`prompts/task_agent.md` filled in); it never sees code,
repo files, hypotheses or this document. It can act on the site only through `bin/shop`.

1. `node harness/server.mjs runs/<run>` in the background (one browser, one context per participant).
2. `python3 pipeline.py task-prompts runs/<run> <pids>` and launch one subagent per participant with
   the text of `runs/<run>/prompts/<pid>_task.md` as its prompt. Personas with `"model": "secondary"`
   use the second model (Sonnet). Run at most 6 at a time.
3. (Skip steps 3-4 while `run_survey` is false in config.json.) After a participant finishes (outcome file exists): `python3 pipeline.py survey-input runs/<run> <pid>`,
   then launch a **fresh** subagent with `runs/<run>/prompts/<pid>_survey.md` as its prompt (same model
   as the task). It reads only its own input file and writes `runs/<run>/raw/<pid>.json`.
4. `python3 pipeline.py save-survey runs/<run> <pids>` validates answers and writes
   `runs/<run>/synthetic_store/<pid>.json` with `synthetic: true`. Nothing is sent to Zoho:
   the harness intercepts the survey link.
5. `python3 analyze.py runs/<run>` writes `runs/<run>/report/`.
