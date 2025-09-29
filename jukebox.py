from flask import Flask, render_template
from flask_socketio import SocketIO

import urllib.request
import json
import urllib3
import pprint


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

queue = []
current_video = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/player")
def player():
    return render_template("player.html")


@socketio.on("add_video")
def handle_add_video(video_id):
    global current_video
    title = fetch_youtube_title(video_id)
    queue.append([video_id, title])
    socketio.emit("queue_updated", queue)

    if current_video is None:
        play_next()


@socketio.on("video_ended")
def handle_video_ended():
    play_next()


@socketio.on("skip_video")
def handle_skip_video():
    play_next()


def play_next():
    global current_video
    if queue:
        current_video = queue.pop()[0]
    else:
        current_video = None

    socketio.emit("now_playing", current_video)
    socketio.emit("queue_updated", queue)


def fetch_youtube_title(video_id):
    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % video_id}
    url = "https://www.youtube.com/oembed"
    query_string = urllib3.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        pprint.pprint(data)
        print(data["title"])


if __name__ == "__main__":
    socketio.run(app)
