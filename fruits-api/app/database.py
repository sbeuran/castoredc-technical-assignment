from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER", "mysqladmin")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "P@ssw0rd123!")
MYSQL_HOST = os.getenv("MYSQL_HOST", "fruits-api-db.mysql.database.azure.com")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "fruits")

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 