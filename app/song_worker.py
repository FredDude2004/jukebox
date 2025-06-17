from .models import SongQueue
from .db import db
from app.socketio import socketio
import pygame
import time
import os

def play_audio(path):
    if not os.path.exists(path):
        print(f"File not found: {path}", flush=True)
        return

    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

    refresh()

    while pygame.mixer.music.get_busy():
        time.sleep(1)

    os.remove(path)

def song_worker():
    print("worker thread started good", flush=True)
    print("SocketIO server attached?", socketio.server is not None)
    pygame.init()
    pygame.mixer.init()

    while True:
        try:
            song = SongQueue.query.filter_by(played=False).order_by(SongQueue.id).first()
            if song:
                print(f"Now playing: {song.filepath}", flush=True)
                song.is_playing = True
                db.session.commit()

                play_audio(song.filepath)

                db.session.delete(song)
                db.session.commit()

                refresh()

            else:
                time.sleep(2)
        except Exception as e:
            print(f"Worker error: {e}", flush=True)
            time.sleep(2)


def refresh():
    print("Emitting refresh_screen event...", flush=True)
    socketio.emit('refresh_screen')


