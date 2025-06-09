#!/bin/bash
set -e

# Print Python version and environment info
echo "Python version:"
python --version

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the application
echo "Starting application..."
gunicorn app.main:app --bind=0.0.0.0:8000 --workers=4 --worker-class uvicorn.workers.UvicornWorker --timeout 600 