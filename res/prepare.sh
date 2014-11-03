#!/bin/sh
sudo chown www-data -R /usr/share/zoneinfo/*
sudo cp -R /lib/owncloud /var/www
sudo mkdir -p /var/www/owncloud/data
sudo chown www-data:www-data -R /var/www/owncloud/data
sudo cp /var/owncloud/res/mount.json /var/www/owncloud/data
sudo chown www-data:www-data /var/www/owncloud/data/mount.json
sudo chmod 770 /var/www/owncloud/data
