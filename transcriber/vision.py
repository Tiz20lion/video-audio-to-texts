from __future__ import annotations

import base64
import shutil
import subprocess
import tempfile
from pathlib import Path


def extract_frames(video_path: Path, fps: float = 0.5) -> tuple[list[Path], str]:
    """Extract frames at given fps using FFmpeg. Returns (sorted frame paths, tmp_dir)."""
    tmp_dir = tempfile.mkdtemp(prefix="tiz_vision_")
    out_pattern = str(Path(tmp_dir) / "frame_%04d.jpg")
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vf", f"fps={fps}",
        "-q:v", "2",
        out_pattern,
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    frames = sorted(Path(tmp_dir).glob("frame_*.jpg"))
    return frames, tmp_dir


def describe_frames(frames: list[Path], api_key: str | None = None, max_frames: int = 20) -> str:
    """Send up to max_frames to Claude vision API and return a visual description."""
    if not frames:
        return ""

    # Sub-sample evenly if too many frames
    if len(frames) > max_frames:
        step = len(frames) / max_frames
        frames = [frames[int(i * step)] for i in range(max_frames)]

    import anthropic  # lazy import — keeps startup fast when --vision not used

    client = anthropic.Anthropic(api_key=api_key)

    content: list[dict] = []
    for frame in frames:
        data = base64.standard_b64encode(frame.read_bytes()).decode()
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": "image/jpeg", "data": data},
        })

    content.append({
        "type": "text",
        "text": (
            "These are frames sampled from a video. "
            "Describe what is visually happening: people, actions, objects, setting, "
            "and any text or graphics visible on screen. "
            "Be concise and factual."
        ),
    })

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        messages=[{"role": "user", "content": content}],
    )
    return next(b.text for b in response.content if b.type == "text")


def visual_description(video_path: Path, fps: float = 0.5, api_key: str | None = None) -> str:
    """Full pipeline: extract frames, describe with Claude, clean up. Returns description."""
    frames, tmp_dir = extract_frames(video_path, fps=fps)
    try:
        return describe_frames(frames, api_key=api_key)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
