#!/bin/bash

# Exit on error
set -e

# Get directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set environment variables
export PATH="$SCRIPT_DIR/venv/bin:$PATH"
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Activate virtual environment if it exists
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
fi

# Start Gunicorn
gunicorn \
    --config "$SCRIPT_DIR/gunicorn.conf.py" \
    --chdir "$SCRIPT_DIR" \
    --bind=0.0.0.0:8000 \
    --timeout 600 \
    --access-logfile '-' \
    --error-logfile '-' \
    --log-level info \
    "app.main:app" 