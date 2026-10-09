import argparse
import datetime
import pathlib

import dotenv

from common import OPENROUTER_BASE_URL, get_api_key, post_with_retries, read_text

NOTE_MODEL = "openai/gpt-4.1"

SYSTEM_PROMPT = (
    "你是會議與訪談筆記整理助手。請根據逐字稿產出繁體中文 Markdown 筆記，"
    "包含：簡介、重點摘要、章節內容、待辦事項。不要編造逐字稿沒有的內容。"
    "只輸出 Markdown 本文，不要加入 frontmatter。"
)


def build_note(transcript: str, api_key: str, model: str) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": transcript},
        ],
        "temperature": 0.2,
    }
    data = post_with_retries(f"{OPENROUTER_BASE_URL}/chat/completions", api_key, payload)
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    dotenv.load_dotenv()
    parser = argparse.ArgumentParser(description="Create a markdown note under note/.")
    parser.add_argument("--transcript", type=pathlib.Path, required=True, help="Corrected transcript (*-ref.txt)")
    parser.add_argument("--title", required=True, help="Note title")
    parser.add_argument("--model", default=NOTE_MODEL, help="OpenRouter chat model")
    args = parser.parse_args()

    if not args.transcript.is_file():
        raise FileNotFoundError(f"Transcript not found: {args.transcript}")

    api_key = get_api_key()
    body = build_note(read_text(args.transcript), api_key, args.model)
    today = datetime.date.today().isoformat()
    frontmatter = f"---\ntitle: '{args.title}'\ndate: '{today}'\nlang: zh-TW\n---\n\n"

    output_dir = args.transcript.parent.parent / "note"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{args.transcript.stem.removesuffix('-ref')}-ai-note.md"
    output_path.write_text(frontmatter + body + "\n", encoding="utf-8")
    print(f"Note saved to {output_path}")


if __name__ == "__main__":
    main()
