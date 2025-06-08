#!/bin/bash

# Exit on error
set -e

# Get directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set Python paths for Azure App Service
PYTHON_DIR="/usr/local/python/3.11/bin"
export PATH="$PYTHON_DIR:$PATH"

echo "Python location: $(which python3)"
echo "Current directory: $SCRIPT_DIR"

# Create and activate virtual environment if it doesn't exist
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$SCRIPT_DIR/venv"
    source "$SCRIPT_DIR/venv/bin/activate"
    echo "Installing dependencies..."
    python3 -m pip install --upgrade pip
    pip install -r "$SCRIPT_DIR/requirements.txt"
    pip install gunicorn
else
    echo "Activating existing virtual environment..."
    source "$SCRIPT_DIR/venv/bin/activate"
fi

# Set environment variables
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Start Gunicorn
echo "Starting Gunicorn..."
echo "Using Python: $(which python3)"
echo "Using Gunicorn: $(which gunicorn)"
gunicorn \
    --config "$SCRIPT_DIR/gunicorn.conf.py" \
    --chdir "$SCRIPT_DIR" \
    --bind=0.0.0.0:8000 \
    --timeout 600 \
    --access-logfile '-' \
    --error-logfile '-' \
    --log-level info \
    "app.main:app" 