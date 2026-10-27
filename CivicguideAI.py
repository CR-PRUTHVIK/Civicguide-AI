"""
CivicGuide AI - Indian Civil Services & Welfare Portal
Primary VS Code entry point for starting the web application.

Usage:
    python CivicguideAI.py
    (or press F5 / click 'Run Python File' in VS Code)
"""

import os
import sys
import socket
import threading
import time
import webbrowser

# Ensure the project directory is the current working directory and in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    os.chdir(PROJECT_ROOT)
except Exception:
    pass

# Ensure Windows terminal handles UTF-8 correctly
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import uvicorn


def get_local_ip() -> str:
    """Detects active local Wi-Fi / LAN IP address for mobile access."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"


def launch_browser():
    """Opens browser automatically after server starts."""
    time.sleep(1.2)
    try:
        webbrowser.open("http://127.0.0.1:8000")
    except Exception:
        pass


def main():
    local_ip = get_local_ip()

    print("\n" + "=" * 65)
    print("🚀 [CivicGuide AI] Indian Civil Services & Welfare Portal")
    print("=" * 65)
    print(f"💻 Local PC Access:    http://127.0.0.1:8000")
    print(f"📱 Mobile / Wi-Fi:     http://{local_ip}:8000")
    print("=" * 65)
    print("💡 Tip: Both your PC and phone can access this portal")
    print("   when connected to the same Wi-Fi / hotspot network.")
    print("   Press CTRL+C anytime in this terminal to stop.")
    print("=" * 65 + "\n")

    # Open browser in a background thread
    threading.Thread(target=launch_browser, daemon=True).start()

    # Start FastAPI server via Uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
