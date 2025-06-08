from fastapi import FastAPI
from app.api.v1.routes import router as api_router, init_data
from app.database import engine, SessionLocal
from app import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize data on startup
db = SessionLocal()
try:
    init_data(db)
finally:
    db.close()

app = FastAPI(
    title="Fruits API",
    description="A comprehensive API for managing fruits, nutritional information, and suppliers",
    version="1.0.0"
)

# Include routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Fruits API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 