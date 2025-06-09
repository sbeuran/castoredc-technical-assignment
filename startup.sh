#!/bin/bash

# Enable bash debugging
set -x

# Log startup information
echo "Starting application setup..."
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Available Python packages: $(pip list)"

# Set the working directory
cd /home/site/wwwroot
echo "Changed to directory: $(pwd)"

# Set environment variables
export PYTHONPATH=/home/site/wwwroot
export PORT=8000
export PYTHONUNBUFFERED=1

# Create SQLite directory if using SQLite
mkdir -p /home/site/wwwroot/data
chmod 777 /home/site/wwwroot/data

# Log environment variables (excluding sensitive data)
echo "Environment variables set:"
env | grep -v "PASSWORD" | grep -v "SECRET"

# Start Gunicorn with config file
echo "Starting Gunicorn..."
exec gunicorn \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --log-level debug \
    --access-logfile - \
    --error-logfile - \
    --capture-output \
    --enable-stdio-inheritance \
    app.main:app 