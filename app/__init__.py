from flask import Flask
from .config import db, socketio, basic_auth
from .models import User, SongQueue
from .main_bp import main_bp
from .admin_routes import admin_bp
from .admin import init_admin
from .song_worker import song_worker
import threading 

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    socketio.init_app(app)
    basic_auth.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        init_admin(app, db)
        start_worker(app)

    return app


def start_worker(app):
    def run_worker():
        with app.app_context():
            song_worker()
    t = threading.Thread(target=run_worker, name="SongWorker", daemon=True)
    t.start()   
