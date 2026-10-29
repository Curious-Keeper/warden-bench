"""Verb-level browser actions on a Playwright Page.

Each function is a thin async wrapper that takes a Page and operates on it.
The HTTP layer in server.py exposes these 1:1; the agent and any direct
caller see the same surface.

Verb names mirror jmagly/carbonyl-agent's LLM-native API design
(click_text, find_text, fill_label) but use Playwright as the engine so
SPA dynamics, file uploads, and audio playback all work.
"""

from __future__ import annotations

import hashlib
from typing import Any

from playwright.async_api import Page, TimeoutError as PWTimeout


DEFAULT_TIMEOUT_MS = 10_000


async def goto(page: Page, url: str) -> None:
    await page.goto(url, wait_until="domcontentloaded", timeout=30_000)


async def reload(page: Page) -> None:
    await page.reload(wait_until="domcontentloaded", timeout=30_000)


async def back(page: Page) -> None:
    await page.go_back(wait_until="domcontentloaded", timeout=30_000)


async def page_state(page: Page) -> dict[str, Any]:
    """Return a compact, LLM-friendly snapshot of the current page.

    Uses Playwright's `aria_snapshot()` (YAML-format ARIA tree of role +
    name + state). Already structured for LLM consumption; no custom
    flattener needed.
    """
    a11y = await page.locator("body").aria_snapshot()
    html = await page.content()
    return {
        "url": page.url,
        "title": await page.title(),
        "accessibility": a11y,
        "dom_hash": hashlib.sha256(html.encode("utf-8", "ignore")).hexdigest()[:16],
    }


async def screenshot(page: Page, full_page: bool = False) -> bytes:
    return await page.screenshot(full_page=full_page, type="png")


async def find_text(page: Page, query: str) -> list[dict[str, Any]]:
    """Locate visible elements matching `query`. Returns text + role for each."""
    locator = page.get_by_text(query, exact=False)
    count = await locator.count()
    matches: list[dict[str, Any]] = []
    for i in range(min(count, 20)):
        item = locator.nth(i)
        try:
            text = (await item.inner_text(timeout=2000)).strip()
        except PWTimeout:
            continue
        role = await item.evaluate("el => el.getAttribute('role') || el.tagName.toLowerCase()")
        matches.append({"index": i, "text": text[:200], "role": role})
    return matches


async def click_text(page: Page, query: str, nth: int = 0) -> None:
    locator = page.get_by_text(query, exact=False).nth(nth)
    await locator.click(timeout=DEFAULT_TIMEOUT_MS)


async def click_role(page: Page, role: str, name: str | None = None) -> None:
    """Click by ARIA role + accessible name. More stable than text on buttons."""
    if name:
        locator = page.get_by_role(role, name=name)
    else:
        locator = page.get_by_role(role)
    await locator.first.click(timeout=DEFAULT_TIMEOUT_MS)


async def fill_label(page: Page, label: str, value: str) -> None:
    await page.get_by_label(label).first.fill(value, timeout=DEFAULT_TIMEOUT_MS)


async def fill_placeholder(page: Page, placeholder: str, value: str) -> None:
    await page.get_by_placeholder(placeholder).first.fill(value, timeout=DEFAULT_TIMEOUT_MS)


async def select_option(page: Page, label: str, option: str) -> None:
    """Select an option from a <select> by visible label or value."""
    target = page.get_by_label(label).first
    await target.select_option(label=option, timeout=DEFAULT_TIMEOUT_MS)


async def press(page: Page, key: str) -> None:
    """Press a single key on the focused element (Enter, Tab, Escape, etc.)."""
    await page.keyboard.press(key)


async def type_text(page: Page, text: str, delay_ms: int = 0) -> None:
    """Type literal text on the focused element."""
    await page.keyboard.type(text, delay=delay_ms)


async def upload_file(page: Page, label: str, path: str) -> None:
    """Set <input type=file> contents by label."""
    await page.get_by_label(label).first.set_input_files(path)


async def wait_for_text(page: Page, text: str, timeout_ms: int = DEFAULT_TIMEOUT_MS) -> bool:
    try:
        await page.get_by_text(text, exact=False).first.wait_for(
            state="visible", timeout=timeout_ms
        )
        return True
    except PWTimeout:
        return False


async def wait_for_url(page: Page, pattern: str, timeout_ms: int = DEFAULT_TIMEOUT_MS) -> bool:
    try:
        await page.wait_for_url(pattern, timeout=timeout_ms)
        return True
    except PWTimeout:
        return False


async def wait_for_selector(
    page: Page, selector: str, timeout_ms: int = DEFAULT_TIMEOUT_MS
) -> bool:
    try:
        await page.wait_for_selector(selector, timeout=timeout_ms, state="visible")
        return True
    except PWTimeout:
        return False
