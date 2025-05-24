from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from .models import User
        db.create_all()

        # Setup admin separately
        from .admin import init_admin
        init_admin(app, db)

        # Import routes after models and admin
        from . import routes

    return app
