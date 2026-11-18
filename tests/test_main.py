from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_items():
    response = client.get("/items")
    assert response.status_code == 200
    assert 1 in response.json() or "1" in response.json()

def test_add_item():
    response = client.post("/items/99", json={"name": "Switch", "quantity": 2})
    assert response.status_code == 201
    assert response.json()["item"]["name"] == "Switch"