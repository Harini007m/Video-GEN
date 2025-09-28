import whisper
import os
import shutil

_model = None
def get_model():
    global _model
    if _model is None:
        _model = whisper.load_model("small")
    return _model

def transcribe_audio(audio_path):
    model = get_model()
    result = model.transcribe(audio_path)
    segments = []
    for seg in result.get("segments", []):
        segments.append({
            "start": float(seg["start"]),
            "end": float(seg["end"]),
            "text": seg["text"].strip()
        })
    return segments
