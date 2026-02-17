"""Transcription helpers built on OpenAI Whisper."""

from functools import lru_cache

import whisper
import torch

import config

@lru_cache(maxsize=1)
def get_model():
    """Load and cache the Whisper model instance."""
    return whisper.load_model(config.WHISPER_MODEL)

def transcribe_audio(audio_path):
    """Transcribe audio and return normalized segment dictionaries."""
    model = get_model()
    use_fp16 = torch.cuda.is_available()
    result = model.transcribe(audio_path, fp16=use_fp16)
    segments = []
    for seg in result.get("segments", []):
        segments.append({
            "start": float(seg["start"]),
            "end": float(seg["end"]),
            "text": seg["text"].strip()
        })
    return segments
