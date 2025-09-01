import pytest


class TestAgents:
    def test_create_agent(self, client):
        """Test agent creation"""
        data = {
            "full_name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "phone_number": "0501234567"
        }
        response = client.post("/agents/", json=data)
        assert response.status_code == 201
        assert response.json()["email"] == data["email"]

    def test_duplicate_email_fails(self, client):
        """Test duplicate email registration fails"""
        data = {
            "full_name": "John Doe",
            "email": "duplicate@example.com",
            "password": "password123",
            "phone_number": "0501234567"
        }
        # First registration
        client.post("/agents/", json=data)

        # Second registration should fail
        response = client.post("/agents/", json=data)
        assert response.status_code == 400


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


class TestProperties:
    def test_create_property(self, client, auth_token):
        """Test property creation"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        property_data = {
            "city": "Tel Aviv",
            "address": "123 Dizengoff St",
            "price": 2000000,
            "rooms": 3,
            "floor": 2,
            "property_type": "apartment",
            "description": "Nice apartment"
        }

        response = client.post("/properties/", json=property_data, headers=headers)
        assert response.status_code == 201
        assert response.json()["city"] == "Tel Aviv"

    def test_get_properties_requires_auth(self, client):
        """Test that getting properties requires authentication"""
        response = client.get("/properties/")
        assert response.status_code == 401

    def test_get_properties_with_auth(self, client, auth_token):
        """Test getting properties with authentication"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.get("/properties/", headers=headers)
        assert response.status_code == 200


class TestGPTChat:
    def test_chat_endpoint(self, client, auth_token):
        """Test GPT chat endpoint"""
        headers = {"Authorization": f"Bearer {auth_token}"}

        response = client.post("/gpt/chat/",
                               json={"question": "Show me apartments in Tel Aviv"},
                               headers=headers)
        assert response.status_code == 200
        assert "message" in response.json()

    def test_chat_with_different_scenarios(self, flexible_client, auth_token):
        """Test chat with different GPT responses"""
        client, mock_gpt = flexible_client
        headers = {"Authorization": f"Bearer {auth_token}"}

        # Test scenario 1: Price filters
        mock_gpt.return_value = {
            "city": "Tel Aviv",
            "min_price": 1000000,
            "max_price": 2000000,
            "description_filters": ["pool", "balcony"]
        }

        response = client.post("/gpt/chat/",
                               json={"question": "Apartments with pool, 1-2M"},
                               headers=headers)
        assert response.status_code == 200
        assert response.json()["filters"]["min_price"] == 1000000

        # Test scenario 2: Rental focused
        mock_gpt.return_value = {
            "city": "Haifa",
            "rental_estimate_max": 5000,
            "yield_percent": 4.0,
            "description_filters": []
        }

        response = client.post("/gpt/chat/",
                               json={"question": "Investment properties in Haifa"},
                               headers=headers)
        assert response.status_code == 200
        assert response.json()["filters"]["rental_estimate_max"] == 5000


class TestPublicEndpoints:
    def test_public_properties(self, client):
        """Test public properties endpoint (no auth required)"""
        response = client.get("/public/properties")
        assert response.status_code == 200
        assert isinstance(response.json(), list)