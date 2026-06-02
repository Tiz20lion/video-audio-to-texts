from __future__ import annotations


def _fmt_srt_ts(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = round((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _fmt_vtt_ts(seconds: float) -> str:
    return _fmt_srt_ts(seconds).replace(",", ".")


def to_txt(segments: list[dict]) -> str:
    return "\n".join(seg["text"].strip() for seg in segments)


def to_srt(segments: list[dict]) -> str:
    blocks: list[str] = []
    for i, seg in enumerate(segments, 1):
        start = _fmt_srt_ts(seg["start"])
        end = _fmt_srt_ts(seg["end"])
        text = seg["text"].strip()
        blocks.append(f"{i}\n{start} --> {end}\n{text}")
    return "\n\n".join(blocks)


def to_vtt(segments: list[dict]) -> str:
    lines = ["WEBVTT", ""]
    for seg in segments:
        start = _fmt_vtt_ts(seg["start"])
        end = _fmt_vtt_ts(seg["end"])
        text = seg["text"].strip()
        lines.append(f"{start} --> {end}\n{text}")
        lines.append("")
    return "\n".join(lines)


FORMATTERS: dict[str, object] = {
    "txt": to_txt,
    "srt": to_srt,
    "vtt": to_vtt,
}
