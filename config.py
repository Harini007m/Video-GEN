import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
TRANSCRIPT_FOLDER = os.path.join(BASE_DIR, "transcripts")
SUBTITLE_FOLDER = os.path.join(BASE_DIR, "subtitles")
ALLOWED_EXTENSIONS = {"mp4", "mp3", "wav", "mkv", "mov", "mpv"}

MAX_CONTENT_LENGTH = 1024 * 1024 * 1024  # 1 GB

SECRET_KEY = os.environ.get("FLASK_SECRET", "dev-secret")
