# File Conventions

| Stage | Input | Output | How |
| --- | --- | --- | --- |
| Transcribe | `raw/<stem>.<ext>` | `transcription/<stem>.txt` | `scripts/transcribe.py` |
| Correct | `transcription/<stem>.txt` | `transcription/<stem>-ref.txt` | `prompts/refactor-transcription.prompt.md` |
| Note | `transcription/<stem>-ref.txt` | `note/<stem>-ai-note.md` | `prompts/generate-note.prompt.md` |

Supported audio formats: `.mp3`, `.wav`, `.m4a`.

The note template comes from `prompts/generate-note.prompt.md`. Its frontmatter uses `title`, `date`, `updated`, `author`, `tags`, `toc`, and `lang: zh-TW`.
