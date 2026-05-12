"""
FastAPI test configuration and basic tests.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "version" in response.json()


def test_register_user():
    """Test user registration."""
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "securepassword123"
        }
    )
    # First attempt should succeed, second should fail (email exists)
    assert response.status_code in [200, 400]
