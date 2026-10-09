---
name: audio-transcribe-note
description: Transcribe user-provided audio through OpenRouter, correct typos in the transcript, and produce a markdown note. Use when the user provides an audio file (.m4a, .mp3, .wav) and wants a transcript, a corrected *-ref.txt transcript, or an ai-note.md note in a raw/transcription/note project layout.
---

# Audio Transcribe Note

## Directory Layout

Expect this project layout. Create any missing directories.

```text
<project>/
├── raw/             ← user audio files
├── transcription/   ← <stem>.txt (raw) and <stem>-ref.txt (corrected)
└── note/            ← <stem>-ai-note.md
```

## Setup

Run once per environment, from this skill directory:

```bash
uv run scripts/check_dependencies.py --install
```

Put the API key in `.env` in the project root or the current directory:

```dotenv
OPENROUTER_API_KEY=your-api-key
```

Chunking needs `ffmpeg` installed.

## Workflow

Run the steps in order. Each step reads the previous step's output.

1. Transcribe the audio in `raw/` into `transcription/<stem>.txt`:

   ```bash
   uv run scripts/transcribe.py --audio "<project>/raw/<file>.m4a"
   ```

   For long audio, add `--chunk --chunk_minutes 30`.

2. Correct typos into `transcription/<stem>-ref.txt`:

   ```bash
   uv run scripts/correct_transcript.py --transcript "<project>/transcription/<stem>.txt"
   ```

3. Write the note into `note/<stem>-ai-note.md`:

   ```bash
   uv run scripts/build_note.py --transcript "<project>/transcription/<stem>-ref.txt" --title "<Title>"
   ```

Pass `--model` to steps 2 and 3 to use a different OpenRouter chat model.

## Notes

- Step 1 uses `openai/gpt-transcribe` with `language=zh`. Change this only if the user asks for another language.
- Steps 2 and 3 only change wording and structure. Read the output before you present it.
- Do not overwrite an existing `-ref.txt` or note without asking.
- See `references/conventions.md` for file naming and note format details.
