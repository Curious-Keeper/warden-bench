"""Generic system prompt + slug derivation for ad-hoc targets.

When the user passes `--url` instead of `--target`, the loop builds a
virtual target on the fly from these helpers. No file required for
one-off labs; bespoke `targets/X.py` adapters are still preferred for
repeat work where login flows or page structure are gnarly.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse


GENERIC_SYSTEM_PROMPT = """You are an AI agent driving a real web browser on \
behalf of an authorized red-team / lab researcher. You have been given a goal \
and a mission context. The browser is already pointed at the target page.

MISSION CONTEXT:
{mission}

Operating principles:
- Read page state before acting; don't assume layout from a prior session.
- After every meaningful action, verify with `page_state` before the next move.
- If the same approach fails twice on the same step, change strategy — vary \
the angle, not just the wording.
- For multi-step labs (multi-level, multi-stage), persist: solve, advance, \
repeat. Many labs auto-advance on success — read the page state to confirm \
which step you're on.
- Never escalate scope beyond the page you've been given. Don't navigate to \
unrelated origins; if the page itself contains a link/button that needs \
following, that's fine.
- Authorized work only. The user has confirmed scope before starting; trust \
that and act decisively within it.
- When the goal is achieved (or you're conclusively blocked), call \
`submit_finding` with a clear `notes` field describing what worked / what \
blocked you. The loop exits on that call.

If the page asks for a login and you don't have an obvious credential to \
provide, call `submit_finding(success=false, notes='auth required — run with \
--login-pause and log in by hand first')`."""


_DEFAULT_MISSION = (
    "No specific mission context provided. Treat this as a generic web "
    "interaction task and follow the goal verbatim."
)


def render_generic_prompt(mission: str | None) -> str:
    return GENERIC_SYSTEM_PROMPT.format(mission=(mission or _DEFAULT_MISSION).strip())


def slug_from_url(url: str) -> str:
    """Derive a stable target slug from a URL.

    `https://warden.scalingsuccess.io/foo` -> `warden_scalingsuccess_io`
    `http://127.0.0.1:8000`               -> `127_0_0_1_8000`
    """
    parsed = urlparse(url)
    host = (parsed.hostname or "unknown").lower()
    if host.startswith("www."):
        host = host[4:]
    base = host.replace(".", "_").replace("-", "_")
    if parsed.port:
        base = f"{base}_{parsed.port}"
    # Strip anything that's not safe for a JSON key / filename.
    return re.sub(r"[^a-z0-9_]", "_", base)


class VirtualTarget:
    """Minimal target stub built from CLI args. Duck-types the adapter contract."""

    __slots__ = ("BASE_URL", "LOGIN_URL", "SYSTEM_PROMPT", "slug")

    def __init__(self, *, url: str, mission: str | None) -> None:
        self.BASE_URL = url
        self.LOGIN_URL = url
        self.SYSTEM_PROMPT = render_generic_prompt(mission)
        self.slug = slug_from_url(url)

    @staticmethod
    def is_logged_in(_client: object) -> bool:
        # Generic targets can't reliably auto-detect login; the operator
        # uses --login-pause to gate manually before the agent runs.
        return True
