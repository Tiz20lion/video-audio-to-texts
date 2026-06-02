# Contributing

## Development setup

```bash
git clone https://github.com/tiz20lion/video-audio-to-texts
cd video-audio-to-texts
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Running tests

```bash
pytest
```

Tests are designed to run without FFmpeg or Whisper installed — the formatter and utility tests are pure Python, and CLI tests mock the transcription call.

## Linting and type checking

```bash
ruff check transcriber/ tests/
mypy transcriber/
```

## Project layout

```
transcriber/
├── __init__.py      version constant
├── __main__.py      python -m transcriber entry
├── cli.py           click CLI definitions
├── core.py          transcribe() — main orchestration
├── extractor.py     FFmpeg audio extraction
├── formatters.py    txt / srt / vtt output
└── utils.py         validation and path helpers
```

## Adding a new output format

1. Add a `to_<fmt>(segments)` function in `formatters.py`
2. Register it in the `FORMATTERS` dict
3. Add the format name to `FORMAT_CHOICES` in `cli.py`
4. Add tests in `tests/test_formatters.py`

## Submitting a PR

- Keep PRs focused — one feature or fix per PR
- Add or update tests for any changed behaviour
- Make sure `pytest`, `ruff check`, and `mypy` all pass before opening the PR
