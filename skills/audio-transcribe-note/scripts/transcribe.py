import argparse
import base64
import pathlib
import tempfile

import dotenv
from pydub import AudioSegment

from common import OPENROUTER_BASE_URL, get_api_key, post_with_retries

TRANSCRIPTION_MODEL = "openai/gpt-transcribe"


def transcribe_file(audio_path: pathlib.Path, api_key: str, label: str) -> str:
    audio_format = audio_path.suffix.lower().lstrip(".")
    payload = {
        "model": TRANSCRIPTION_MODEL,
        "input_audio": {
            "data": base64.b64encode(audio_path.read_bytes()).decode("ascii"),
            "format": audio_format,
        },
        "language": "zh",
        "response_format": "json",
    }
    print(f"Transcribing {label}...")
    data = post_with_retries(f"{OPENROUTER_BASE_URL}/audio/transcriptions", api_key, payload)
    return data["text"].strip()


def transcribe_chunks(audio_path: pathlib.Path, api_key: str, chunk_minutes: float) -> str:
    audio = AudioSegment.from_file(audio_path)
    chunk_ms = int(chunk_minutes * 60 * 1000)
    starts = range(0, len(audio), chunk_ms)
    texts = []
    for index, start in enumerate(starts, start=1):
        chunk = audio[start : start + chunk_ms]
        with tempfile.NamedTemporaryFile(suffix=".mp3") as temp_file:
            chunk.export(temp_file.name, format="mp3")
            texts.append(transcribe_file(pathlib.Path(temp_file.name), api_key, f"chunk {index}/{len(starts)}"))
    return "\n".join(texts)


def main() -> None:
    dotenv.load_dotenv()
    parser = argparse.ArgumentParser(description="Transcribe an audio file in raw/ into transcription/.")
    parser.add_argument("--audio", type=pathlib.Path, required=True, help="Audio file under raw/")
    parser.add_argument("--chunk", action="store_true", help="Split audio before transcribing")
    parser.add_argument("--chunk_minutes", type=float, default=30, help="Chunk length in minutes")
    args = parser.parse_args()

    if args.chunk_minutes <= 0:
        parser.error("--chunk_minutes must be greater than 0")
    audio_path = args.audio
    if not audio_path.is_file():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    api_key = get_api_key()
    if args.chunk:
        text = transcribe_chunks(audio_path, api_key, args.chunk_minutes)
    else:
        text = transcribe_file(audio_path, api_key, audio_path.name)

    output_dir = audio_path.parent.parent / "transcription"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{audio_path.stem}.txt"
    output_path.write_text(text + "\n", encoding="utf-8")
    print(f"Transcription saved to {output_path}")


if __name__ == "__main__":
    main()
