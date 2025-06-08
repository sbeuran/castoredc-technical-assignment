from fastapi import FastAPI
from app.api.v1.routes import router as api_router, init_data
from app.database import engine, SessionLocal
from app import models
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting application initialization")

try:
    # Create database tables
    logger.info("Creating database tables")
    models.Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")

    # Initialize data on startup
    logger.info("Initializing database data")
    db = SessionLocal()
    try:
        init_data(db)
        logger.info("Database data initialized successfully")
    finally:
        db.close()
except Exception as e:
    logger.error(f"Error during initialization: {str(e)}")
    raise

app = FastAPI(
    title="Fruits API",
    description="A comprehensive API for managing fruits, nutritional information, and suppliers",
    version="1.0.0"
)

# Include routers
logger.info("Setting up API routes")
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Fruits API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint to verify the application is running"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting uvicorn server")
    uvicorn.run(app, host="0.0.0.0", port=8000) 