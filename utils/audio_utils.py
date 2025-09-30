import subprocess
import os

FFMPEG_PATH = r"C:\Users\harin\ffmpeg\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe"

def extract_audio(video_path, audio_path):
    if not os.path.exists(FFMPEG_PATH):
        raise RuntimeError("FFmpeg not found at expected path. Please ensure FFmpeg is installed.")
    cmd = [
        FFMPEG_PATH, "-y",
        "-i", video_path,
        "-ac", "1",
        "-ar", "16000",
        audio_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed:\n{result.stderr.decode('utf-8', errors='ignore')}")
    return audio_path
