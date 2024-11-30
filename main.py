#!/usr/bin/env python
import io
import os
import time

import flask
import picamera2

import camera

app = flask.Flask(__name__)


def take_photo():
    with picamera2.Picamera2() as picam2:
        picam2.start_preview(picamera2.Preview.NULL)

        preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
        picam2.configure(preview_config)

        capture_config = picam2.create_still_configuration()

        picam2.start()
        time.sleep(1)

        metadata = picam2.capture_metadata()
        controls = {c: metadata[c] for c in ["ExposureTime", "AnalogueGain", "ColourGains"]}

        picam2.set_controls(controls)

        picam2.switch_mode(capture_config)

        image = picam2.capture_image()

    return image


@app.get("/")
def get_root():
    title = "Printer"
    image = "./printer"

    return flask.render_template("index.html", title=title, image=image)


@app.get("/printer")
def get_print_image():
    try:
        image = take_photo()
    except RuntimeError:
        os._exit(1)

    image_io = io.BytesIO()
    image_name = "printer.jpg"
    image.save(image_io, format="JPEG")
    image_io.seek(0)

    return flask.send_file(
        image_io,
        mimetype="image/jpeg",
    )
