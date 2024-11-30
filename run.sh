#!/bin/bash
. venv/bin/activate
while true
do
	flask --app main run -h 0.0.0.0 --reload
	sleep 1
done
