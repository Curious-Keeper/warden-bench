"""Target adapters — per-webapp glue.

Each adapter encapsulates what's specific to a single webapp:

  * BASE_URL / LOGIN_URL — entry points
  * is_logged_in(client) — poll callback for serve.py --login
  * SYSTEM_PROMPT — the agent loop's system prompt for this target
  * Optional helpers — target-specific actions like submit_attack(),
    current_bounty_status(), solve_level(), etc.

The base Target class below is a structural type. Adapters inherit it
and override what they need; the registry below lets the CLI look them
up by short name.
"""

from __future__ import annotations

import importlib
from typing import Any, Protocol


class Target(Protocol):
    BASE_URL: str
    LOGIN_URL: str
    SYSTEM_PROMPT: str

    @staticmethod
    def is_logged_in(client: Any) -> bool: ...


_REGISTRY = {
    "warden": "targets.warden",
}


def get_target(name: str) -> Any:
    """Look up a target adapter module by short name."""
    if name not in _REGISTRY:
        raise KeyError(
            f"unknown target {name!r}. known: {', '.join(sorted(_REGISTRY))}"
        )
    return importlib.import_module(_REGISTRY[name])


def list_targets() -> list[str]:
    return sorted(_REGISTRY)
