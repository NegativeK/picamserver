#!/usr/bin/python3
"""Set and fetch configuration options and load environment variables."""
import os
import pathlib
import secrets

import dotenv

IMAGE_FILE = pathlib.Path("./data/photo.jpg")
LISTENER_PATH = pathlib.Path("/tmp/listeners")
LISTENER_AGE_SECONDS = 30
REFRESH_INTERVAL = 2

def get_session_key() -> str:
    """Fetch (and set if necessary) the session secret key.

    Returns:
        The session key.
    """
    session_key = os.getenv("SESSION_KEY", default=None)

    if session_key is None:
        session_key = secrets.token_hex()
        os.environ["SESSION_KEY"] = session_key

        env_file = pathlib.Path("./.env")
        print("Creating .env if not already existent.")
        env_file.touch(mode=0o600, exist_ok=True)
        env_file.write_text(f"SESSION_KEY={session_key}")

    return session_key


LISTENER_PATH.mkdir(mode=0o744, exist_ok=True)
dotenv.load_dotenv()
