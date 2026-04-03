import pytest
from unittest.mock import patch, MagicMock
from pydub import AudioSegment
from io import BytesIO
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tts
