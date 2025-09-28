import os
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

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
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
    upload_path = os.path.join(config.UPLOAD_FOLDER, filename)
    if not os.path.exists(upload_path):
        return render_template("error.html", message="Uploaded file not found"), 404

    base_name = os.path.splitext(filename)[0]
    audio_name = f"{base_name}.wav"
    audio_path = os.path.join(config.TRANSCRIPT_FOLDER, audio_name)

    try:
        extract_audio(upload_path, audio_path)
        segments = transcribe_audio(audio_path)
        srt_text = segments_to_srt(segments)
        srt_filename = f"{base_name}.srt"
        srt_path = os.path.join(config.SUBTITLE_FOLDER, srt_filename)
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt_text)
        return render_template("result.html", srt_file=srt_filename)
    except Exception as e:
        return render_template("error.html", message=str(e)), 500

@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(config.SUBTITLE_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
