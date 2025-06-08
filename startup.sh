#!/bin/bash

# Navigate to app directory
cd /home/site/wwwroot

# Add the current directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:/home/site/wwwroot

# Install dependencies
pip install -r requirements.txt

# Start the application with debug logging
gunicorn app.main:app --bind=0.0.0.0:8000 --workers=4 --timeout 600 --access-logfile - --error-logfile - --log-level debug 