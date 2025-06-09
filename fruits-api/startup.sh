#!/bin/bash

# Set the working directory
cd /home/site/wwwroot

# Set environment variables
export PYTHONPATH=/home/site/wwwroot
export PORT=8000

# Start Gunicorn with the correct app module
exec gunicorn --chdir /home/site/wwwroot --bind=0.0.0.0:8000 --workers=4 --timeout=600 --access-logfile=- --error-logfile=- --log-level=info "app.main:app" 