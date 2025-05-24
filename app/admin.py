from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import User

admin = Admin()

def init_admin(app, db):
    admin.init_app(app)
    admin.add_view(ModelView(User, db.session))
