"""Tool definitions and dispatch for the Claude agent loop.

Each tool maps 1:1 to a method on `BrowserClient`. The schemas below are
what Claude sees; `dispatch()` is what runs the call. Adding a new verb
means adding it in three places (client, server, here) — keep them in
sync.
"""

from __future__ import annotations

import base64
from typing import Any

from browser.client import BrowserClient


# JSONSchema tool definitions for the Anthropic SDK. The last entry will
# get `cache_control` injected when `cached_tools()` is used so the whole
# tools block is cached on the prompt.
TOOLS: list[dict[str, Any]] = [
    {
        "name": "page_state",
        "description": (
            "Snapshot the current page: URL, title, a YAML accessibility tree "
            "(role + name + state), and a DOM hash. Cheap; call freely. "
            "This is your default 'what's on screen' tool — prefer it over "
            "screenshot unless you need pixel-level detail (canvas, image)."
        ),
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "screenshot",
        "description": (
            "Take a PNG screenshot of the current viewport. Returns an image "
            "block in the result. Use ONLY when the accessibility tree is "
            "empty/unhelpful (canvas, custom widget, image-only content). "
            "Costs ~5-10x a page_state call."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "full_page": {
                    "type": "boolean",
                    "description": "Capture the full scrollable page, not just viewport.",
                    "default": False,
                }
            },
            "required": [],
        },
    },
    {
        "name": "goto",
        "description": "Navigate to a URL. Waits for DOMContentLoaded.",
        "input_schema": {
            "type": "object",
            "properties": {"url": {"type": "string"}},
            "required": ["url"],
        },
    },
    {
        "name": "reload",
        "description": "Reload the current page.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "back",
        "description": "Go back one entry in browser history.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "find_text",
        "description": (
            "Find visible elements containing the given text. Returns up to 20 "
            "matches with their inner text and DOM role. Useful before clicking "
            "to confirm the right element exists."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    {
        "name": "click_text",
        "description": (
            "Click a visible element whose text contains `query`. Use `nth` to "
            "disambiguate when multiple matches exist (default 0 = first)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "nth": {"type": "integer", "default": 0},
            },
            "required": ["query"],
        },
    },
    {
        "name": "click_role",
        "description": (
            "Click an element by ARIA role + accessible name. More stable than "
            "click_text for buttons/links. Roles: 'button', 'link', 'textbox', etc."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "role": {"type": "string"},
                "name": {"type": "string"},
            },
            "required": ["role"],
        },
    },
    {
        "name": "fill_label",
        "description": (
            "Fill a text input/textarea identified by its <label>. Replaces "
            "existing content. For inputs without labels, use fill_placeholder."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "label": {"type": "string"},
                "value": {"type": "string"},
            },
            "required": ["label", "value"],
        },
    },
    {
        "name": "fill_placeholder",
        "description": (
            "Fill a text input/textarea identified by its placeholder text. "
            "Use when the input has no <label>."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "placeholder": {"type": "string"},
                "value": {"type": "string"},
            },
            "required": ["placeholder", "value"],
        },
    },
    {
        "name": "select_option",
        "description": "Choose an option from a <select> by its visible label.",
        "input_schema": {
            "type": "object",
            "properties": {
                "label": {"type": "string"},
                "option": {"type": "string"},
            },
            "required": ["label", "option"],
        },
    },
    {
        "name": "press",
        "description": (
            "Press a single key on the focused element. Examples: 'Enter', "
            "'Tab', 'Escape', 'ArrowDown'."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"key": {"type": "string"}},
            "required": ["key"],
        },
    },
    {
        "name": "type_text",
        "description": (
            "Type literal text on the focused element. Use after a click on a "
            "field that fill_label can't address."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "delay_ms": {"type": "integer", "default": 0},
            },
            "required": ["text"],
        },
    },
    {
        "name": "upload_file",
        "description": (
            "Upload a file to an <input type=file> identified by its label. "
            "Path must already exist on the harness host."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "label": {"type": "string"},
                "path": {"type": "string"},
            },
            "required": ["label", "path"],
        },
    },
    {
        "name": "wait_for_text",
        "description": "Wait for visible text to appear. Returns true on success.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "timeout_ms": {"type": "integer", "default": 10000},
            },
            "required": ["text"],
        },
    },
    {
        "name": "wait_for_url",
        "description": "Wait for the URL to match a glob pattern. Returns true on success.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pattern": {"type": "string"},
                "timeout_ms": {"type": "integer", "default": 10000},
            },
            "required": ["pattern"],
        },
    },
    {
        "name": "synthesize_speech",
        "description": (
            "Convert text to a WAV audio file via TTS (ElevenLabs if "
            "ELEVENLABS_API_KEY set, else local piper). Returns the file path. "
            "Use this before upload_file when a target needs an audio submission "
            "(e.g. a voice/AUDIO input channel)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
    },
    {
        "name": "submit_finding",
        "description": (
            "Terminal tool: declare you are done. Set `success=true` if you "
            "achieved the goal (extracted the password / triggered the bounty / "
            "completed the task), else `success=false` with a `notes` field "
            "explaining what blocked you. The loop exits after this call."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "notes": {
                    "type": "string",
                    "description": "What you tried and what the outcome was.",
                },
            },
            "required": ["success", "notes"],
        },
    },
]


def cached_tools() -> list[dict[str, Any]]:
    """Return TOOLS with `cache_control` on the last entry for prompt caching."""
    out = [dict(t) for t in TOOLS]
    out[-1] = dict(out[-1], cache_control={"type": "ephemeral"})
    return out


# ----------------------------- dispatch --------------------------------


_FINDING_SENTINEL = object()


class FindingResult:
    __slots__ = ("success", "notes")

    def __init__(self, success: bool, notes: str) -> None:
        self.success = success
        self.notes = notes


def dispatch(client: BrowserClient, name: str, args: dict[str, Any]) -> Any:
    """Execute a tool call. Returns a value suitable for a tool_result block.

    For most verbs that's a dict or string; screenshot returns a dict with
    the image base64-encoded for the SDK image block; submit_finding
    returns a FindingResult sentinel the loop checks for.
    """
    if name == "page_state":
        return client.state()
    if name == "screenshot":
        png = client.screenshot(full_page=args.get("full_page", False))
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": base64.b64encode(png).decode("ascii"),
            },
        }
    if name == "goto":
        return client.goto(args["url"])
    if name == "reload":
        return client.reload()
    if name == "back":
        return client.back()
    if name == "find_text":
        return {"matches": client.find_text(args["query"])}
    if name == "click_text":
        client.click_text(args["query"], nth=args.get("nth", 0))
        return {"ok": True}
    if name == "click_role":
        client.click_role(args["role"], name=args.get("name"))
        return {"ok": True}
    if name == "fill_label":
        client.fill_label(args["label"], args["value"])
        return {"ok": True}
    if name == "fill_placeholder":
        client.fill_placeholder(args["placeholder"], args["value"])
        return {"ok": True}
    if name == "select_option":
        client.select_option(args["label"], args["option"])
        return {"ok": True}
    if name == "press":
        client.press(args["key"])
        return {"ok": True}
    if name == "type_text":
        client.type_text(args["text"], delay_ms=args.get("delay_ms", 0))
        return {"ok": True}
    if name == "upload_file":
        client.upload_file(args["label"], args["path"])
        return {"ok": True}
    if name == "wait_for_text":
        return {"found": client.wait_for_text(args["text"], args.get("timeout_ms", 10000))}
    if name == "wait_for_url":
        return {"matched": client.wait_for_url(args["pattern"], args.get("timeout_ms", 10000))}
    if name == "synthesize_speech":
        from agent import tts

        path = tts.synthesize(args["text"])
        return {"path": str(path)}
    if name == "submit_finding":
        return FindingResult(success=bool(args["success"]), notes=str(args.get("notes", "")))
    raise ValueError(f"unknown tool: {name}")
