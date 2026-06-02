# tiz-mp4-txt

Local audio/video transcription — no cloud, no subscriptions.  
Drop in a file, get a transcript. Powered by [OpenAI Whisper](https://github.com/openai/whisper).

[![CI](https://github.com/tiz20lion/video-audio-to-texts/actions/workflows/ci.yml/badge.svg)](https://github.com/tiz20lion/video-audio-to-texts/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

---

## Features

- Transcribes `.mp4`, `.mp3`, `.mov`, `.mkv`, `.wav`, `.m4a`, `.webm`
- Output as plain text (`.txt`), subtitles (`.srt`), or WebVTT (`.vtt`) — or all three at once
- Choose Whisper model size: `tiny` → `base` → `small` → `medium` → `large`
- Works entirely offline after the first model download
- Single command, zero configuration required

---

## Requirements

- Python 3.9 or later
- [FFmpeg](https://ffmpeg.org/download.html) installed and on your `PATH`

### Install FFmpeg

| OS | Command |
|---|---|
| macOS | `brew install ffmpeg` |
| Ubuntu / Debian | `sudo apt install ffmpeg` |
| Windows | Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH |

---

## Installation

```bash
pip install tiz-mp4-txt
```

### From source

```bash
git clone https://github.com/tiz20lion/video-audio-to-texts
cd video-audio-to-texts
pip install -e .
```

### Docker

```bash
# Build
docker build -t tiz-mp4-txt .

# Run (mount the directory containing your file)
docker run --rm -v $(pwd):/data tiz-mp4-txt video.mp4
```

---

## Quick Start

```bash
# Transcribe a video — saves video.txt in the same folder
tiz-mp4-txt video.mp4

# Get a subtitle file
tiz-mp4-txt --format srt lecture.mp4

# Get all three formats at once
tiz-mp4-txt --format all meeting.mp4

# Use a more accurate model
tiz-mp4-txt --model large interview.mp3

# Skip language detection (faster)
tiz-mp4-txt --language en podcast.mp3

# Print to stdout (pipe-friendly)
tiz-mp4-txt --stdout audio.wav | grep "important phrase"

# Transcribe multiple files
tiz-mp4-txt clip1.mp4 clip2.mp4 clip3.mp4

# Save output to a specific directory
tiz-mp4-txt --output ./transcripts/ video.mp4
```

---

## CLI Reference

```
tiz-mp4-txt [OPTIONS] FILE [FILE...]

Arguments:
  FILE              Path to one or more audio or video files

Options:
  --model           Whisper model [tiny|base|small|medium|large]  (default: base)
  --language CODE   Language code (e.g. en, fr, yo). Auto-detected if omitted.
  --format          Output format [txt|srt|vtt|all]  (default: txt)
  --output PATH     Output directory or file path
  --stdout          Print transcript to stdout instead of saving
  --verbose         Show progress and debug info
  --version         Show version and exit
  -h, --help        Show this message and exit
```

### Model sizes

| Model | Size | Speed | Accuracy |
|---|---|---|---|
| `tiny` | ~39 MB | Fastest | Basic |
| `base` | ~74 MB | Fast | Good (default) |
| `small` | ~244 MB | Moderate | Better |
| `medium` | ~769 MB | Slow | Great |
| `large` | ~1.5 GB | Slowest | Best |

Models are downloaded automatically on first use and cached in `~/.cache/whisper`.

---

## Programmatic Use

```python
from transcriber.core import transcribe

exit_code = transcribe(
    files=["lecture.mp4"],
    model="small",
    language="en",
    fmt="srt",
    verbose=True,
)
```

---

## Performance

On a modern CPU (no GPU required):

| File length | Model | Approx. time |
|---|---|---|
| 5 min | base | ~20 s |
| 10 min | base | ~45 s |
| 60 min | base | ~5 min |

GPU acceleration is used automatically if CUDA is available.

---

## License

[MIT](LICENSE)
