from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sqlalchemy.orm import Session
from app.database import get_db
import logging
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Fruits API",
    description="A simple API for managing fruits",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Fruits API"}

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        db_status = f"unhealthy: {str(e)}"

    # Get environment information
    env_info = {
        "WEBSITE_HOSTNAME": os.getenv("WEBSITE_HOSTNAME", "not set"),
        "PYTHON_VERSION": sys.version,
        "DATABASE_TYPE": "MySQL" if os.getenv("MYSQL_HOST") else "SQLite",
    }

    return {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "database_status": db_status,
        "environment": env_info,
        "application_status": "running"
    }

@app.get("/api/v1/get_all_data")
async def get_all_data():
    # Temporary mock data
    return {
        "fruits": [
            {"id": 1, "name": "Apple", "color": "Red"},
            {"id": 2, "name": "Banana", "color": "Yellow"},
            {"id": 3, "name": "Orange", "color": "Orange"}
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 