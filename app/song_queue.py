from .models import SongQueue 
from .config import db
import os
import threading
import uuid
import yt_dlp

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_song(url):
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filepath.replace('.mp3', '.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = 'Unknown title'
        if info:
            title = info.get('title', 'Unknown title')

    return filename, filepath, title

def add_to_queue(url):
    try:
        filename, filepath, title = download_song(url)
        new_song = SongQueue(url=url, filename=filename, filepath=filepath, title=title)
        db.session.add(new_song)
        db.session.commit()
        print(f"Added to DB queue: {title}", flush=True)
    except Exception as e:
        print(f"Download failed: {e}", flush=True)



