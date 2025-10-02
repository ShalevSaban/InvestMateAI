import pytest

class TestAuth:
    def test_login_success(self, client):
        """Test successful login"""
        # Create agent first
        agent_data = {
            "full_name": "Test User",
            "email": "login@example.com",
            "password": "testpass123",
            "phone_number": "0501234567"
        }
        client.post("/agents/", json=agent_data)

        # Login
        response = client.post("/auth/login", data={
            "username": agent_data["email"],
            "password": agent_data["password"]
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_wrong_password(self, client):
        """Test login with wrong password"""
        response = client.post("/auth/login", data={
            "username": "test@example.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
