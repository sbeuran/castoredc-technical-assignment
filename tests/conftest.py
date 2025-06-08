import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set testing environment variable before importing any app modules
os.environ["TESTING"] = "true"

# Import app modules after setting environment variable
from app.main import app
from app.database import Base, get_db
from app.models import Fruit, NutritionalInfo, Supplier

# Create test database engine
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session")
def engine():
    return test_engine

@pytest.fixture(scope="function", autouse=True)
def create_tables(engine):
    """Create all tables before each test and drop them after"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(create_tables):
    """Provide a clean database session for each test"""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture
def client(db_session):
    """Provide a test client with a clean database session"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # Session is handled by the db_session fixture
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear() 