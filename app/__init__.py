from flask import Flask
from dotenv import load_dotenv
from app.song_worker import song_worker
from app.config import Config
from app.db import db
from app.socketio import socketio
import threading


def create_app(config_class=Config):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config_class)
    socketio.init_app(app)

    db.init_app(app)

    with app.app_context():
        from .models import User, SongQueue
        db.create_all()

        from .admin import init_admin
        init_admin(app, db)

        from app import routes

        start_worker(app)

    return app

def start_worker(app):
    def run_worker():
        with app.app_context():
            song_worker()
    t = threading.Thread(target=run_worker, name="SongWorker", daemon=True)
    t.start()
