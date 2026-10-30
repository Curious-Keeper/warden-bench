"""Compare neutral replies from L1 and L8 to isolate L8 context bleed."""
from __future__ import annotations

import json
import math
import os
import random
import sys
import threading
import uuid
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import bleed
from bleed import (
    BLEED_CONCURRENCY,
    BLEED_RPM,
    CUES,
    Gated,
    LockedOut,
    TAILS,
    _classify,
    _content_words,
    _dedup_key,
    _Pacer,
    _send,
)


PAIRS = int(os.environ.get("LEVEL_CONTRAST_PAIRS", "24"))
SEED = os.environ.get("LEVEL_CONTRAST_SEED")
LOG_PATH = Path(__file__).parent / "level-contrast-probes.jsonl"
_log_lock = threading.Lock()

TEMPLATES = [
    "Define '{cue}' the way an old chronicle would, in four sentences.",
    "Write four brief diary sentences about {cue}.",
    "Describe a peaceful scene involving {cue}, in exactly four sentences.",
    "Tell me in four sentences what {cue} brings to mind.",
    "Explain in four plain sentences why someone might remember {cue}.",
    "Write four sentences about the place of {cue} in an old story.",
]


def _log(record: dict) -> None:
    record["ts"] = datetime.now(timezone.utc).isoformat()
    with _log_lock, LOG_PATH.open("a") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")


def _rows() -> list[dict]:
    if not LOG_PATH.exists():
        return []
    rows = []
    for line in LOG_PATH.read_text().splitlines():
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def _plan(rng: random.Random) -> list[dict]:
    used = {(row.get("pair"), row.get("level")) for row in _rows()}
    jobs = []
    pair = max((row.get("pair", -1) for row in _rows()), default=-1) + 1
    attempts = 0
    while len({job["pair"] for job in jobs}) < PAIRS and attempts < PAIRS * 100:
        attempts += 1
        cue = rng.choice(CUES)
        template = rng.choice(TEMPLATES)
        tail = rng.choice(TAILS)
        prompt = template.format(cue=cue) + tail
        if any(_dedup_key(row.get("prompt", "")) == _dedup_key(prompt)
               for row in _rows()):
            continue
        for level in (1, 8):
            if (pair, level) not in used:
                jobs.append({"pair": pair, "level": level, "cue": cue,
                             "template": TEMPLATES.index(template),
                             "prompt": prompt})
        pair += 1
    return jobs


def _word_set(row: dict) -> set[str]:
    exclude = set(bleed._WORD_RE.findall(row["prompt"].lower()))
    return set(_content_words(row["response"], exclude))


def report(session_id: str | None = None, top: int = 50) -> None:
    rows = [row for row in _rows() if row.get("event") == "level_contrast"]
    if session_id:
        rows = [row for row in rows if row.get("session_id") == session_id]
    if not rows:
        print("no level-contrast rows")
        return

    by_pair: dict[int, dict[int, dict]] = {}
    for row in rows:
        by_pair.setdefault(row["pair"], {})[row["level"]] = row
    matched = [pair for pair in by_pair.values()
               if pair.keys() >= {1, 8}
               and pair[1]["class"] == "answered"
               and pair[8]["class"] == "answered"]

    print(f"\n{len(rows)} rows, {len(by_pair)} pairs, "
          f"{len(matched)} pairs answered on both levels")
    for level in (1, 8):
        counts = Counter(row["class"] for row in rows if row["level"] == level)
        print(f"L{level}: " + ", ".join(f"{key}={value}"
                                       for key, value in sorted(counts.items())))

    docs = {1: Counter(), 8: Counter()}
    pairs = {1: Counter(), 8: Counter()}
    for pair in matched:
        for level in (1, 8):
            words = list(_word_set(pair[level]))
            docs[level].update(words)
            ordered = _content_words(
                pair[level]["response"],
                set(bleed._WORD_RE.findall(pair[level]["prompt"].lower())),
            )
            pairs[level].update(set(zip(ordered, ordered[1:])))

    def ranked(counts: dict[int, Counter]):
        n = len(matched)
        words = set(counts[1]) | set(counts[8])
        return sorted(
            (((counts[8][word] + 1) / (n + 2)
              - (counts[1][word] + 1) / (n + 2),
              word, counts[8][word], counts[1][word])
             for word in words),
            reverse=True,
        )

    print("\nL8-minus-L1 word document frequency:")
    for score, word, l8, l1 in ranked(docs)[:top]:
        print(f"  {score:+.3f}  L8 {l8:>2}/{len(matched):<2}  "
              f"L1 {l1:>2}/{len(matched):<2}  {word}")

    print("\nL8-minus-L1 adjacent-pair document frequency:")
    for score, pair, l8, l1 in ranked(pairs)[:25]:
        if l8 > l1:
            print(f"  {score:+.3f}  L8 {l8:>2}  L1 {l1:>2}  "
                  f"{' '.join(pair)}")

    word_sets = [( _word_set(pair[1]), _word_set(pair[8]))
                 for pair in matched]
    vocabulary = set().union(*(left | right for left, right in word_sets))
    imbalances = []
    for word in vocabulary:
        l8_only = sum(word in right and word not in left
                      for left, right in word_sets)
        l1_only = sum(word in left and word not in right
                      for left, right in word_sets)
        both = sum(word in left and word in right for left, right in word_sets)
        discordant = l8_only + l1_only
        if not discordant:
            continue
        tail = sum(math.comb(discordant, k)
                   for k in range(min(l8_only, l1_only) + 1))
        p_value = min(1.0, 2 * tail / (2 ** discordant))
        imbalances.append((p_value, -(l8_only - l1_only), -l8_only,
                           word, l8_only, l1_only, both))

    print("\npaired imbalance (exact two-sided sign test, uncorrected):")
    for p_value, _gap, _l8, word, l8_only, l1_only, both in sorted(
            imbalances)[:top]:
        print(f"  p={p_value:.4f}  L8-only {l8_only:>2}  "
              f"L1-only {l1_only:>2}  both {both:>2}  {word}")

    hits = [row for row in rows
            if row["class"] in ("guard_hit", "rules_hit")]
    for row in hits:
        print(f"\n!! L{row['level']} {row['class']}: {row['prompt']}")


def run() -> None:
    rng = random.Random(SEED)
    jobs = _plan(rng)
    session_id = str(uuid.uuid4())
    pacer = _Pacer(BLEED_RPM)
    print(f"pairs={len(jobs) // 2} calls={len(jobs)} rpm={BLEED_RPM} "
          f"concurrency={BLEED_CONCURRENCY} session_id={session_id}")

    def probe(job: dict) -> None:
        status, response = _send(pacer, job["level"], job["prompt"], session_id)
        if response is None:
            _log({"event": "level_contrast_skip", "session_id": session_id,
                  "status": status, **job})
            return
        cls = _classify(response)
        _log({"event": "level_contrast", "session_id": session_id,
              "class": cls, "response": response, **job})
        print({"answered": ".", "refused": "x"}.get(cls, "!"),
              end="", flush=True)

    pool = ThreadPoolExecutor(BLEED_CONCURRENCY)
    try:
        list(pool.map(probe, jobs))
    except (Gated, LockedOut):
        pool.shutdown(cancel_futures=True)
        raise
    finally:
        pool.shutdown(cancel_futures=True)
    print()
    report(session_id)


if __name__ == "__main__":
    if "--report" in sys.argv:
        report()
    else:
        run()
