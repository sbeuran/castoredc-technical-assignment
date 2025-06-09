#!/bin/bash

# Set the working directory
cd /home/site/wwwroot

# Set environment variables
export PYTHONPATH=/home/site/wwwroot
export PORT=8000

# Start Gunicorn with config file
exec gunicorn -c /home/site/wwwroot/gunicorn.conf.py 