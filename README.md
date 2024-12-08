Don't use this; it's gross.

# But Why
It's a simple web server. It lets you view a Pi camera via a web page that
refreshes every few seconds. It's currently hackish and shouldn't be run in
any environment that matters.

# Installation

Start with a clean install of [Raspberry Pi OS Lite 64bit](https://www.raspberrypi.com/software/operating-systems/), then `apt` install a bunch of stuff, clone the repo, `cd` into it and set up a python virtual envorinment, activate it and install python requirements with the following code: 

```
sudo apt install -y git screen python3-picamera2 python3-dotenv    # From https://pypi.org/project/picamera2/ - installs a LOT - be patient!
git clone https://github.com/NegativeK/picamserver.git
cd picamserver
mkdir data
python3 -m venv --system-site-packages venv # From https://forums.raspberrypi.com/viewtopic.php?t=361758
. venv/bin/activate
pip install -r requirements.txt
```

# Running
`bash forever.sh`

forever.sh runs the flask server in a screen session. If the server dies, it's
forcibly restarted. Hit ctrl+c a lot in the screen session to kill it. The
server will die if there are simultaneous requests against the camera. (I 
warned you that this is gross.)

# Configuration
Defaults:
* The image file is stored at `picamserver/data/photo.jpg`.
* Session tokens are stored in `picamserver/listeners`.
* Session tokens are removed by the camera daemon 30 seconds after the client stops loading images.
* The camera daemon refreshes the image file ever 2 seconds.

All of these values can be changed at the top of config.py.

# Todo
* Scale down the image via GET parameters
