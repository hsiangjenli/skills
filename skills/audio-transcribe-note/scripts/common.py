import os
import pathlib
import time

import requests

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
RETRYABLE_STATUS_CODES = {502, 503, 504}
MAX_REQUEST_RETRIES = 3


def get_api_key() -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set")
    return api_key


def post_with_retries(url: str, api_key: str, payload: dict, timeout: int = 1800) -> dict:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    for attempt in range(1, MAX_REQUEST_RETRIES + 1):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=timeout)
            if response.ok:
                return response.json()
            if response.status_code not in RETRYABLE_STATUS_CODES:
                raise RuntimeError(f"OpenRouter returned {response.status_code}: {response.text}")
            if attempt >= MAX_REQUEST_RETRIES:
                raise RuntimeError(f"OpenRouter failed after retries: {response.text}")
        except requests.RequestException as error:
            if attempt >= MAX_REQUEST_RETRIES:
                raise RuntimeError("OpenRouter request failed after retries") from error
        print(f"OpenRouter request failed; retrying ({attempt}/{MAX_REQUEST_RETRIES - 1})...")
        time.sleep(attempt * 5)
    raise RuntimeError("OpenRouter request failed unexpectedly")


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")
