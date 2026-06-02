from __future__ import annotations

import wave
from pathlib import Path

import pytest


@pytest.fixture
def sample_wav(tmp_path: Path) -> Path:
    """1-second silent 16 kHz mono WAV — no external tools needed."""
    wav_path = tmp_path / "sample.wav"
    sample_rate = 16000
    with wave.open(str(wav_path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b"\x00\x00" * sample_rate)
    return wav_path


@pytest.fixture
def sample_mp4(tmp_path: Path) -> Path:
    """Fake .mp4 file for extension/validation tests (not real video)."""
    p = tmp_path / "sample.mp4"
    p.write_bytes(b"\x00" * 64)
    return p
