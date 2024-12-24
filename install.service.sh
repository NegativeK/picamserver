#!/usr/bin/env bash

set -e

directory=$(pwd)
user=$(echo $USER)

read -p "
-------------------------------------------------------
Press 'Enter' if your user has 'sudo' and you're ready to install the Picamserver services to start at boot.

Press 'ctrl + c' if you don't want continue.

Using directory '${directory}' with user '${user}' for install.
" </dev/tty

echo "
-------------------------------------------------------
Installing...

(be patient - this might take a sec!)
"

sudo cp picamserver-image.service /etc/systemd/system/
sudo cp picamserver-web.service /etc/systemd/system/
sudo sed -i "s|WORK_DIR|${directory}|g" /etc/systemd/system/picamserver-image.service
sudo sed -i "s|WORK_DIR|${directory}|g" /etc/systemd/system/picamserver-web.service
sudo sed -i "s|USER|${user}|g" /etc/systemd/system/picamserver-web.service
sudo sed -i "s|USER|${user}|g" /etc/systemd/system/picamserver-image.service
sudo systemctl daemon-reload
sudo systemctl enable picamserver-web
sudo systemctl start picamserver-web
sudo systemctl enable picamserver-image
sudo systemctl start picamserver-image


echo "
-------------------------------------------------------
Install complete! run these commands as needed:

IMAGE SERVER
sudo systemctl start picamserver-image
sudo systemctl stop picamserver-image
sudo systemctl status picamserver-image

WEB SERVER
sudo systemctl start picamserver-web
sudo systemctl stop picamserver-web
sudo systemctl status picamserver-web

WATCHING LOGS:
journalctl --follow --unit picamserver-\*     # tail both
journalctl --follow --unit picamserver-image  # tail just image server
journalctl --follow --unit picamserver-web    # tail just web server

"