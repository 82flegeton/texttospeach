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


def test_fetch_audio_raises_on_non_200():
    with patch("tts.requests.post") as mock_post:
        mock_post.return_value = MagicMock(status_code=401, text="Unauthorized")
        with pytest.raises(RuntimeError, match="401"):
            tts.fetch_audio("hello", "voice123", "bad_key")


def test_fetch_audio_returns_bytes_on_success():
    fake_mp3 = b"fake_audio_data"
    with patch("tts.requests.post") as mock_post:
        mock_post.return_value = MagicMock(status_code=200, content=fake_mp3)
        result = tts.fetch_audio("hello", "voice123", "key")
    assert result == fake_mp3


def test_fetch_audio_sends_correct_voice_id():
    with patch("tts.requests.post") as mock_post:
        mock_post.return_value = MagicMock(status_code=200, content=b"audio")
        tts.fetch_audio("hello", "my_voice_id", "key")
    call_url = mock_post.call_args[0][0]
    assert "my_voice_id" in call_url
