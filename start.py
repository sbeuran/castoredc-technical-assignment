import uvicorn
from app.database import Base, engine

def main():
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Start the server
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main() 