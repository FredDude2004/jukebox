from flask import render_template, request, redirect, session, url_for, current_app as app
from .models import User
from . import db
from queue import Queue
import os
import uuid
import yt_dlp
import pygame


DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

download_queue = Queue()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if User.query.filter_by(username=username).first():
        return render_template('index.html', error='User already exists')
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    session['username'] = username
    return redirect(url_for('dashboard'))

@app.route("/dashboard")
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_to_queue_route():
    link = request.form['song']
    add_to_queue(link)
    return redirect(url_for('dashboard'))


def add_to_queue(link):
    try:
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
            ydl.download([link])

        # Add metadata to the queue
        download_queue.put({
            'link': link,
            'filename': filename,
            'filepath': filepath
        })

        print(f"Queued file at {filepath}, exists: {os.path.exists(filepath)}", flush=True)
        handle_enqueue()

    except Exception as e:
        print(f"Failed to download {link}: {e}")



# Playing the Audio File
def play_audio(path):
    if not os.path.exists(path):
        print(f"File not found: {path}", flush=True)
        return

    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

    os.remove(path) # Delete the file once done playing

def handle_enqueue():
    audio_file = download_queue.get()
    audio_file_path = audio_file['filepath']
    print(audio_file_path, flush=True)
    play_audio(audio_file_path)

        







