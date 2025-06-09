from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging
import sys

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

load_dotenv()

# Use SQLite by default for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fruits.db")
logger.info(f"Database configuration: URL type: {DATABASE_URL.split(':')[0]}")

try:
    if DATABASE_URL.startswith("sqlite"):
        logger.info("Using SQLite database")
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    else:
        # MySQL configuration for production
        logger.info("Attempting MySQL database connection")
        required_env_vars = ["MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_HOST", "MYSQL_DATABASE"]
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            logger.info("Available environment variables: " + ", ".join(os.environ.keys()))
            # Fallback to SQLite if MySQL configuration is incomplete
            logger.warning("Falling back to SQLite database due to missing MySQL configuration")
            DATABASE_URL = "sqlite:///./fruits.db"
            engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        else:
            MYSQL_USER = os.getenv("MYSQL_USER")
            MYSQL_HOST = os.getenv("MYSQL_HOST")
            MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
            logger.info(f"Connecting to MySQL at {MYSQL_HOST}/{MYSQL_DATABASE} with user {MYSQL_USER}")
            
            try:
                DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{os.getenv('MYSQL_PASSWORD')}@{MYSQL_HOST}/{MYSQL_DATABASE}?ssl_ca=None"
                engine = create_engine(DATABASE_URL)
                # Test the connection
                with engine.connect() as conn:
                    result = conn.execute("SELECT 1")
                    logger.info("MySQL connection test successful")
            except Exception as mysql_error:
                logger.error(f"Failed to connect to MySQL: {str(mysql_error)}")
                logger.warning("Falling back to SQLite database due to MySQL connection failure")
                DATABASE_URL = "sqlite:///./fruits.db"
                engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    # Test the final database connection
    with engine.connect() as conn:
        logger.info("Successfully connected to database")
except Exception as e:
    logger.error(f"Critical database error: {str(e)}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 