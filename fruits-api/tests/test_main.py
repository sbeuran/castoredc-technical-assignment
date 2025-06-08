import pytest
from fastapi.testclient import TestClient
from app.main import app, init_db
import os

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    # Use an in-memory database for testing
    global DATABASE_FILE
    app.DATABASE_FILE = ":memory:"
    init_db()
    yield
    # Clean up after tests

def test_create_fruit():
    response = client.post(
        "/fruits",
        json={"fruit": "apple", "color": "red"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["fruit"] == "apple"
    assert data["color"] == "red"
    assert "id" in data

def test_get_fruits():
    # First create a fruit
    client.post("/fruits", json={"fruit": "banana", "color": "yellow"})
    
    response = client.get("/fruits")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)

def test_get_fruit():
    # First create a fruit
    create_response = client.post(
        "/fruits",
        json={"fruit": "grape", "color": "purple"}
    )
    fruit_id = create_response.json()["id"]
    
    response = client.get(f"/fruits/{fruit_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["fruit"] == "grape"
    assert data["color"] == "purple"

def test_get_nonexistent_fruit():
    response = client.get("/fruits/9999")
    assert response.status_code == 404 