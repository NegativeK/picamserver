Don't use this; it's gross.

# But Why
It's a simple web server. It lets you view a Pi camera via a web page that
refreshes every few seconds. It's currently hackish and shouldn't be run in
any environment that matters.

# Prerequisites 

You'll need the following hardware:

* Raspberry Pi - This project developed on a [Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
* Raspberry Pi Camera Module - This project developed on an [HQ](https://www.amazon.com/dp/B08B1QLGHS) and a 
 [V2](https://www.amazon.com/dp/B01ER2SKFS)
* MicroSD Card with [Raspberry Pi OS Lite 64bit](https://www.raspberrypi.com/software/operating-systems/)

Before proceeding, consider testing your camera to make sure it is wired up correctly and works. The ribbon cable
can be easily be inserted backwards either on the Pi side or the camera side - be careful!

# Installation

The first `apt install...` call installs a LOT - be patient!

```
sudo apt install -y python3-flask git screen python3-picamera2 python3-dotenv
git clone https://github.com/NegativeK/picamserver.git
cd picamserver
mkdir -p data listeners
```

python3-picamera2 installation instructions from [PyPi](https://pypi.org/project/picamera2/) .

Note that there's no recommendation to use a virtual environment. This code 
assumes a Raspberry Pi and is intended to work on Raspbian, so it uses the apt
packages.

# Running
`./main.py`

main forks a process for the camera and a process for the flask server. If
either one dies, main kills the other.

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
