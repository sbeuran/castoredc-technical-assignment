#!/bin/bash

# Exit on error
set -e

# Get directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Debug information
echo "Current directory: $SCRIPT_DIR"
echo "Python version: $(python3 --version)"
echo "Python location: $(which python3)"

# Install pip if not available
echo "Installing/Upgrading pip..."
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
python3 -m pip install --user -r "$SCRIPT_DIR/requirements.txt"
python3 -m pip install --user gunicorn

# Set environment variables
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
export PATH="$HOME/.local/bin:$PATH"

# Start Gunicorn
echo "Starting Gunicorn..."
echo "Using Python: $(which python3)"
echo "Gunicorn path: $(which gunicorn)"
gunicorn \
    --config "$SCRIPT_DIR/gunicorn.conf.py" \
    --chdir "$SCRIPT_DIR" \
    --bind=0.0.0.0:8000 \
    --timeout 600 \
    --access-logfile '-' \
    --error-logfile '-' \
    --log-level info \
    "app.main:app" 