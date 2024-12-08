Don't use this; it's gross.

# But Why
It's a simple web server. It lets you view a Pi camera via a web page that
refreshes every few seconds. It's currently hackish and shouldn't be run in
any environment that matters.

# Installation

Start with a clean install of [Raspberry Pi OS Lite 64bit](https://www.raspberrypi.com/software/operating-systems/), and `apt` install a bunch of stuff. Installs a LOT - be patient!

```
sudo apt install -y flask git screen python3-picamera2 python3-dotenv
git clone https://github.com/NegativeK/picamserver.git
cd picamserver
mkdir data
```

python3-picamera2 installation instructions from https://pypi.org/project/picamera2/ .

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
