from __future__ import annotations

import shutil
import sys
from typing import Sequence

from .extractor import extract_audio
from .formatters import FORMATTERS
from .utils import check_ffmpeg, get_output_path, is_video, validate_file


def transcribe(
    files: Sequence[str],
    model: str = "base",
    language: str | None = None,
    fmt: str = "txt",
    output: str | None = None,
    stdout: bool = False,
    verbose: bool = False,
) -> int:
    """Transcribe one or more audio/video files. Returns an exit code (0 = success)."""
    import whisper  # lazy — keeps import time fast and lets tests run without whisper

    check_ffmpeg()

    if verbose:
        print(f"Loading Whisper model '{model}'…")

    wmodel = whisper.load_model(model)
    exit_code = 0

    for file_str in files:
        try:
            input_path = validate_file(file_str)
        except (FileNotFoundError, ValueError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            exit_code = 1
            continue

        tmp_dir: str | None = None
        audio_path = input_path

        try:
            if is_video(input_path):
                if verbose:
                    print(f"Extracting audio from '{input_path.name}'…")
                audio_path, tmp_dir = extract_audio(input_path)

            if verbose:
                print(f"Transcribing '{input_path.name}'…")

            whisper_kwargs: dict = {}
            if language:
                whisper_kwargs["language"] = language

            result = wmodel.transcribe(str(audio_path), verbose=verbose or None, **whisper_kwargs)
            segments: list[dict] = result["segments"]

            formats = ["txt", "srt", "vtt"] if fmt == "all" else [fmt]

            for f in formats:
                formatter = FORMATTERS[f]  # type: ignore[index]
                text = formatter(segments)  # type: ignore[operator]

                if stdout:
                    print(text)
                else:
                    out_dir = output if fmt != "all" else None
                    out_path = get_output_path(input_path, out_dir, f)
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    out_path.write_text(text, encoding="utf-8")
                    if verbose:
                        print(f"Saved: {out_path}")
                    else:
                        print(f"  → {out_path}")

        except RuntimeError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            exit_code = 1
        finally:
            if tmp_dir:
                shutil.rmtree(tmp_dir, ignore_errors=True)

    return exit_code
