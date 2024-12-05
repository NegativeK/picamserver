#!/usr/bin/env python
import flask

import config

app = flask.Flask(__name__)


def ensure_listener():
    if "listener" not in flask.session:
        # Create a file in LISTENER_PATH named uuid, contents timestamp
        pass


@app.get("/")
def get_root():
    ensure_listener()
    title = "Printer"
    image_request_path = "./printer"

    return flask.render_template(
        "index.html",
        title=title,
        image=image_request_path,
    )


@app.get("/printer")
def get_print_image():
    return flask.send_from_directory(
        config.IMAGE_FILE.parent,
        config.IMAGE_FILE.name,
        mimetype="image/jpeg",
    )
