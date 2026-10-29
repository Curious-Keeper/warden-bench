"""Warden integration test — skips if warden isn't running locally.

Verifies the warden adapter can navigate the static HTML form. Doesn't
attempt to solve a level (that's the agent loop's job); just proves the
verb layer round-trips against the warden's actual DOM.

Run with `WARDEN_BASE` set to a reachable warden origin. If the JSON
harness in operator/ already runs against it, this should too.
"""

from __future__ import annotations

import os

import httpx
import pytest

from targets import warden


WARDEN_BASE = os.environ.get("WARDEN_BASE", warden.BASE_URL)


def _warden_alive() -> bool:
    try:
        r = httpx.get(f"{WARDEN_BASE}/", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _warden_alive(),
    reason=f"warden not reachable at {WARDEN_BASE}",
)


def test_load_warden_home(client) -> None:
    client.goto(WARDEN_BASE + "/")
    assert client.wait_for_text("Levels", timeout_ms=10_000)
    assert warden.is_logged_in(client)


def test_current_level_reads(client) -> None:
    client.goto(WARDEN_BASE + "/")
    client.wait_for_text("Levels", timeout_ms=10_000)
    level = warden.current_level(client)
    assert level >= 1
