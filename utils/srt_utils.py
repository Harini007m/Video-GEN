import srt
from datetime import timedelta

def _to_timedelta(seconds):
    return timedelta(seconds=seconds)

def segments_to_srt(segments):
    subtitles = []
    for i, seg in enumerate(segments, start=1):
        start = _to_timedelta(seg["start"])
        end = _to_timedelta(seg["end"])
        content = seg["text"]
        subtitles.append(srt.Subtitle(index=i, start=start, end=end, content=content))
    return srt.compose(subtitles)
