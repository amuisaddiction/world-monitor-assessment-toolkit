from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "World Monitor Security Assessment API"}

def test_start_scan():
    response = client.post("/api/scans", json={"target_url": "http://127.0.0.1:8080"})
    assert response.status_code == 200
    assert "id" in response.json()

def test_start_scan_invalid_target():
    response = client.post("/api/scans", json={"target_url": "https://www.worldmonitor.app"})
    assert response.status_code == 400
