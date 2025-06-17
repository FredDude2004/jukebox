from flask import render_template, request, redirect, session, url_for, current_app as app
from .models import User, SongQueue
from .song_queue import add_to_queue
from .db import db

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if User.query.filter_by(username=username).first():
        return render_template('index.html', error='User already exists')
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    session['username'] = username
    return redirect(url_for('dashboard'))

@app.route("/dashboard")
def dashboard():
    if 'username' in session:
        songs = SongQueue.query.order_by(SongQueue.id).all()
        return render_template('dashboard.html', username=session['username'], songs=songs)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_to_queue_route():
    link = request.form['song']
    add_to_queue(link)
    return redirect(url_for('dashboard'))




