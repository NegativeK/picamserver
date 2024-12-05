#!/usr/bin/env python
import time

import picamera2

import config


def picam2_setup(picam2: picamera2.Picamera2) -> None:
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


def web_listening() -> bool:
    has_files = not any(config.LISTENER_PATH.iterdir())

    return has_files


def run_camera_loop(picam2: picamera2.Picamera2) -> None:
    while True:
        if web_listening():
            picam2_setup(picam2)
            image = picam2.capture_image()
            image.save(config.IMAGE_FILE, "JPEG")

        time.sleep(config.REFRESH_INTERVAL)


def main() -> None:
    with picamera2.Picamera2() as picam2:
        run_camera_loop(picam2)


if __name__ == "__main__":
    main()
