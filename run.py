import subprocess
from app import create_app
from app.config import socketio


def setup_mdns_hostname(hostname="jukebox"):
    try:
        # Set the hostname
        subprocess.run(["sudo", "hostnamectl", "set-hostname", hostname], check=True)

        # Install Avahi (mDNS service) if not installed
        subprocess.run(["sudo", "pacman", "-S", "avahi-daemon"], check=True)

        # Enable and start avahi-daemon
        subprocess.run(["sudo", "systemctl", "enable", "avahi-daemon"], check=True)
        subprocess.run(["sudo", "systemctl", "start", "avahi-daemon"], check=True)

        print(f"Hostname set to {hostname}. You can now access via http://{hostname}.local:5000")
    except subprocess.CalledProcessError as e:
        print("Failed to set up mDNS hostname:", e)

if __name__ == '__main__':
    setup_mdns_hostname()
    app = create_app()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)
