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
