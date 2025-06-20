from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_basicauth import BasicAuth

load_dotenv()

db = SQLAlchemy()
socketio = SocketIO(async_mode='eventlet', cors_allowed_origins="*")
basic_auth = BasicAuth()

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME")
    BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD")

