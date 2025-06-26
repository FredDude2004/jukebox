from .config import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)

    def __init__(self, username):
        self.username = username

class SongQueue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(512), nullable=False)
    filename = db.Column(db.String(256), nullable=False)
    filepath = db.Column(db.String(512), nullable=False)
    title = db.Column(db.String(512), nullable=True)
    is_playing = db.Column(db.Boolean, default=False)
    played = db.Column(db.Boolean, default=False)
