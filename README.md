# Installation

sudo apt install -y python3-picamera2 # From https://pypi.org/project/picamera2/

python3 -m venv --system-site-packages env # From https://forums.raspberrypi.com/viewtopic.php?t=361758

. venv/bin/activate
pip install -r requirements.txt

# TODO
* Scale down the image via GET parameters
* Save the image (in /run/shm?) and let clients load that
    * Requires a global for the camera object
