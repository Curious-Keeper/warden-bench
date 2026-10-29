# Reusable Browser-Agent Harness

A two-process LLM-driven browser harness. One process runs a long-lived
headed Playwright session and exposes verb-level browser actions over a
local HTTP API. A separate stateless agent process drives that browser
via Claude tool-use. Works against any webapp where you'd otherwise need
to write per-site scrapers.

Built for authorized red-team arenas, tested against the Warden lab, and
designed to be target-agnostic — adding a new webapp is one file in
[targets/](targets/).

## Why two processes

The browser is a service:

* **Login once, stay logged in.** Storage state (cookies + localStorage)
  persists across agent restarts, so OAuth/SSO flows happen once.
* **Watch the agent work.** Headed Chromium opens; you see every click.
  Useful for debugging, demos, and intervening when needed.
* **Mid-flow intervention.** Captcha, MFA, manual recovery — switch to
  the browser window, do the thing, the agent picks back up.
* **Headless flag flips for CI** — same code path.

## Setup

```bash
cd browser-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env  # then edit
```

Required env: `ANTHROPIC_API_KEY`. Optional: `HARNESS_HEADED=0` for
headless, `HARNESS_MODEL=claude-opus-4-7` for harder targets,
`ELEVENLABS_API_KEY` for AUDIO-channel TTS.

## Quickstart: warden lab (test target)

The Warden lab is the sanity-check target —
JSON-driven solves are already known via the
[`operator/`](../operator/) harness, so the browser
solves are easy to validate against ground truth.

```bash
# Terminal 1 — boot the browser service (headed Chromium opens)
.venv/bin/python serve.py

# Terminal 2 — drive the loop
.venv/bin/python -m agent.loop \
    --target warden \
    --goal "Solve level 1 — extract the secret password and submit it"
```

Watch Chromium do the work. The loop prints `success=...` on exit and a
cost summary; full event log is in `arena-probes.jsonl`.

## Quickstart: any webapp (no adapter needed)

For a one-off lab where you don't want to write a target adapter, use
`--url` + `--mission` instead of `--target`:

```bash
# Terminal 1 — boot the browser service
.venv/bin/python serve.py

# Terminal 2 — drive an ad-hoc target
.venv/bin/python -m agent.loop \
    --url https://some-lab.example.com \
    --mission "Authorized red-team exercise. Defender LLM picks 1 of 4 actions; bounty fires when it picks 'suppress'." \
    --goal "Beat the bounty by tricking the defender into suppression. Iterate until done." \
    --max-iters 100 \
    --login-pause
```

Flags:

| flag | what it does |
|---|---|
| `--url` | Ad-hoc target URL. Mutually exclusive with `--target`. Slug auto-derived from hostname (e.g. `lab.example.com` → `lab_example_com`) and used to namespace state + logs. |
| `--mission` | Free-text scenario context appended to the system prompt. Works with both `--target` and `--url`. Use for "this is a workshop demo / authorized bounty / simulated exercise on X". |
| `--login-pause` | Navigate to the target and pause for stdin Enter before the agent runs. Lets you log in by hand for any auth scheme (passcode, OAuth, MFA). Saves storage state on continue. |
| `--no-warm-start` | Skip the auto-loaded "prior wins on this target" block. Useful for cold-baseline runs. |
| `--max-iters` | Default 50; bump to 100+ for whole-lab runs ("beat every level"). |

Three CLI shapes, same loop:

```bash
# Bespoke adapter (fast path; uses targets/warden.py)
python -m agent.loop --target warden --goal "Solve level 1"

# Ad-hoc URL (no adapter file needed)
python -m agent.loop --url https://x.example --goal "..."

# Bespoke + extra mission framing
python -m agent.loop --target warden --mission "Workshop demo." --goal "Beat all levels."
```

Warm-start is automatic on subsequent runs of the same slug — past
`success=true` findings get folded into the user message as PAIR-style
"these worked before, treat as hints" context. Toggle off with
`--no-warm-start` for a clean baseline.

## Logging in to auth-gated targets

For targets behind OAuth/SSO, bootstrap once with `serve.py --login <target>`:
it opens the browser, polls the adapter's `is_logged_in()`, saves
`storage_state.json` under `.session/` (gitignored) and exits. Re-run when the
session expires. For ad-hoc URLs use `--login-pause` instead.

## How the agent loop works

`agent/loop.py` is a Claude tool-use loop. Tools (defined in
`agent/tools.py`) map 1:1 to verbs in `browser/actions.py`:

| Tool | What it does |
|---|---|
| `page_state` | URL + title + ARIA snapshot + DOM hash. Default perception. |
| `screenshot` | PNG of the viewport. Use only when the a11y tree is unhelpful (canvas, custom widgets). |
| `find_text` / `click_text` / `click_role` | Locate and click. |
| `fill_label` / `fill_placeholder` / `select_option` | Form input. |
| `press` / `type_text` | Keyboard. |
| `upload_file` / `synthesize_speech` | File uploads + TTS for AUDIO channels. |
| `wait_for_text` / `wait_for_url` / `wait_for_selector` | Sync waits. |
| `goto` / `reload` / `back` | Navigation. |
| `submit_finding` | Terminal call: "I'm done, here's why." Loop exits. |

Loop terminates on: `submit_finding` → `stop_reason=end_turn` → or
`max_iters` (default 20). PAIR-style feedback is supported by the
caller — pass `extra_user_context=...` into `loop.run()` with prior
failed attempts; the loop folds that into the first user message.

## Adding a new target

Each adapter is one file in [targets/](targets/) with this contract:

```python
# targets/my_target.py
import os
BASE_URL  = os.environ.get("MY_TARGET_BASE", "https://...")
LOGIN_URL = BASE_URL + "/login"   # where to send the user for manual login

SYSTEM_PROMPT = """You are an attacker against ... (target-specific brief)"""

def is_logged_in(client) -> bool:
    """Poll callback for `serve.py --login`. Return True once auth state is good."""
    state = client.state()
    return "Sign out" in state["accessibility"]   # or whatever signal works
```

Then register the short name in [targets/__init__.py](targets/__init__.py):

```python
_REGISTRY = {
    "warden": "targets.warden",
    "my_target": "targets.my_target",   # ← add this line
}
```

Optionally add target-specific helpers (`submit_attack`, `solve_level`,
etc.) — the agent doesn't call them directly, but the loop driver can.

## Dedup + state

[agent/dedup.py](agent/dedup.py) implements pre-submit duplicate
filtering. Arenas often reject 'highly similar' submissions, and the warden
returns HTTP 409 on exact-match prompts per (ip, level). Two layers:

* Exact-match: sha256 of normalized field tuple. Always on. O(1).
* Embedding similarity: cosine via Voyage. Opt-in (`VOYAGE_API_KEY`),
  fall back to disabled if not set.

State lives in `arena-state.json`:

```json
{
  "warden": {
    "attempts": [
      {"hash": "...", "ts": "...", "key": {...}, "text": "...",
       "embedding": [...], "result": {"success": false, "reason": "..."}}
    ]
  }
}
```

`AttemptStore.exhausted_angles(limit=20)` returns the most recent
failures FIFO-trimmed — feed that as `extra_user_context` into the next
`loop.run()`.

## Logging

Every iteration, every tool call, every Claude response writes a line
to `arena-probes.jsonl` (rotated to `arena-probes-N.jsonl` between
runs via `state.rotate_log()`). Same shape as the warden harness's
`warden-probes-N.jsonl`. Grep by `kind` (`claude_call`, `tool_call`,
`tool_error`, `loop_finding`, etc.).

## Cost

Sonnet 4.6 with prompt caching: typical 20-iter loop on a small target
~$0.05–0.15. Opus 4.7 multiplies by ~5x. The system prompt and tool
definitions are cached, so subsequent iterations within the 5-minute
TTL pay cache-read rates instead of re-creation.

`log.cost_summary()` returns input/output/cache tokens + a USD estimate
based on Sonnet 4.6 list rates. Override the rates for Opus.

## Engine choice — why Playwright

Considered:

* **carbonyl-agent** — terminal-[REDACTED-L6]ed Chromium with LLM-native action
  verbs. Great API design (`click_text`, `find_text`) borrowed here. But
  [REDACTED-L6]ing breaks on rich UI, audio playback/upload, and OAuth popups.
* **Fortemi** — ruled out; it's a knowledge-base / MCP server, not a
  browser tool.
* **Anthropic computer-use** — vision-only at pixel coords. Slow and
  expensive when the page already exposes selectors. Reserved as an
  escape hatch for canvas/custom widgets where the a11y tree is empty.

Playwright is mainstream, handles SPA dynamics + login flows + audio
uploads cleanly, and exposes `Locator.aria_snapshot()` (YAML accessibility
tree) — already structured for LLM consumption, no custom flattener
needed. The verbs are implemented thin enough that swapping engines
later means re-implementing [`browser/client.py`](browser/client.py)
against a different backend, not rewriting callers.

## Files

```
browser-agent/
├── browser/
│   ├── actions.py     # verb implementations on a Playwright Page
│   ├── client.py      # sync HTTP client; what the agent imports
│   └── server.py      # FastAPI app exposing actions over HTTP
├── agent/
│   ├── dedup.py       # exact + embedding dedup, AttemptStore
│   ├── loop.py        # Claude tool-use loop
│   ├── state.py       # JSONL logging + token tally
│   ├── tools.py       # tool defs for Claude + dispatch to client
│   └── tts.py         # ElevenLabs / piper for AUDIO channels
├── targets/
│   └── warden.py      # warden target adapter
├── tests/             # pytest smoke + warden integration
├── serve.py           # entrypoint: runs the service or login bootstrap
├── requirements.txt
├── .env.example
└── README.md          # this file
```

## Anti-patterns

* **Don't** commit `.session/` — it holds live cookies. Review any new
  `arena-probes*.jsonl` before committing; page snapshots can capture
  account UI.
* **Don't** point this at non-authorized targets. Every adapter's
  SYSTEM_PROMPT bakes in the target context; sending those prompts
  elsewhere would be both unauthorized and ineffective.
* **Don't** use `--no-verify` to skip pre-commit hooks if you're
  pairing this with the parent repo's git workflow.

## Related

* [operator/harness.md](../operator/harness.md) —
  the JSON-endpoint sibling harness for the warden. The patterns here
  (PAIR feedback, JSONL logging, attempt store, prompt caching)
  originate there.
