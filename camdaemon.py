#!/usr/bin/env python3
"""Store a camera image to the filesystem and update it on a set interval."""
import datetime
import pathlib
import time

import picamera2

import config


def picam2_setup(picam2: picamera2.Picamera2) -> None:
    """Set up a Picamera2 and set exposure settings.

    Args:
        picam2: The instantiated camera object.
    """
    picam2.start_preview(picamera2.Preview.NULL)

    preview_config = picam2.create_preview_configuration(
        main={"size": (800, 600)},
    )
    picam2.configure(preview_config)

    capture_config = picam2.create_still_configuration()

    picam2.start()
    time.sleep(1)

    metadata = picam2.capture_metadata()
    controls = {
        c: metadata[c]
        for c in ["ExposureTime", "AnalogueGain", "ColourGains"]
    }

    picam2.set_controls(controls)

    picam2.switch_mode(capture_config)


def web_listening() -> bool:
    """Check if there's a web service with active user sessions for the image.

    Returns:
        Whether there are active use sessions.
    """
    current_time = datetime.datetime.now(tz=datetime.UTC)
    oldest_session_time = current_time - datetime.timedelta(
        seconds=config.LISTENER_AGE_SECONDS,
    )

    for session_file in config.LISTENER_PATH.iterdir():
        session_contents = session_file.read_text()
        session_timestamp = datetime.datetime.fromisoformat(session_contents)

        if session_timestamp < oldest_session_time:
            print("Removing expired session file.")
            session_file.unlink()

    has_files = any(config.LISTENER_PATH.iterdir())

    return has_files


def run_camera_loop(picam2: picamera2.Picamera2) -> None:
    """Run an infinite loop for capturing the camera image.

    Args:
        picam2: The instantiated Picamera2 object.
    """
    image_file = config.IMAGE_FILE

    while True:
        if web_listening():
            tmp_image_file = pathlib.Path(f"{image_file}_tmp")

            image = picam2.capture_image()
            image.save(tmp_image_file, "JPEG")
            tmp_image_file.rename(image_file)

        time.sleep(config.REFRESH_INTERVAL)


def main() -> None:
    """Instantiate a Picamera2 and initiate the photo taking loop."""
    try:
        with picamera2.Picamera2() as picam2:
            picam2_setup(picam2)
            run_camera_loop(picam2)
    except (RuntimeError, IndexError):
        print("\n" + "="*80)
        print(
            "Error when trying to set up the camera. Is it connected? Is",
            "something else using it?",
        )
        print("="*80, "\n")

        raise


if __name__ == "__main__":
    main()
