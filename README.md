# 🎵 Jukebox

A real-time collaborative music queue web app built with Flask. Jukebox allows users to add songs via YouTube, and admins can control playback (pause, skip, stop) through a secure dashboard. Ideal for parties or shared spaces where everyone can contribute to the vibe.

---

## 🚀 Features

- 📥 Add songs to a shared queue by pasting YouTube links
- ⏯️ Admin dashboard for playback controls (Pause, Skip, Stop)
- 🔄 Real-time updates using WebSockets (Flask-SocketIO)
- 🧑‍💼 BasicAuth-protected admin interface
- ⏳ Loading states to prevent duplicate submissions
- 📱 Mobile-friendly interface

---

## 🛠️ Tech Stack

| Tech           | Role                                     |
|----------------|------------------------------------------|
| Python         | Core backend language                    |
| Flask          | Web framework                            |
| Flask-SocketIO | Real-time communication                  |
| SQLAlchemy     | ORM and database management              |
| Flask-Admin    | Admin dashboard for playback controls    |
| Flask-BasicAuth| Simple admin authentication              |
| FFmpeg         | Download and process audio from YouTube  |
| yt-dlp         | Download YouTube content                 |
| SQLite         | Lightweight database                     |
| HTML/CSS/JS    | Frontend (simple and functional)         |
| Socket.IO JS   | Client-side real-time updates            |

---

## 🧰 Setup

### ✅ Prerequisites

- Python 3.8+
- FFmpeg installed (`ffmpeg` available in PATH)
- Node.js (only if customizing the frontend)
- Git

---

### 🔧 Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/jukebox.git
cd jukebox

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Then edit .env to set your BasicAuth credentials

# Initialize the database
python
>>> from app import db
>>> db.create_all()
>>> exit()

# Start the app
flask run
