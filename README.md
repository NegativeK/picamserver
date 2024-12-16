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
mkdir data listeners
```

python3-picamera2 installation instructions from https://pypi.org/project/picamera2/ .

Note that there's no recommendation to use a virtual environment. This code 
assumes a Raspberry Pi and is intended to work on Raspbian, so it uses the apt
packages.

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

# Development
Because the install just uses Debian packages, you don't need a virtual env
to do development. However, if you would like to install the linter and type
checker, you can follow the instructions below.

To set up a development virtual environment in your local repo, run the
following commands:
```
python3 -m venv venv
. venv/bin/activate
pip install --editable .[dev]
```

Whether you're in a virtualenv or not, you can start the processes with:
```
python3 camdaemon.py
python3 -m flask --app main run -h 0.0.0.0 --reload
```

If you have make installed, there is a Makefile for development. To do linting
and type checking, you can run:
```
make static_checking
```
This will enable the virtualenv and run:
```
ruff check
mypy *.py
```
