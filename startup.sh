#!/bin/bash

# Exit on error
set -e

# Get directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create and activate virtual environment if it doesn't exist
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python -m venv "$SCRIPT_DIR/venv"
    source "$SCRIPT_DIR/venv/bin/activate"
    echo "Installing dependencies..."
    python -m pip install --upgrade pip
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
gunicorn \
    --config "$SCRIPT_DIR/gunicorn.conf.py" \
    --chdir "$SCRIPT_DIR" \
    --bind=0.0.0.0:8000 \
    --timeout 600 \
    --access-logfile '-' \
    --error-logfile '-' \
    --log-level info \
    "app.main:app" 