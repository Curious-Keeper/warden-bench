"""Pre-submit dedup + per-target attempt store.

Some targets reject 'highly similar submissions'. The warden dedupes
exact prompts per (ip, level) with HTTP 409. Filtering near-duplicates
client-side saves submission budget and keeps the agent from looping
on the same angle.

Two layers:

  * **Exact match** (always on) — sha256 of normalized key fields. O(1)
    lookup against a per-target seen set in `arena-state.json`.
  * **Embedding similarity** (opt-in, requires `voyageai`) — cosine
    against past attempt embeddings. Rejects when cosine > threshold.

Callers integrate via:

    store = AttemptStore('warden')
    if store.is_duplicate(key) or store.is_similar(text):
        return {'rejected': True, 'reason': 'duplicate'}
    store.record(key=..., text=..., result=...)
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any


HARNESS_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STATE_PATH = HARNESS_ROOT / "arena-state.json"
DEFAULT_SIMILARITY_THRESHOLD = 0.88


def _normalize(text: str) -> str:
    """Lowercase + collapse whitespace + strip — same as warden's filter."""
    return re.sub(r"\s+", " ", text.strip().lower())


def _hash_key(fields: dict[str, Any]) -> str:
    """Stable sha256 of a normalized field dict."""
    norm = {k: _normalize(str(v)) for k, v in sorted(fields.items())}
    blob = json.dumps(norm, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


class AttemptStore:
    """Per-target attempt log keyed by content hash.

    Layout in `arena-state.json`:

        {
          "some_target": {
            "attempts": [
              {"hash": "...", "ts": "...", "key": {...}, "text": "...",
               "embedding": [...], "result": {...}}
            ]
          },
          "warden": {...}
        }
    """

    def __init__(
        self,
        target: str,
        path: Path | str = DEFAULT_STATE_PATH,
        similarity_threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    ) -> None:
        self.target = target
        self.path = Path(path)
        self.similarity_threshold = similarity_threshold
        self._data: dict[str, Any] = self._load()

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def _save(self) -> None:
        self.path.write_text(
            json.dumps(self._data, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )

    def _bucket(self) -> dict[str, Any]:
        return self._data.setdefault(self.target, {"attempts": []})

    # ------------------- exact-match dedup -----------------------------

    def is_duplicate(self, key: dict[str, Any]) -> bool:
        h = _hash_key(key)
        return any(a["hash"] == h for a in self._bucket()["attempts"])

    # ------------------- embedding dedup (opt-in) ----------------------

    def is_similar(self, text: str, embedder: Any | None = None) -> bool:
        """Return True if `text`'s embedding is too close to a past attempt.

        `embedder` is a callable str → list[float]. If None, falls back to
        `_default_embedder` (Voyage if VOYAGE_API_KEY set; raises if not).
        Use `record(..., embedding=embedder(text))` so future calls have
        comparable vectors.
        """
        embedder = embedder or _default_embedder
        emb = embedder(text)
        for a in self._bucket()["attempts"]:
            past = a.get("embedding")
            if not past:
                continue
            if _cosine(emb, past) >= self.similarity_threshold:
                return True
        return False

    # ------------------- record + read ---------------------------------

    def record(
        self,
        *,
        key: dict[str, Any],
        text: str | None = None,
        embedding: list[float] | None = None,
        result: dict[str, Any] | None = None,
    ) -> str:
        h = _hash_key(key)
        import time

        self._bucket()["attempts"].append(
            {
                "hash": h,
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "key": key,
                "text": text,
                "embedding": embedding,
                "result": result,
            }
        )
        self._save()
        return h

    def attempts(self) -> list[dict[str, Any]]:
        return list(self._bucket()["attempts"])

    def successful(self) -> list[dict[str, Any]]:
        return [
            a
            for a in self._bucket()["attempts"]
            if (a.get("result") or {}).get("success") is True
        ]

    def exhausted_angles(self, limit: int = 20) -> list[dict[str, Any]]:
        """Return the most-recent failed attempts, FIFO-trimmed.

        Used to feed PAIR-style context into the next agent loop run via
        `loop.run(extra_user_context=...)`.
        """
        failures = [
            a
            for a in self._bucket()["attempts"]
            if (a.get("result") or {}).get("success") is not True
        ]
        return failures[-limit:]


# ----------------------------- helpers ---------------------------------


def _cosine(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def _default_embedder(text: str) -> list[float]:
    """Voyage embedding (voyage-3-lite, 512 dims). Requires VOYAGE_API_KEY."""
    key = os.environ.get("VOYAGE_API_KEY")
    if not key:
        raise RuntimeError(
            "embedding dedup requires VOYAGE_API_KEY (or pass `embedder=` explicitly)"
        )
    try:
        import voyageai  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError(
            "voyageai not installed; pip install voyageai or pass an explicit embedder"
        ) from exc
    vc = voyageai.Client(api_key=key)
    return vc.embed([text], model="voyage-3-lite", input_type="document").embeddings[0]
