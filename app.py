"""Flask app for uploading media and generating subtitle files."""

import os
import threading
import traceback
import uuid

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from utils.audio_utils import extract_audio
from utils.transcript_utils import transcribe_audio
from utils.srt_utils import segments_to_srt
import config

# Create directories if not exist
for folder in [config.UPLOAD_FOLDER, config.TRANSCRIPT_FOLDER, config.SUBTITLE_FOLDER]:
    os.makedirs(folder, exist_ok=True)

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH

PROCESS_LOCK = threading.Lock()
PROCESSING_FILES = set()

def allowed_file(filename):
    """Return True if file extension is in configured allow-list."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS

@app.route("/")
def index():
    """Render the upload form."""
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    """Handle upload and redirect to processing route."""
    if "file" not in request.files:
        flash("No file uploaded")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("No file selected")
        return redirect(request.url)
    if not allowed_file(file.filename):
        flash("Unsupported file type")
        return redirect(request.url)

    filename = secure_filename(file.filename)
    uid = uuid.uuid4().hex[:8]
    saved_name = f"{uid}_{filename}"
    upload_path = os.path.join(config.UPLOAD_FOLDER, saved_name)
    file.save(upload_path)

    return redirect(url_for("process", filename=saved_name))

@app.route("/process/<filename>")
def process(filename):
    """Process uploaded media into SRT subtitle file."""
    upload_path = os.path.join(config.UPLOAD_FOLDER, filename)
    if not os.path.exists(upload_path):
        return render_template("error.html", message="Uploaded file not found"), 404

    base_name = os.path.splitext(filename)[0]
    srt_filename = f"{base_name}.srt"
    srt_path = os.path.join(config.SUBTITLE_FOLDER, srt_filename)
    if os.path.exists(srt_path):
        return render_template("result.html", srt_file=srt_filename)

    with PROCESS_LOCK:
        if filename in PROCESSING_FILES:
            return render_template(
                "error.html",
                message="This file is already being processed. Please refresh in a moment.",
            ), 409
        PROCESSING_FILES.add(filename)

    audio_name = f"{base_name}.wav"
    audio_path = os.path.join(config.TRANSCRIPT_FOLDER, audio_name)

    try:
        print(f"Starting audio extraction for {filename}")
        extract_audio(upload_path, audio_path)
        print("Audio extraction completed")
        print("Starting transcription")
        segments = transcribe_audio(audio_path)
        print(f"Transcription completed, {len(segments)} segments")
        srt_text = segments_to_srt(segments)
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt_text)
        print("SRT file saved")
        return render_template("result.html", srt_file=srt_filename)
    except (RuntimeError, OSError, ValueError) as e:
        print(f"Error during processing: {str(e)}")
        traceback.print_exc()
        return render_template("error.html", message=str(e)), 500
    finally:
        with PROCESS_LOCK:
            PROCESSING_FILES.discard(filename)

@app.route("/download/<path:filename>")
def download(filename):
    """Download generated subtitle file."""
    return send_from_directory(config.SUBTITLE_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
