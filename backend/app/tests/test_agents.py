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

    def test_empty_agents(self, client,clean_agent_db):
        response = client.get("/agents/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_agents(self, client,clean_agent_db):
        # 1. Create Agents
        agent1 = {
            "full_name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "phone_number": "0501234567"
        }
        agent2 = {
            "full_name": "David Moses",
            "email": "davidmoses@example.com",
            "password": "password123",
            "phone_number": "0501234568"
        }
        client.post("/agents/", json=agent1)
        client.post("/agents/", json=agent2)

        # 2. test
        response = client.get("/agents/")
        assert response.status_code == 200
        assert len(response.json()) == 2

        # 3. Verify actual data
        agents = response.json()
        emails = [agent["email"] for agent in agents]
        assert "john@example.com" in emails
        assert "davidmoses@example.com" in emails

        # 4. Check structure
        assert "id" in agents[0]
        assert "password" not in agents[0]

    def test_get_agent_by_id(self, client, sample_agent):
        """Test getting specific agent by ID"""
        agent_id = sample_agent["id"]

        response = client.get(f"/agents/{agent_id}")

        assert response.status_code == 200
        assert response.json()["email"] == sample_agent["email"]
        assert response.json()["id"] == agent_id
