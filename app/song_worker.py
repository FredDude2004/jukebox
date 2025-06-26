from .config import db, socketio
from .models import SongQueue
import pygame
import time
import os

is_paused = False

def pause():
    global is_paused 
    if is_paused:
        pygame.mixer.music.unpause()
        print("Unpaused")
    else:
        pygame.mixer.music.pause()
        print("Paused")
    is_paused = not is_paused

def skip():
    pygame.mixer.music.stop()

def clear_queue():
    # deleting all songs from DB
    SongQueue.query.delete()
    db.session.commit()

    print("All rows deleted from SongQueue")

    # stopping current song
    pygame.mixer.music.stop()

    # removing all downloaded songs
    downloads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'downloads')
    downloads_dir = os.path.abspath(downloads_dir)

    if os.path.exists(downloads_dir):
        for file in os.listdir(downloads_dir):
            os.remove(os.path.join(downloads_dir, file))
        print("Queue Cleared")
    else:
        print(f"Directory not found: {downloads_dir}")

def play_audio(path):
    global song_playing

    if not os.path.exists(path):
        print(f"File not found: {path}", flush=True)
        return

    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy() or is_paused:
        time.sleep(0.1)

    os.remove(path)

def song_worker():
    pygame.init()
    pygame.mixer.init()
    while True:
        try:
            song = SongQueue.query.filter_by(played=False).order_by(SongQueue.id).first()
            if song:
                song.is_playing = True
                db.session.commit()
                socketio.emit("refresh_screen")
                play_audio(song.filepath)
                db.session.delete(song)
                db.session.commit()
                socketio.emit("refresh_screen")
            else:
                time.sleep(1)
        except Exception as e:
            print("Worker error:", e)
            time.sleep(1)
