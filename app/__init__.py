from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import threading 

db = SQLAlchemy()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from .models import User, SongQueue
        db.create_all()

        # Setup admin separately
        from .admin import init_admin
        init_admin(app, db)

        from . import routes

        from .song_worker import song_worker
        def start_worker(app):
            from .song_worker import song_worker

            def wrapped_worker():
                with app.app_context():
                    song_worker()

            t = threading.Thread(target=song_worker, name="SongWorker", daemon=True)
            t.start()

    if os.getenv("WEKZEUG_RUN_MAIN") == "true":
        start_worker(app)

    return app
