#!/usr/bin/env bash
# One command to rerun the synthetic pilot.
#   ./run.sh <run_name> [P01 P02 ...]     (default: all personas)
# API mode (ANTHROPIC_API_KEY set or `ant auth login`): runs everything end to end.
# Subagent mode (no key): prepares the run and prints what Claude Code must do (see ORCHESTRATE.md),
#   then `./run.sh <run_name> --analyze` writes the report.
set -euo pipefail
cd "$(dirname "$0")"
RUN="runs/${1:?run name}"; shift || true
mkdir -p "$RUN"
if [ "${1:-}" = "--analyze" ]; then python3 analyze.py "$RUN"; exit 0; fi
[ -f personas.json ] || python3 personas.py
PIDS="$*"; [ -n "$PIDS" ] || PIDS=$(python3 -c "import json;print(' '.join(p['id'] for p in json.load(open('personas.json'))))")
node harness/server.mjs "$RUN" > "$RUN/harness.log" 2>&1 & HP=$!
trap 'curl -s -X POST localhost:8787/shutdown >/dev/null 2>&1 || kill $HP 2>/dev/null' EXIT
sleep 3
if [ -n "${ANTHROPIC_API_KEY:-}" ] || (command -v ant >/dev/null && ant auth status 2>/dev/null | grep -q "(active)"); then
  python3 -c "import anthropic" 2>/dev/null || pip install -q anthropic
  python3 api_runner.py "$RUN" $PIDS
  python3 analyze.py "$RUN"
else
  python3 pipeline.py task-prompts "$RUN" $PIDS > /dev/null
  echo "No API credentials: subagent mode. Ask Claude Code to follow simulation/ORCHESTRATE.md for run '$RUN'."
  echo "Harness is running (Ctrl-C to stop when the subagents are done)."; wait $HP
fi
