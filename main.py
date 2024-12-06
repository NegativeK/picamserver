#!/usr/bin/env python
import datetime
import flask
import uuid

import config

app = flask.Flask(__name__)
# TODO Secure this.
app.secret_key = b"INSECUREINSECUREINSECUREINSECURE"


def ensure_listener_file():
    if "listener" not in flask.session:
        flask.session["listener"] = str(uuid.uuid4())

    now = str(datetime.datetime.now())
    listener_file = config.LISTENER_PATH / flask.session["listener"]
    listener_file.write_text(now)


@app.get("/")
def get_root():
    title = "Printer"
    image_request_path = "./printer"

    return flask.render_template(
        "index.html",
        title=title,
        image=image_request_path,
    )


@app.get("/printer")
def get_print_image():
    ensure_listener_file()

    return flask.send_from_directory(
        config.IMAGE_FILE.parent,
        config.IMAGE_FILE.name,
        mimetype="image/jpeg",
    )
