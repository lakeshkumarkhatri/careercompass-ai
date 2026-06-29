from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_check():
    """Verify GET /api/health returns expected response."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "CareerCompass AI"
    }
