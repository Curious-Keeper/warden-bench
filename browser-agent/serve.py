"""Entrypoint for the browser service.

    python serve.py                  # run the service, headed Chromium
    python serve.py --login TARGET   # open browser to TARGET's login URL,
                                     # poll until logged in, save storage
                                     # state, exit. Use once per session.

Env: HARNESS_HOST, HARNESS_PORT, HARNESS_HEADED, HARNESS_SESSION_DIR.
See .env.example.
"""

from __future__ import annotations

import argparse
import os
import sys
import threading
import time
from pathlib import Path

from dotenv import load_dotenv


def _run_service_in_thread() -> threading.Thread:
    """Boot uvicorn in a daemon thread so we can drive the client from main."""
    import uvicorn

    from browser import server

    host = os.environ.get("HARNESS_HOST", "127.0.0.1")
    port = int(os.environ.get("HARNESS_PORT", "8765"))
    config = uvicorn.Config(server.app, host=host, port=port, log_level="warning")
    srv = uvicorn.Server(config)

    def _run() -> None:
        srv.run()

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return t


def _login_flow(target_name: str, timeout_s: int = 600) -> int:
    from browser.client import BrowserClient
    from targets import get_target

    target = get_target(target_name)
    _run_service_in_thread()

    client = BrowserClient()
    client.wait_until_ready(timeout_s=30)

    print(f"[login] opening {target.LOGIN_URL}")
    client.goto(target.LOGIN_URL)
    print(f"[login] log in by hand in the browser window. polling every 2s "
          f"(timeout {timeout_s}s)…")

    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        try:
            if target.is_logged_in(client):
                client.save_state()
                print("[login] success — storage_state saved. exiting.")
                return 0
        except Exception as exc:
            print(f"[login] is_logged_in raised {exc!r} — retrying")
        time.sleep(2)

    print(f"[login] timed out after {timeout_s}s — not logged in", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    load_dotenv(dotenv_path=Path(__file__).parent / ".env")

    parser = argparse.ArgumentParser(description="harness browser service")
    parser.add_argument(
        "--login",
        metavar="TARGET",
        help="run the manual login bootstrap for TARGET, then exit",
    )
    args = parser.parse_args(argv)

    if args.login:
        return _login_flow(args.login)

    from browser.server import main as run_server

    run_server()
    return 0


if __name__ == "__main__":
    sys.exit(main())
