from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app.song_worker import song_worker
from app.config import Config
from app.db import db
import threading

def create_app(config_class=Config):
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(config_class)

    # ✅ Initialize the database with the app
    db.init_app(app)

    with app.app_context():
        from .models import User, SongQueue
        db.create_all()

        from .admin import init_admin
        init_admin(app, db)

        from app import routes

        # ✅ Start background worker thread with context
        start_worker(app)

    return app

def start_worker(app):
    def run_worker():
        with app.app_context():
            song_worker()
    t = threading.Thread(target=run_worker, name="SongWorker", daemon=True)
    t.start()
