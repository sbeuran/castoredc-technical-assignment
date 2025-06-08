import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import Fruit, NutritionalInfo, Supplier

# Set up test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the get_db dependency
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the Fruits API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

def test_get_all_data_empty(client):
    response = client.get("/api/v1/get_all_data")
    assert response.status_code == 200
    data = response.json()
    assert "fruits" in data
    assert "total_fruits" in data
    assert "total_suppliers" in data
    assert "total_nutritional_records" in data
    assert data["total_fruits"] == 0

def test_get_all_data_with_sample_data(client, db_session):
    # Create sample data
    fruit = Fruit(
        name="Apple",
        color="Red",
        taste="Sweet",
        origin_country="USA",
        price_per_kg=2.99
    )
    db_session.add(fruit)
    db_session.flush()

    nutritional_info = NutritionalInfo(
        fruit_id=fruit.id,
        calories=52,
        carbohydrates=14,
        protein=0.3,
        fat=0.2,
        fiber=2.4,
        vitamins="A, C"
    )
    db_session.add(nutritional_info)

    supplier = Supplier(
        name="Fresh Farms",
        country="USA",
        contact_email="contact@freshfarms.com",
        rating=4.5
    )
    db_session.add(supplier)
    db_session.flush()

    fruit.suppliers.append(supplier)
    db_session.commit()

    # Test the endpoint
    response = client.get("/api/v1/get_all_data")
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_fruits"] == 1
    assert data["total_suppliers"] == 1
    assert data["total_nutritional_records"] == 1
    
    fruit_data = data["fruits"][0]
    assert fruit_data["name"] == "Apple"
    assert fruit_data["color"] == "Red"
    assert fruit_data["nutritional_info"]["calories"] == 52
    assert len(fruit_data["suppliers"]) == 1
    assert fruit_data["suppliers"][0]["name"] == "Fresh Farms"

def test_get_fruits_empty(client):
    response = client.get("/api/v1/fruits")
    assert response.status_code == 200
    assert response.json() == []

def test_get_fruits(client, db_session):
    # Create test fruit
    fruit = Fruit(name="apple", color="red")
    db_session.add(fruit)
    db_session.commit()

    response = client.get("/api/v1/fruits")
    assert response.status_code == 200
    fruits = response.json()
    assert len(fruits) == 1
    assert fruits[0]["id"] == fruit.id
    assert fruits[0]["fruit"] == "apple"
    assert fruits[0]["color"] == "red"

def test_get_fruit_by_id(client, db_session):
    # Create test fruit
    fruit = Fruit(name="apple", color="red")
    db_session.add(fruit)
    db_session.commit()

    response = client.get(f"/api/v1/fruits/{fruit.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == fruit.id
    assert data["fruit"] == "apple"
    assert data["color"] == "red"

def test_get_fruit_not_found(client):
    response = client.get("/api/v1/fruits/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Fruit not found"

def test_create_fruit(client):
    fruit_data = {
        "fruit": "apple",
        "color": "red"
    }
    response = client.post("/api/v1/fruits", json=fruit_data)
    assert response.status_code == 200
    data = response.json()
    assert data["fruit"] == "apple"
    assert data["color"] == "red"
    assert "id" in data 