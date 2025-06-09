from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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
async def health_check():
    return {"status": "healthy"}

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