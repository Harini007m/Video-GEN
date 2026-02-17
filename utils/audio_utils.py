"""Audio extraction helpers backed by FFmpeg."""

import glob
import os
import shutil
import subprocess


def _find_ffmpeg_executable():
    """Return a usable ffmpeg executable path, or None when unavailable."""
    env_path = os.environ.get("FFMPEG_PATH")
    if env_path and os.path.exists(env_path):
        return env_path

    path_ffmpeg = shutil.which("ffmpeg")
    if path_ffmpeg:
        return path_ffmpeg

    user_profile = os.environ.get("USERPROFILE")
    if user_profile:
        pattern = os.path.join(user_profile, "ffmpeg", "*", "bin", "ffmpeg.exe")
        matches = glob.glob(pattern)
        if matches:
            return matches[0]

    return None


def extract_audio(video_path, audio_path):
    """Extract mono 16 kHz WAV audio from a media file using FFmpeg."""
    ffmpeg_path = _find_ffmpeg_executable()
    if not ffmpeg_path:
        raise RuntimeError(
            "FFmpeg not found. Install FFmpeg and add it to PATH, or set FFMPEG_PATH to ffmpeg.exe."
        )

    cmd = [
        ffmpeg_path,
        "-y",
        "-i",
        video_path,
        "-ac",
        "1",
        "-ar",
        "16000",
        audio_path,
    ]
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed:\n{result.stderr.decode('utf-8', errors='ignore')}")
    return audio_path
