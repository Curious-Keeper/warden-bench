"""FastAPI service exposing a long-lived Playwright browser over local HTTP.

Run via `python -m browser.server` or `python serve.py`. Defaults to
127.0.0.1:8765 with a headed Chromium window so you can watch the agent
work, intervene to log in, etc. Storage state (cookies + localStorage) is
persisted to .session/storage_state.json on every checkpoint, so login
survives restarts.

Single Browser → BrowserContext → Page per process. Multi-tab is out of
scope until a target needs it.
"""

from __future__ import annotations

import asyncio
import contextlib
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from playwright.async_api import Browser, BrowserContext, Page, async_playwright

from . import actions


HARNESS_ROOT = Path(__file__).resolve().parent.parent
SESSION_DIR = HARNESS_ROOT / os.environ.get("HARNESS_SESSION_DIR", ".session")
STORAGE_STATE_PATH = SESSION_DIR / "storage_state.json"

# Headed flags: let media streams through without permission prompts
# (audio-channel targets hang on the permission prompt otherwise).
HEADED_LAUNCH_ARGS = [
    "--use-fake-ui-for-media-stream",
    "--autoplay-policy=no-user-gesture-required",
]


class _State:
    playwright = None
    browser: Browser | None = None
    context: BrowserContext | None = None
    page: Page | None = None
    lock = asyncio.Lock()


state = _State()


@asynccontextmanager
async def _lifespan(_app: FastAPI):
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    headed = os.environ.get("HARNESS_HEADED", "1") != "0"

    state.playwright = await async_playwright().start()
    state.browser = await state.playwright.chromium.launch(
        headless=not headed,
        args=HEADED_LAUNCH_ARGS if headed else [],
    )

    context_kwargs: dict[str, Any] = {
        "viewport": {"width": 1280, "height": 800},
        "permissions": ["microphone", "camera"] if headed else [],
    }
    if STORAGE_STATE_PATH.exists():
        context_kwargs["storage_state"] = str(STORAGE_STATE_PATH)

    state.context = await state.browser.new_context(**context_kwargs)
    state.page = await state.context.new_page()
    try:
        yield
    finally:
        with contextlib.suppress(Exception):
            if state.context is not None:
                await state.context.storage_state(path=str(STORAGE_STATE_PATH))
        with contextlib.suppress(Exception):
            if state.browser is not None:
                await state.browser.close()
        with contextlib.suppress(Exception):
            if state.playwright is not None:
                await state.playwright.stop()


app = FastAPI(title="harness-browser", version="0.1.0", lifespan=_lifespan)


def _page() -> Page:
    if state.page is None:
        raise HTTPException(status_code=503, detail="browser not started")
    return state.page


# ------------------------------- Models --------------------------------


class GotoBody(BaseModel):
    url: str


class TextQuery(BaseModel):
    query: str
    nth: int = 0


class RoleQuery(BaseModel):
    role: str
    name: str | None = None


class LabelValue(BaseModel):
    label: str
    value: str


class PlaceholderValue(BaseModel):
    placeholder: str
    value: str


class LabelOption(BaseModel):
    label: str
    option: str


class KeyPress(BaseModel):
    key: str


class TypeText(BaseModel):
    text: str
    delay_ms: int = 0


class UploadBody(BaseModel):
    label: str
    path: str


class WaitText(BaseModel):
    text: str
    timeout_ms: int = actions.DEFAULT_TIMEOUT_MS


class WaitUrl(BaseModel):
    pattern: str
    timeout_ms: int = actions.DEFAULT_TIMEOUT_MS


class WaitSelector(BaseModel):
    selector: str
    timeout_ms: int = actions.DEFAULT_TIMEOUT_MS


# ----------------------------- Endpoints -------------------------------


@app.get("/healthz")
async def healthz() -> dict[str, Any]:
    return {
        "ok": state.page is not None,
        "url": state.page.url if state.page else None,
        "storage_state_exists": STORAGE_STATE_PATH.exists(),
    }


@app.post("/goto")
async def _goto(body: GotoBody) -> dict[str, Any]:
    async with state.lock:
        await actions.goto(_page(), body.url)
    return {"ok": True, "url": _page().url}


@app.post("/reload")
async def _reload() -> dict[str, Any]:
    async with state.lock:
        await actions.reload(_page())
    return {"ok": True, "url": _page().url}


@app.post("/back")
async def _back() -> dict[str, Any]:
    async with state.lock:
        await actions.back(_page())
    return {"ok": True, "url": _page().url}


@app.get("/state")
async def _state() -> dict[str, Any]:
    async with state.lock:
        return await actions.page_state(_page())


@app.get("/screenshot")
async def _screenshot(full_page: bool = False) -> Response:
    async with state.lock:
        png = await actions.screenshot(_page(), full_page=full_page)
    return Response(content=png, media_type="image/png")


@app.get("/find_text")
async def _find_text(query: str) -> dict[str, Any]:
    async with state.lock:
        matches = await actions.find_text(_page(), query)
    return {"matches": matches}


@app.post("/click_text")
async def _click_text(body: TextQuery) -> dict[str, Any]:
    async with state.lock:
        await actions.click_text(_page(), body.query, nth=body.nth)
    return {"ok": True}


@app.post("/click_role")
async def _click_role(body: RoleQuery) -> dict[str, Any]:
    async with state.lock:
        await actions.click_role(_page(), body.role, name=body.name)
    return {"ok": True}


@app.post("/fill_label")
async def _fill_label(body: LabelValue) -> dict[str, Any]:
    async with state.lock:
        await actions.fill_label(_page(), body.label, body.value)
    return {"ok": True}


@app.post("/fill_placeholder")
async def _fill_placeholder(body: PlaceholderValue) -> dict[str, Any]:
    async with state.lock:
        await actions.fill_placeholder(_page(), body.placeholder, body.value)
    return {"ok": True}


@app.post("/select_option")
async def _select_option(body: LabelOption) -> dict[str, Any]:
    async with state.lock:
        await actions.select_option(_page(), body.label, body.option)
    return {"ok": True}


@app.post("/press")
async def _press(body: KeyPress) -> dict[str, Any]:
    async with state.lock:
        await actions.press(_page(), body.key)
    return {"ok": True}


@app.post("/type")
async def _type(body: TypeText) -> dict[str, Any]:
    async with state.lock:
        await actions.type_text(_page(), body.text, delay_ms=body.delay_ms)
    return {"ok": True}


@app.post("/upload_file")
async def _upload(body: UploadBody) -> dict[str, Any]:
    if not Path(body.path).exists():
        raise HTTPException(status_code=400, detail=f"file not found: {body.path}")
    async with state.lock:
        await actions.upload_file(_page(), body.label, body.path)
    return {"ok": True}


@app.post("/wait_for_text")
async def _wait_for_text(body: WaitText) -> dict[str, Any]:
    async with state.lock:
        ok = await actions.wait_for_text(_page(), body.text, timeout_ms=body.timeout_ms)
    return {"ok": ok}


@app.post("/wait_for_url")
async def _wait_for_url(body: WaitUrl) -> dict[str, Any]:
    async with state.lock:
        ok = await actions.wait_for_url(_page(), body.pattern, timeout_ms=body.timeout_ms)
    return {"ok": ok}


@app.post("/wait_for_selector")
async def _wait_for_selector(body: WaitSelector) -> dict[str, Any]:
    async with state.lock:
        ok = await actions.wait_for_selector(
            _page(), body.selector, timeout_ms=body.timeout_ms
        )
    return {"ok": ok}


@app.post("/save_state")
async def _save_state() -> dict[str, Any]:
    async with state.lock:
        await state.context.storage_state(path=str(STORAGE_STATE_PATH))
    return {"ok": True, "path": str(STORAGE_STATE_PATH)}


def main() -> None:
    import uvicorn

    host = os.environ.get("HARNESS_HOST", "127.0.0.1")
    port = int(os.environ.get("HARNESS_PORT", "8765"))
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
