from __future__ import annotations

import sys

import click

from . import __version__
from .core import transcribe

MODEL_CHOICES = ["tiny", "base", "small", "medium", "large"]
FORMAT_CHOICES = ["txt", "srt", "vtt", "all"]


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("files", nargs=-1, required=True, metavar="FILE [FILE...]")
@click.option(
    "--model",
    default="base",
    show_default=True,
    type=click.Choice(MODEL_CHOICES),
    help="Whisper model size (larger = more accurate, slower).",
)
@click.option(
    "--language",
    default=None,
    metavar="CODE",
    help="Language code (e.g. en, fr, yo). Auto-detected if omitted.",
)
@click.option(
    "--format",
    "fmt",
    default="txt",
    show_default=True,
    type=click.Choice(FORMAT_CHOICES),
    help="Output format.",
)
@click.option(
    "--output",
    default=None,
    metavar="PATH",
    help="Output directory or file path (defaults to same directory as input).",
)
@click.option(
    "--stdout",
    is_flag=True,
    default=False,
    help="Print transcript to stdout instead of saving to a file.",
)
@click.option(
    "--verbose",
    is_flag=True,
    default=False,
    help="Show progress and debug information.",
)
@click.option(
    "--vision",
    is_flag=True,
    default=False,
    help="Add visual description using Claude vision API (requires ANTHROPIC_API_KEY).",
)
@click.option(
    "--vision-fps",
    default=0.5,
    show_default=True,
    type=float,
    metavar="FPS",
    help="Frames per second to sample for vision analysis.",
)
@click.version_option(__version__, prog_name="tiz-mp4-txt")
def main(
    files: tuple[str, ...],
    model: str,
    language: str | None,
    fmt: str,
    output: str | None,
    stdout: bool,
    verbose: bool,
    vision: bool,
    vision_fps: float,
) -> None:
    """Transcribe audio or video files to text using OpenAI Whisper.

    \b
    Supported formats: .mp4  .mp3  .mov  .mkv  .wav  .m4a  .webm

    \b
    Examples:
      tiz-mp4-txt video.mp4
      tiz-mp4-txt --format srt lecture.mp4
      tiz-mp4-txt --format all --output ./captions/ video.mp4
      tiz-mp4-txt --model large --language en interview.mp3
      tiz-mp4-txt --stdout podcast.mp3 | grep keyword
      tiz-mp4-txt clip1.mp4 clip2.mp4 clip3.mp4
      tiz-mp4-txt --vision video.mp4
    """
    import os

    code = transcribe(
        files=files,
        model=model,
        language=language,
        fmt=fmt,
        output=output,
        stdout=stdout,
        verbose=verbose,
        vision=vision,
        vision_fps=vision_fps,
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )
    sys.exit(code)
