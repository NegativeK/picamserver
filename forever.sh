#!/bin/bash
cd ~/picamserver
screen -d -m python3 camdaemon.py
screen -d -m flask --app main run -h 0.0.0.0 --reload
