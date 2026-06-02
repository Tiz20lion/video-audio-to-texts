from __future__ import annotations

import shutil
import sys
from pathlib import Path

SUPPORTED_EXTENSIONS = {".mp4", ".mp3", ".mov", ".mkv", ".wav", ".m4a", ".webm"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm"}
OUTPUT_FORMATS = {"txt", "srt", "vtt", "all"}


def validate_file(path: str) -> Path:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not p.is_file():
        raise ValueError(f"Not a file: {path}")
    suffix = p.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(f"Unsupported file type '{p.suffix}'. Supported: {supported}")
    return p


def check_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        print(
            "Error: FFmpeg is not installed or not found on PATH.\n"
            "Install it from https://ffmpeg.org/download.html and try again.",
            file=sys.stderr,
        )
        sys.exit(1)


def is_video(path: Path) -> bool:
    return path.suffix.lower() in VIDEO_EXTENSIONS


def get_output_path(input_path: Path, output: str | None, fmt: str) -> Path:
    ext = f".{fmt}"
    if output is None:
        return input_path.with_suffix(ext)
    out = Path(output)
    if out.is_dir():
        return out / input_path.with_suffix(ext).name
    return out
