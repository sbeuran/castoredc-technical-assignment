#!/bin/bash

# Initialize the database
python -m app.init_db

# Start the application with Gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 