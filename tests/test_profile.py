import pytest
from fastapi.testclient import TestClient
from app import app
import json
from pathlib import Path

client = TestClient(app)

def test_create_and_get_profile():
    user_id = "test_user_123"
    profile_data = {
        "user_id": user_id,
        "email": "test@example.com",
        "career_goals": "Senior Software Engineer",
        "skills": ["python", "fastapi"],
        "completed_courses": ["Intro to Python"],
        "preferences": {"theme": "dark"}
    }
    
    # Test Create
    response = client.post("/api/profile", json=profile_data)
    assert response.status_code == 200
    assert response.json()["user_id"] == user_id
    
    # Test Get
    response = client.get(f"/api/profile/{user_id}")
    assert response.status_code == 200
    assert response.json()["user_id"] == user_id
    
    # Cleanup (simple file-based cleanup)
    data_path = Path("data/users.json")
    if data_path.exists():
        with open(data_path, "r", encoding="utf-8") as f:
            users = json.load(f)
        if user_id in users:
            del users[user_id]
            with open(data_path, "w", encoding="utf-8") as f:
                json.dump(users, f)
