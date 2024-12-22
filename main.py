#!/usr/bin/env python3
"""Start a flask server for sharing Pi functionality."""
import multiprocessing
import time
from collections.abc import Iterable

import camdaemon
import flaskapp

SECONDS_TO_TERMINATION = 5
context = multiprocessing.get_context("fork")


def stop_processes(processes: Iterable[context.Process]) -> None:
    """Stop running processes.

    Processes that don't finishly cleanly within 5 seconds are terminated.

    Args:
        processes: The processes to stop and potentially terminate.
    """
    for proc in processes:
        if proc.is_alive():
            print(f"waiting on {proc} to finish")
            proc.join(SECONDS_TO_TERMINATION)
        if proc.is_alive():
            print(f"terminating {proc}")
            proc.terminate()


def main() -> None:
    """Handle startup and shutdown of the processes.

    Improvements: https://stackoverflow.com/a/19929767
    """
    processes = []
    process_classes = [camdaemon.CameraProcess, flaskapp.Process]

    for process_class in process_classes:
        process = process_class()
        process.start()
        processes.append(process)

    healthy = True
    while healthy:
        for process in processes:
            if process.exitcode is not None:
                print(
                    f"{process} has exited with code {process.exitcode}; "
                    "terminating",
                    )
                healthy = False

        time.sleep(0.1)

    stop_processes(processes)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(130) from None
