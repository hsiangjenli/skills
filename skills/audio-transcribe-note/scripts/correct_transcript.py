import argparse
import pathlib

import dotenv

from common import OPENROUTER_BASE_URL, get_api_key, post_with_retries, read_text

CORRECTION_MODEL = "openai/gpt-4.1"

SYSTEM_PROMPT = (
    "你是繁體中文逐字稿校對員。請只修正明顯的錯字、同音字誤植、專有名詞與英文術語拼寫，"
    "保留口語語氣、段落與原意，不要摘要、不要刪減、不要加入新內容。"
    "只輸出修正後的全文。"
)


def correct_text(text: str, api_key: str, model: str) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        "temperature": 0,
    }
    data = post_with_retries(f"{OPENROUTER_BASE_URL}/chat/completions", api_key, payload)
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    dotenv.load_dotenv()
    parser = argparse.ArgumentParser(description="Create *-ref.txt from a transcription.")
    parser.add_argument("--transcript", type=pathlib.Path, required=True, help="Transcription .txt file")
    parser.add_argument("--model", default=CORRECTION_MODEL, help="OpenRouter chat model")
    args = parser.parse_args()

    if not args.transcript.is_file():
        raise FileNotFoundError(f"Transcript not found: {args.transcript}")

    api_key = get_api_key()
    corrected = correct_text(read_text(args.transcript), api_key, args.model)
    output_path = args.transcript.with_name(f"{args.transcript.stem}-ref.txt")
    output_path.write_text(corrected + "\n", encoding="utf-8")
    print(f"Corrected transcript saved to {output_path}")


if __name__ == "__main__":
    main()
