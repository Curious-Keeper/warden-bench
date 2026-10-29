"""JSONL event logging + run-level cost accounting.

Mirrors the shape of `operator/warden-probes-N.jsonl`: one event
per line, with a `kind` discriminator. Loaders can grep by kind, by
target, or by run.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


HARNESS_ROOT = Path(__file__).resolve().parent.parent


def _default_log_path() -> Path:
    return HARNESS_ROOT / "arena-probes.jsonl"


@dataclass
class TokenTally:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_creation_tokens: int = 0

    def add(self, usage: Any) -> None:
        self.input_tokens += getattr(usage, "input_tokens", 0) or 0
        self.output_tokens += getattr(usage, "output_tokens", 0) or 0
        self.cache_read_tokens += getattr(usage, "cache_read_input_tokens", 0) or 0
        self.cache_creation_tokens += getattr(usage, "cache_creation_input_tokens", 0) or 0

    def as_dict(self) -> dict[str, int]:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cache_read_tokens": self.cache_read_tokens,
            "cache_creation_tokens": self.cache_creation_tokens,
        }


@dataclass
class RunLog:
    target: str
    run_id: str = field(default_factory=lambda: f"{int(time.time())}")
    path: Path = field(default_factory=_default_log_path)
    tally: TokenTally = field(default_factory=TokenTally)

    def event(self, kind: str, **fields: Any) -> None:
        record = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "run_id": self.run_id,
            "target": self.target,
            "kind": kind,
            **fields,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")

    def cost_summary(self, sonnet_in: float = 3.0, sonnet_out: float = 15.0) -> dict[str, Any]:
        """USD estimate using Sonnet 4.6 list rates ($/MTok). Override for Opus."""
        t = self.tally
        usd = (
            (t.input_tokens / 1_000_000) * sonnet_in
            + (t.output_tokens / 1_000_000) * sonnet_out
            + (t.cache_read_tokens / 1_000_000) * (sonnet_in * 0.1)
            + (t.cache_creation_tokens / 1_000_000) * (sonnet_in * 1.25)
        )
        return {**t.as_dict(), "usd_estimate": round(usd, 4)}


def rotate_log(path: Path | None = None) -> Path | None:
    """Move arena-probes.jsonl → arena-probes-N.jsonl. Mirrors cfp pattern."""
    src = path or _default_log_path()
    if not src.exists():
        return None
    n = 0
    while True:
        candidate = src.with_name(f"{src.stem}-{n}{src.suffix}")
        if not candidate.exists():
            os.replace(src, candidate)
            return candidate
        n += 1
