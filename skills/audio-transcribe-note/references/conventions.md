# File Conventions

| Stage | Input | Output |
| --- | --- | --- |
| Transcribe | `raw/<stem>.<ext>` | `transcription/<stem>.txt` |
| Correct | `transcription/<stem>.txt` | `transcription/<stem>-ref.txt` |
| Note | `transcription/<stem>-ref.txt` | `note/<stem>-ai-note.md` |

Supported audio formats: `.mp3`, `.wav`, `.m4a`.

Note frontmatter uses `title`, `date`, and `lang: zh-TW`. Body sections are: 簡介, 重點摘要, 章節內容, 待辦事項.
