#!/usr/bin/env python
import datetime
import multiprocessing
import uuid

import config

context = multiprocessing.get_context("fork")


class Process(context.Process):
    def __init__(self) -> None:
        """Set up flask.

        Because flask is multithreaded, we don't want it loading when the
        parent task imports this module. Load it after this process begins.
        """
        import flask
        self.flask = flask

        super().__init__(daemon=True)

    def run(self) -> None:
        """Configure the flask application."""
        app = self.flask.Flask(__name__)
        # TODO Secure this.
        app.secret_key = config.get_session_key()


        @app.get("/")
        def get_root():
            title = "Printer"
            image_request_path = "./printer"

            return self.flask.render_template(
                "index.html",
                title=title,
                image=image_request_path,
            )


        @app.get("/printer")
        def get_print_image():
            self.ensure_listener_file()

            return self.flask.send_from_directory(
                config.IMAGE_FILE.parent,
                config.IMAGE_FILE.name,
                mimetype="image/jpeg",
            )

        app.run(host="0.0.0.0", port=5000)


    def ensure_listener_file(self):
        """Update the time in the listener file.

        Create a listener file for the session if one does not exist.
        """
        if "listener" not in self.flask.session:
            self.flask.session["listener"] = str(uuid.uuid4())

        now = str(datetime.datetime.now())
        listener_file = config.LISTENER_PATH / self.flask.session["listener"]
        listener_file.write_text(now)
