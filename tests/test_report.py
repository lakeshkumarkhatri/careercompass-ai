import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_career_report_no_file():
    # Test that it fails without a file
    response = client.post("/api/career-report")
    assert response.status_code == 422 # FastAPI validation error
