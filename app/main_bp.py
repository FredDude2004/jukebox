from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import User, SongQueue
from .song_queue import add_to_queue
from .config import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['username'] = username
        if username == 'admin':
            return redirect(url_for('admin_routes.admin_dashboard'))
        return redirect(url_for('main.dashboard'))
    return render_template('index.html', error='Invalid credentials')

@main_bp.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if User.query.filter_by(username=username).first():
        return render_template('index.html', error='User already exists')
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('main.index'))

@main_bp.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('main.index'))
    songs = SongQueue.query.order_by(SongQueue.id).all()
    return render_template('dashboard.html', username=session['username'], songs=songs)

@main_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main.index'))

@main_bp.route('/add', methods=['POST'])
def add_song():
    link = request.form['song']
    add_to_queue(link)
    return redirect(url_for('main.dashboard'))



