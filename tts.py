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
