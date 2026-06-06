from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch


def _make_mock_anthropic(mock_client: MagicMock) -> MagicMock:
    """Return a mock anthropic module whose Anthropic() returns mock_client."""
    mock_module = MagicMock()
    mock_module.Anthropic.return_value = mock_client
    return mock_module


# ── describe_frames ───────────────────────────────────────────────────────────

def test_describe_frames_empty_returns_empty():
    from transcriber.vision import describe_frames

    result = describe_frames([])
    assert result == ""


def test_describe_frames_calls_anthropic(tmp_path: Path):
    frame = tmp_path / "frame_0001.jpg"
    frame.write_bytes(b"\xff\xd8\xff\xd9")  # minimal JPEG stub

    mock_text_block = MagicMock()
    mock_text_block.type = "text"
    mock_text_block.text = "A person works on a car."

    mock_response = MagicMock()
    mock_response.content = [mock_text_block]

    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_response

    with patch.dict(sys.modules, {"anthropic": _make_mock_anthropic(mock_client)}):
        from transcriber.vision import describe_frames

        result = describe_frames([frame])

    assert result == "A person works on a car."
    mock_client.messages.create.assert_called_once()
    call_kwargs = mock_client.messages.create.call_args.kwargs
    assert call_kwargs["model"] == "claude-opus-4-8"


def test_describe_frames_subsamples_when_over_limit(tmp_path: Path):
    frames = []
    for i in range(30):
        f = tmp_path / f"frame_{i:04d}.jpg"
        f.write_bytes(b"\xff\xd8\xff\xd9")
        frames.append(f)

    mock_text_block = MagicMock()
    mock_text_block.type = "text"
    mock_text_block.text = "description"

    mock_response = MagicMock()
    mock_response.content = [mock_text_block]

    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_response

    with patch.dict(sys.modules, {"anthropic": _make_mock_anthropic(mock_client)}):
        from transcriber.vision import describe_frames

        describe_frames(frames, max_frames=20)

    call_kwargs = mock_client.messages.create.call_args.kwargs
    # 20 image blocks + 1 text prompt block
    assert len(call_kwargs["messages"][0]["content"]) == 21
