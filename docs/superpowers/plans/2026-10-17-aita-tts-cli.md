# AITA TTS CLI Plan

Spec: none (user skipped brainstorming questions). Rulings are provisional.

## Global Constraints
- Simplest thing that works; no extra abstractions.
- No emojis, no em dashes in code or docs.
- Notebook `Azure AITA Text-To-Speech.ipynb` stays untouched.
- Tests run fully offline (Azure SDK faked); real key not required.
- Default voice `en-US-KaiNeural`; MP3 format `Audio24Khz160KBitRateMonoMp3` when output ends in `.mp3`.
- Env vars: AZURE_SPEECH_KEY, AZURE_SERVICE_REGION, FILE_PATH, optional AZURE_SPEECH_VOICE; loaded from `env.env` then `.env`.

### Task 1: CLI, tests, CI, docs
- `aita_tts.py`: `read_text_file(path)`, `synthesize(text, key, region, voice, output=None)` (file or speaker; Canceled raises RuntimeError), `main(argv=None)` with argparse (`input` optional falling back to FILE_PATH, `-o/--output`, `--voice`). Exit 2 for missing config/empty input, 1 for synthesis failure. Never print story text.
- `tests/test_aita_tts.py`: offline pytest covering mp3 file output, speaker output, canceled error, missing env exit 2, FILE_PATH fallback, empty file error.
- `requirements-dev.txt`, `.gitignore`, `samples/example_story.txt`, `.github/workflows/tests.yml` (pytest, Python 3.12), README usage + tests sections.
