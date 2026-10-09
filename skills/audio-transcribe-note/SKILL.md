---
name: audio-transcribe-note
description: Transcribe user-provided audio through OpenRouter, then correct typos and write a markdown note by following the bundled prompts. Use when the user provides an audio file (.m4a, .mp3, .wav) and wants a transcript, a corrected *-ref.txt transcript, or a *-ai-note.md note in a raw/transcription/note project layout.
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

Chunking needs `ffmpeg` installed.

The transcription step needs `OPENROUTER_API_KEY`. Put it in `.env` in the project root or the current directory:

```dotenv
OPENROUTER_API_KEY=your-api-key
```

## Workflow

1. Transcribe the audio in `raw/` into `transcription/<stem>.txt`:

   ```bash
   uv run scripts/transcribe.py --audio "<project>/raw/<file>.m4a"
   ```

   For long audio, add `--chunk --chunk_minutes 30`.

2. Correct the transcript into `transcription/<stem>-ref.txt`. Read `prompts/refactor-transcription.prompt.md` and apply its rules to `transcription/<stem>.txt`. Save the result as `transcription/<stem>-ref.txt`.

3. Write the note into `note/<stem>-ai-note.md`. Read `prompts/generate-note.prompt.md` and apply its template to `transcription/<stem>-ref.txt`. Save the result as `note/<stem>-ai-note.md`.

Steps 2 and 3 are done by the agent itself using the prompts. No extra API call or script is needed.

## Notes

- Step 1 uses `openai/gpt-transcribe` with `language=zh`. Change this only if the user asks for another language.
- Steps 2 and 3 only change wording and structure, and must not add content that is not in the transcript. Read the output before you present it.
- Do not overwrite an existing `-ref.txt` or note without asking.
- See `references/conventions.md` for file naming details.
