#!/bin/bash

# Exit on error
set -e

# Get directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Debug information
echo "Current directory: $SCRIPT_DIR"
echo "Python version: $(python3 --version)"
echo "Python location: $(which python3)"
echo "Pip version: $(pip3 --version)"

# Install dependencies directly without virtual environment
echo "Installing dependencies..."
pip3 install --user -r "$SCRIPT_DIR/requirements.txt"
pip3 install --user gunicorn

# Set environment variables
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Start Gunicorn
echo "Starting Gunicorn..."
echo "Using Python: $(which python3)"
~/.local/bin/gunicorn \
    --config "$SCRIPT_DIR/gunicorn.conf.py" \
    --chdir "$SCRIPT_DIR" \
    --bind=0.0.0.0:8000 \
    --timeout 600 \
    --access-logfile '-' \
    --error-logfile '-' \
    --log-level info \
    "app.main:app" 