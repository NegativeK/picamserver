#!/bin/bash
. venv/bin/activate && flask --app main run -h 0.0.0.0 --reload
