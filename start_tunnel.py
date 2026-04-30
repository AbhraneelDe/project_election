"""
start_tunnel.py
───────────────
Starts the Django dev server AND opens an ngrok tunnel.
Run with:  python start_tunnel.py
"""
import os
import sys
import time
import threading
import subprocess
from dotenv import load_dotenv

load_dotenv()


def run_django():
    """Start Django development server."""
    subprocess.run(
        [sys.executable, "manage.py", "runserver", "8000"],
        env={**os.environ, "DJANGO_SETTINGS_MODULE": "election_assistant.settings"}
    )


def start_tunnel():
    """Open an ngrok tunnel to port 8000 and print the public URL."""
    try:
        from pyngrok import ngrok, conf

        # Set auth token if provided
        ngrok_token = os.getenv("NGROK_AUTHTOKEN", "")
        if ngrok_token:
            conf.get_default().auth_token = ngrok_token

        # Wait for Django to start
        time.sleep(3)

        tunnel = ngrok.connect(8000, proto="http")
        public_url = tunnel.public_url

        print("\n" + "═" * 60)
        print("  🏛️  ElectionGuide — Live Public URL")
        print("═" * 60)
        print(f"  🌐  {public_url}")
        print(f"  💬  Chat: {public_url}/chat/")
        print("═" * 60)
        print("  Press Ctrl+C to stop the server.\n")

        ngrok.set_auth_token  # keep alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            ngrok.kill()

    except ImportError:
        print("\n⚠️  pyngrok not installed. Run:  pip install pyngrok")
    except Exception as e:
        print(f"\n⚠️  Tunnel error: {e}")
        print("   The Django server is still running at http://127.0.0.1:8000")


if __name__ == "__main__":
    print("🚀 Starting ElectionGuide server...")

    # Run Django in a background thread
    django_thread = threading.Thread(target=run_django, daemon=True)
    django_thread.start()

    # Start tunnel in main thread
    start_tunnel()
