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