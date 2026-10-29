"""Smoke tests for the browser service against example.com.

Always runs — no external dependencies beyond network.
"""

from __future__ import annotations


def test_healthz(client) -> None:
    h = client.healthz()
    assert h["ok"] is True


def test_goto_state_roundtrip(client) -> None:
    client.goto("https://example.com")
    state = client.state()
    assert "example.com" in state["url"]
    assert "Example Domain" in state["title"]
    assert "Example Domain" in state["accessibility"]
    assert len(state["dom_hash"]) == 16


def test_screenshot_returns_png(client, tmp_path) -> None:
    client.goto("https://example.com")
    out = tmp_path / "example.png"
    png = client.screenshot(save_to=out)
    assert png.startswith(b"\x89PNG\r\n\x1a\n")
    assert out.read_bytes() == png


def test_find_text(client) -> None:
    client.goto("https://example.com")
    matches = client.find_text("Example Domain")
    assert any("Example Domain" in m["text"] for m in matches)
