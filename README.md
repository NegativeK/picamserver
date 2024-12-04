Don't use this; it's gross.

# But Why
It's a simple web server. It lets you view a Pi camera via a web page that
refreshes every few seconds. It's currently hackish and shouldn't be run in
any environment that matters.

# Installation

```
sudo apt install -y python3-picamera2 # From https://pypi.org/project/picamera2/
python3 -m venv --system-site-packages venv # From https://forums.raspberrypi.com/viewtopic.php?t=361758
. venv/bin/activate`
pip install -r requirements.txt
```

# Running
`bash forever.sh`

forever.sh runs the flask server in a screen session. If the server dies, it's
forcibly restarted. Hit ctrl+c a lot in the screen session to kill it. The
server will die if there are simultaneous requests against the camera. (I 
warned you that this is gross.)

# Todo
* Scale down the image via GET parameters
* Save the image (in /run/shm?) and let clients load that
    * Each session stores a unique timestamped file in a directory
    * If the directory has any files, the camera daemon takes photos and
      updates the image file
    * Sessions clean up their timestamped file
    * The camera daemon removes timestamped files that are too old
