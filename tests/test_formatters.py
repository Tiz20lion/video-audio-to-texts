from __future__ import annotations

from transcriber.formatters import to_srt, to_txt, to_vtt

SEGMENTS = [
    {"start": 0.0, "end": 3.5, "text": " Hello world"},
    {"start": 3.5, "end": 7.0, "text": " This is a test"},
]

HOUR_SEGMENT = [
    {"start": 3661.5, "end": 3665.0, "text": " Late in the file"},
]


# ── to_txt ────────────────────────────────────────────────────────────────────

def test_txt_contains_all_text():
    result = to_txt(SEGMENTS)
    assert "Hello world" in result
    assert "This is a test" in result


def test_txt_strips_leading_space():
    result = to_txt(SEGMENTS)
    for line in result.splitlines():
        assert not line.startswith(" ")


def test_txt_empty_segments():
    assert to_txt([]) == ""


# ── to_srt ────────────────────────────────────────────────────────────────────

def test_srt_index_starts_at_one():
    lines = to_srt(SEGMENTS).split("\n")
    assert lines[0] == "1"


def test_srt_contains_arrow():
    result = to_srt(SEGMENTS)
    assert "-->" in result


def test_srt_timestamp_format():
    result = to_srt(SEGMENTS)
    assert "00:00:00,000 --> 00:00:03,500" in result
    assert "00:00:03,500 --> 00:00:07,000" in result


def test_srt_hours_and_milliseconds():
    result = to_srt(HOUR_SEGMENT)
    assert "01:01:01,500" in result


def test_srt_second_block_index():
    result = to_srt(SEGMENTS)
    blocks = result.split("\n\n")
    assert blocks[1].startswith("2\n")


def test_srt_empty_segments():
    assert to_srt([]) == ""


# ── to_vtt ────────────────────────────────────────────────────────────────────

def test_vtt_starts_with_header():
    assert to_vtt(SEGMENTS).startswith("WEBVTT")


def test_vtt_uses_dot_not_comma():
    body = to_vtt(SEGMENTS).split("WEBVTT", 1)[1]
    assert "," not in body


def test_vtt_timestamp_format():
    result = to_vtt(SEGMENTS)
    assert "00:00:00.000 --> 00:00:03.500" in result


def test_vtt_empty_segments():
    result = to_vtt([])
    assert result.startswith("WEBVTT")
