#!/bin/bash

# Set the working directory
cd /home/site/wwwroot

# Set environment variables
export PYTHONPATH=/home/site/wwwroot
export PORT=8000

# Start Gunicorn with config file
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --log-level debug --access-logfile - --error-logfile - --bind=0.0.0.0:8000 