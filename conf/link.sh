#!/bin/bash

# link nginx
sudo cp -f journal-nginx.conf /etc/nginx/conf.d/

# link gunicorn
sudo cp -f journal-gunicorn.conf /etc/supervisor/conf.d/

sudo cp -f journal-memcached.conf /etc/supervisor/conf.d/