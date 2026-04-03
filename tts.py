import os
import sys
import re
import requests
from pathlib import Path
from pydub import AudioSegment
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

CHUNK_LIMIT = 5000
API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
MODEL_ID = "eleven_multilingual_v2"


def read_text(path: str) -> str:
    """Read text content from a file."""
    with open(path, encoding="utf-8") as f:
        return f.read()


def chunk_text(text: str, limit: int = CHUNK_LIMIT) -> list[str]:
    """Split text at sentence boundaries if it exceeds limit."""
    if len(text) <= limit:
        return [text]
    chunks = []
    sentences = re.split(r"(?<=[.!?]) +", text)
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= limit:
            current = (current + " " + sentence).strip()
        else:
            if current:
                chunks.append(current)
            current = sentence
    if current:
        chunks.append(current)
    return chunks


def fetch_audio(text: str, voice_id: str, api_key: str) -> bytes:
    """Fetch MP3 bytes from ElevenLabs TTS API."""
    url = API_URL.format(voice_id=voice_id)
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(f"ElevenLabs API error {response.status_code}: {response.text}")
    return response.content
