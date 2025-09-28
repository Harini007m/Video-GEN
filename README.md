# Video Caption Generator

## Setup
1. Install FFmpeg and add to system PATH.
2. Create virtual environment:
   python -m venv .venv
   .venv\Scripts\activate  (Windows)
3. Install dependencies:
   pip install -r requirements.txt
4. Run Flask:
   python app.py
5. Open http://127.0.0.1:5000/ in browser.
6. Upload a video/audio to generate SRT subtitles.

Notes:
- Whisper model default: small. Change model in transcript_utils.py if needed.
- Uploaded files saved in 'uploads/', transcripts in 'transcripts/', subtitles in 'subtitles/'.
