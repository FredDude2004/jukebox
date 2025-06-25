from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import User, SongQueue
from .song_worker import pause, skip, stop_queue

admin = Admin(name='Jukebox Admin', template_mode='bootstrap3')

def init_admin(app, db):
    admin.init_app(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(SongQueue, db.session))

def handle_admin_action(action):
    if action == "pause":
        pause()
    elif action == "skip":
        skip()
    elif action == "stop":
        stop_queue()

