from __future__ import annotations

from pathlib import Path

import pytest

from transcriber.utils import get_output_path, is_video, validate_file

# ── validate_file ─────────────────────────────────────────────────────────────

def test_validate_missing_file():
    with pytest.raises(FileNotFoundError, match="not found"):
        validate_file("/nonexistent/path/file.mp4")


def test_validate_unsupported_extension(tmp_path: Path):
    f = tmp_path / "clip.avi"
    f.write_bytes(b"x")
    with pytest.raises(ValueError, match="Unsupported"):
        validate_file(str(f))


def test_validate_directory(tmp_path: Path):
    with pytest.raises(ValueError, match="Not a file"):
        validate_file(str(tmp_path))


@pytest.mark.parametrize("ext", [".mp4", ".mp3", ".mov", ".mkv", ".wav", ".m4a", ".webm"])
def test_validate_supported_extensions(tmp_path: Path, ext: str):
    f = tmp_path / f"file{ext}"
    f.write_bytes(b"fake")
    result = validate_file(str(f))
    assert result == f


# ── is_video ──────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("name", ["clip.mp4", "clip.mov", "clip.mkv", "clip.webm"])
def test_is_video_true(name: str):
    assert is_video(Path(name)) is True


@pytest.mark.parametrize("name", ["audio.mp3", "audio.wav", "audio.m4a"])
def test_is_video_false(name: str):
    assert is_video(Path(name)) is False


# ── get_output_path ───────────────────────────────────────────────────────────

def test_output_path_default(tmp_path: Path):
    inp = tmp_path / "video.mp4"
    assert get_output_path(inp, None, "txt") == tmp_path / "video.txt"


def test_output_path_srt(tmp_path: Path):
    inp = tmp_path / "lecture.mp4"
    assert get_output_path(inp, None, "srt") == tmp_path / "lecture.srt"


def test_output_path_to_existing_dir(tmp_path: Path):
    inp = tmp_path / "video.mp4"
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    result = get_output_path(inp, str(out_dir), "srt")
    assert result == out_dir / "video.srt"


def test_output_path_explicit_file(tmp_path: Path):
    inp = tmp_path / "video.mp4"
    explicit = str(tmp_path / "my_transcript.txt")
    assert get_output_path(inp, explicit, "txt") == Path(explicit)
