from __future__ import annotations

from unittest import mock

import pytest
from click.testing import CliRunner

from transcriber.cli import main


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ── help / version ────────────────────────────────────────────────────────────

def test_help(runner: CliRunner):
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Whisper" in result.output or "transcrib" in result.output.lower()


def test_help_short_flag(runner: CliRunner):
    result = runner.invoke(main, ["-h"])
    assert result.exit_code == 0


def test_version(runner: CliRunner):
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "tiz-mp4-txt" in result.output
    assert "0.1.0" in result.output


# ── argument / option validation ──────────────────────────────────────────────

def test_no_files_exits_nonzero(runner: CliRunner):
    result = runner.invoke(main, [])
    assert result.exit_code != 0


def test_invalid_model(runner: CliRunner):
    result = runner.invoke(main, ["--model", "gigantic", "file.mp4"])
    assert result.exit_code != 0
    assert "gigantic" in result.output or "invalid" in result.output.lower()


def test_invalid_format(runner: CliRunner):
    result = runner.invoke(main, ["--format", "xml", "file.mp4"])
    assert result.exit_code != 0


# ── core path (mocked) ────────────────────────────────────────────────────────

def test_nonexistent_file_returns_exit_1(runner: CliRunner):
    with mock.patch("transcriber.cli.transcribe", return_value=1) as mock_tx:
        result = runner.invoke(main, ["/no/such/file.mp4"])
    assert result.exit_code == 1
    mock_tx.assert_called_once()


def test_transcribe_called_with_correct_args(runner: CliRunner, tmp_path):
    fake_mp3 = tmp_path / "audio.mp3"
    fake_mp3.write_bytes(b"\xff\xfb" + b"\x00" * 64)

    with mock.patch("transcriber.cli.transcribe", return_value=0) as mock_tx:
        result = runner.invoke(
            main,
            [
                "--model", "small",
                "--language", "en",
                "--format", "srt",
                "--verbose",
                str(fake_mp3),
            ],
        )

    assert result.exit_code == 0
    mock_tx.assert_called_once_with(
        files=(str(fake_mp3),),
        model="small",
        language="en",
        fmt="srt",
        output=None,
        stdout=False,
        verbose=True,
    )


def test_stdout_flag_passed_through(runner: CliRunner, tmp_path):
    fake = tmp_path / "audio.wav"
    fake.write_bytes(b"\x00" * 64)

    with mock.patch("transcriber.cli.transcribe", return_value=0) as mock_tx:
        runner.invoke(main, ["--stdout", str(fake)])

    _, kwargs = mock_tx.call_args
    assert kwargs["stdout"] is True
