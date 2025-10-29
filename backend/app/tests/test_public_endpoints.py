class TestPublicEndpoints:
    def test_public_properties(self, client):
        """Test public properties endpoint (no auth required)"""
        response = client.get("/public/properties")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_config_values(self):
        from app.config import Config
        assert Config.SECRET_KEY is not None