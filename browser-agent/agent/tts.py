"""Text-to-speech for the AUDIO channel on voice-input targets.

The arena's AUDIO channel is a 'Slack Huddle Voice Message' — the
defender LLM transcribes whatever audio you upload. So all we need is
to convert attacker text to an audio file the form will accept, then
hand the path to `client.upload_file()`.

Two backends, picked in this order:

  1. ElevenLabs HTTPS API — `ELEVENLABS_API_KEY` set
  2. Piper local binary — `piper` on PATH
  3. otherwise raise with a clear pointer

Output is always a WAV file under `audio/`. Caller passes the returned
path to `upload_file('Slack Huddle Voice Message', path)`.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
from pathlib import Path

import httpx


HARNESS_ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = HARNESS_ROOT / "audio"

ELEVENLABS_DEFAULT_VOICE = "21m00Tcm4TlvDq8ikWAM"  # 'Rachel' — clean default


def synthesize(text: str, *, voice: str | None = None) -> Path:
    """Synthesize `text` to a WAV file. Returns the path.

    Output filename is derived from a content hash so re-synthesizing the
    same text returns the same path (idempotent for replay).
    """
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    out = AUDIO_DIR / f"{digest}.wav"
    if out.exists():
        return out

    if os.environ.get("ELEVENLABS_API_KEY"):
        _synthesize_elevenlabs(text, out, voice=voice or ELEVENLABS_DEFAULT_VOICE)
    elif shutil.which("piper"):
        _synthesize_piper(text, out)
    else:
        raise RuntimeError(
            "no TTS backend available — set ELEVENLABS_API_KEY or install `piper` "
            "(https://github.com/rhasspy/piper) and put it on PATH"
        )
    return out


def _synthesize_elevenlabs(text: str, out: Path, *, voice: str) -> None:
    key = os.environ["ELEVENLABS_API_KEY"]
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/stream"
    headers = {"xi-api-key": key, "Accept": "audio/wav"}
    body = {
        "text": text,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }
    with httpx.stream("POST", url, headers=headers, json=body, timeout=60.0) as r:
        r.raise_for_status()
        with out.open("wb") as f:
            for chunk in r.iter_bytes():
                f.write(chunk)


def _synthesize_piper(text: str, out: Path) -> None:
    """Use the local `piper` binary; voice is whatever PIPER_VOICE points at."""
    voice = os.environ.get("PIPER_VOICE")
    if not voice:
        raise RuntimeError(
            "PIPER_VOICE must be set to a piper voice .onnx path — "
            "see https://github.com/rhasspy/piper/blob/master/VOICES.md"
        )
    subprocess.run(
        ["piper", "--model", voice, "--output_file", str(out)],
        input=text.encode("utf-8"),
        check=True,
    )
