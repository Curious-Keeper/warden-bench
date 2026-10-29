"""Sync HTTP client for the browser service.

The agent loop, target adapters, and any direct REPL/notebook caller use
this. It mirrors the verb surface in actions.py and the endpoint surface
in server.py so swapping the engine later (carbonyl, computer-use) means
re-implementing this client against a different backend, not rewriting
callers.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import httpx


DEFAULT_BASE_URL = (
    f"http://{os.environ.get('HARNESS_HOST', '127.0.0.1')}:"
    f"{os.environ.get('HARNESS_PORT', '8765')}"
)


class BrowserClient:
    def __init__(self, base_url: str = DEFAULT_BASE_URL, timeout: float = 60.0) -> None:
        self._http = httpx.Client(base_url=base_url, timeout=timeout)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "BrowserClient":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    # ---- helpers -------------------------------------------------------

    def _post(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        r = self._http.post(path, json=json or {})
        r.raise_for_status()
        return r.json()

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        r = self._http.get(path, params=params or {})
        r.raise_for_status()
        return r.json()

    # ---- service health ------------------------------------------------

    def healthz(self) -> dict[str, Any]:
        return self._get("/healthz")

    def wait_until_ready(self, timeout_s: float = 30.0) -> None:
        """Poll /healthz until the browser context is up."""
        import time

        deadline = time.monotonic() + timeout_s
        last_err: Exception | None = None
        while time.monotonic() < deadline:
            try:
                if self.healthz().get("ok"):
                    return
            except Exception as exc:
                last_err = exc
            time.sleep(0.5)
        raise RuntimeError(f"browser service not ready within {timeout_s}s: {last_err}")

    # ---- navigation ----------------------------------------------------

    def goto(self, url: str) -> dict[str, Any]:
        return self._post("/goto", {"url": url})

    def reload(self) -> dict[str, Any]:
        return self._post("/reload")

    def back(self) -> dict[str, Any]:
        return self._post("/back")

    # ---- perception ----------------------------------------------------

    def state(self) -> dict[str, Any]:
        return self._get("/state")

    def screenshot(self, save_to: str | Path | None = None, full_page: bool = False) -> bytes:
        r = self._http.get("/screenshot", params={"full_page": full_page})
        r.raise_for_status()
        png = r.content
        if save_to is not None:
            Path(save_to).write_bytes(png)
        return png

    def find_text(self, query: str) -> list[dict[str, Any]]:
        return self._get("/find_text", {"query": query})["matches"]

    # ---- action verbs --------------------------------------------------

    def click_text(self, query: str, nth: int = 0) -> None:
        self._post("/click_text", {"query": query, "nth": nth})

    def click_role(self, role: str, name: str | None = None) -> None:
        self._post("/click_role", {"role": role, "name": name})

    def fill_label(self, label: str, value: str) -> None:
        self._post("/fill_label", {"label": label, "value": value})

    def fill_placeholder(self, placeholder: str, value: str) -> None:
        self._post("/fill_placeholder", {"placeholder": placeholder, "value": value})

    def select_option(self, label: str, option: str) -> None:
        self._post("/select_option", {"label": label, "option": option})

    def press(self, key: str) -> None:
        self._post("/press", {"key": key})

    def type_text(self, text: str, delay_ms: int = 0) -> None:
        self._post("/type", {"text": text, "delay_ms": delay_ms})

    def upload_file(self, label: str, path: str | Path) -> None:
        self._post("/upload_file", {"label": label, "path": str(path)})

    # ---- waits ---------------------------------------------------------

    def wait_for_text(self, text: str, timeout_ms: int = 10_000) -> bool:
        return self._post("/wait_for_text", {"text": text, "timeout_ms": timeout_ms})["ok"]

    def wait_for_url(self, pattern: str, timeout_ms: int = 10_000) -> bool:
        return self._post("/wait_for_url", {"pattern": pattern, "timeout_ms": timeout_ms})["ok"]

    def wait_for_selector(self, selector: str, timeout_ms: int = 10_000) -> bool:
        return self._post(
            "/wait_for_selector", {"selector": selector, "timeout_ms": timeout_ms}
        )["ok"]

    # ---- session -------------------------------------------------------

    def save_state(self) -> dict[str, Any]:
        return self._post("/save_state")
