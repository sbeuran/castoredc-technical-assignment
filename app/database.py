from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Use SQLite by default for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fruits.db")
logger.info(f"Initializing database with URL: {DATABASE_URL}")

try:
    if DATABASE_URL.startswith("sqlite"):
        logger.info("Using SQLite database")
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    else:
        # MySQL configuration for production
        logger.info("Using MySQL database")
        required_env_vars = ["MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_HOST", "MYSQL_DATABASE"]
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            # Fallback to SQLite if MySQL configuration is incomplete
            logger.info("Falling back to SQLite database")
            DATABASE_URL = "sqlite:///./fruits.db"
            engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        else:
            MYSQL_USER = os.getenv("MYSQL_USER")
            MYSQL_HOST = os.getenv("MYSQL_HOST")
            MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
            # Don't log the password
            logger.info(f"Connecting to MySQL at {MYSQL_HOST}/{MYSQL_DATABASE} with user {MYSQL_USER}")
            DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{os.getenv('MYSQL_PASSWORD')}@{MYSQL_HOST}/{MYSQL_DATABASE}?ssl_ca=None"
            engine = create_engine(DATABASE_URL)

    # Test the database connection
    with engine.connect() as conn:
        logger.info("Successfully connected to database")
except Exception as e:
    logger.error(f"Error connecting to database: {str(e)}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 