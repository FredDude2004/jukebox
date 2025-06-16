from .models import SongQueue 
from . import db
from queue import Queue
import os
import uuid
import yt_dlp
import pygame
import threading
import time

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
        ydl.download([url])

    return filename, filepath


def add_to_queue(url):
    try:
        filename, filepath = download_song(url)
        new_song = SongQueue(url=url, filename=filename, filepath=filepath)
        db.session.add(new_song)
        db.session.commit()
        print(f"Added to DB queue: {filepath}", flush=True)
    except Exception as e:
        print(f"Download failed: {e}", flush=True)



