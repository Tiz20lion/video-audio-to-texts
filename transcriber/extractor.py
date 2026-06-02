from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


def extract_audio(input_path: Path) -> tuple[Path, str]:
    """Extract audio track from a video file to a 16 kHz mono WAV.

    Returns (wav_path, tmp_dir) — caller is responsible for removing tmp_dir.
    """
    tmp_dir = tempfile.mkdtemp(prefix="tiz_mp4_txt_")
    out_path = Path(tmp_dir) / (input_path.stem + ".wav")

    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        str(out_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"FFmpeg failed to extract audio from '{input_path.name}':\n{result.stderr.strip()}"
        )

    return out_path, tmp_dir
