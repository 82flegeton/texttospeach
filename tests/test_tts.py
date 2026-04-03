import pytest
from unittest.mock import patch, MagicMock
from pydub import AudioSegment
from io import BytesIO
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tts


def test_read_text_returns_file_content(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("Hello world.")
    assert tts.read_text(str(f)) == "Hello world."


def test_chunk_text_returns_single_chunk_if_short():
    assert tts.chunk_text("Short text.", limit=5000) == ["Short text."]


def test_chunk_text_splits_at_sentence_boundary():
    long_text = ("This is a sentence. " * 300).strip()
    chunks = tts.chunk_text(long_text, limit=500)
    assert all(len(c) <= 520 for c in chunks)
    assert len(chunks) > 1


def test_chunk_text_no_empty_chunks():
    long_text = ("Word. " * 1000).strip()
    chunks = tts.chunk_text(long_text, limit=200)
    assert all(c.strip() for c in chunks)
