"""Shared pytest fixtures for the harness smoke tests.

Boots the browser service in a daemon thread for a session-scoped client.
Headless by default so tests don't pop a window.
"""

from __future__ import annotations

import os
import sys
import threading
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="session")
def harness_port() -> int:
    return int(os.environ.get("HARNESS_TEST_PORT", "8766"))


@pytest.fixture(scope="session")
def browser_service(harness_port: int):
    """Start the browser service on a test-only port for the session."""
    os.environ["HARNESS_HEADED"] = "0"
    os.environ["HARNESS_PORT"] = str(harness_port)

    import uvicorn

    from browser import server

    config = uvicorn.Config(
        server.app, host="127.0.0.1", port=harness_port, log_level="warning"
    )
    srv = uvicorn.Server(config)

    thread = threading.Thread(target=srv.run, daemon=True)
    thread.start()

    deadline = time.monotonic() + 30
    import httpx

    while time.monotonic() < deadline:
        try:
            r = httpx.get(f"http://127.0.0.1:{harness_port}/healthz", timeout=1)
            if r.status_code == 200 and r.json().get("ok"):
                break
        except Exception:
            pass
        time.sleep(0.5)
    else:
        raise RuntimeError("browser service failed to start within 30s")

    yield srv

    srv.should_exit = True
    thread.join(timeout=5)


@pytest.fixture(scope="session")
def client(browser_service, harness_port: int):
    from browser.client import BrowserClient

    base_url = f"http://127.0.0.1:{harness_port}"
    with BrowserClient(base_url=base_url) as c:
        yield c
