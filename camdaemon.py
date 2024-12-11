#!/usr/bin/env python3
import datetime
import time

import picamera2

import config


def picam2_setup(picam2: picamera2.Picamera2) -> None:
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
    current_time = datetime.datetime.now()
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
    while True:
        if web_listening():
            image = picam2.capture_image()
            image.save(config.IMAGE_FILE, "JPEG")

        time.sleep(config.REFRESH_INTERVAL)


def main() -> None:
    try:
        with picamera2.Picamera2() as picam2:
            picam2_setup(picam2)
            run_camera_loop(picam2)
    except (RuntimeError, IndexError) as r_err:
        print("\n" + "="*80)
        print(
            "Error when trying to set up the camera. Is it connected? Is",
            "something else using it?",
        )
        print("="*80, "\n")

        raise r_err


if __name__ == "__main__":
    main()
