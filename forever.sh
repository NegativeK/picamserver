#!/bin/bash
cd ~/picamserver
screen -d -m ./run_flask.sh
screen -d -m ./run_cam.sh
