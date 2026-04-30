# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VoiceDocs is a Windows-focused voice-to-text application for frequent short Japanese input (~200 entries/day). It uses Google Cloud Speech-to-Text V2 (Chirp 3) and Win32 SendInput for universal paste support.

## Commands

```bash
# Setup
uv sync

# Run
python main.py

# Tests
python -m pytest tests/ -v --tb=short
python -m pytest tests/path/to/test_file.py::test_name -v
python -m pytest tests/ -v --tb=short --cov=app --cov-report=html

# Type check
pyright app service utils

# Build executable
python build.py
```

## Architecture

Layered design: `app` (Tkinter UI) → `service` (pipeline) → `external_service` (Google APIs) → `utils` (config/env).

**Core recording pipeline** (`service/`):
1. `audio_recorder.py` — PyAudio mic input
2. `audio_file_manager.py` — WAV file persistence (enables F8 retry)
3. `transcription_handler.py` — background thread coordinator
4. `google_stt_api.py` — Google Cloud STT V2 client
5. `text_transformer.py` — punctuation control, CSV replacements, spacing cleanup
6. Output: `clipboard_manager.py` → `paste_backend.py` (Win32 Ctrl+V) or `docs_output.py` (Google Docs append)

**UI layer** (`app/`):
- `application.py` — wires all dependencies at startup
- `main_window.py` (`VoiceInputManager`) — top-level orchestrator
- `ui_queue_processor.py` — thread-safe UI updates via queue

**Config** (`utils/`):
- `app_config.py` — typed property facade
- `config_manager.py` — INI file I/O (`utils/config.ini`)
- `env_loader.py` — `.env` parsing (credentials, paths)

**Hotkeys:** Pause = record/stop, F8 = retry last audio, F9 = toggle punctuation, Esc = exit.

## Coding Standards

- Type hints required on all parameters and return values
- Functions ≤ 50 lines; single responsibility per function/module
- Import order: stdlib → third-party → local (alphabetical within groups, `import` before `from`)
- UI-facing strings in Japanese
- Comments only for non-obvious logic, in Japanese, minimal

## Data Files

- `data/replacements.txt` — CSV (old,new) substitution rules applied post-transcription
- `data/technical_terms.txt` — one phrase per line, sent as phrase hints to STT API

## Environment

`.env` required at project root:
```
GOOGLE_PROJECT_ID=...
GOOGLE_LOCATION=asia-northeast1
GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}
```
