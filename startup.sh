#!/bin/bash

# Exit on error
set -e

# Get directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment
source $SCRIPT_DIR/venv/bin/activate

# Start Gunicorn
exec gunicorn \
    --config $SCRIPT_DIR/gunicorn.conf.py \
    --chdir $SCRIPT_DIR \
    --bind=0.0.0.0:8000 \
    --timeout 600 \
    --access-logfile '-' \
    --error-logfile '-' \
    --log-level info \
    "app.main:app" 