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

    def test_update_property(self, client, auth_token, sample_property):
        headers = {"Authorization": f"Bearer {auth_token}"}
        property_id = sample_property

        update_data = {"price": 1500000}
        response = client.put(f"/properties/{property_id}", json=update_data, headers=headers)

        assert response.status_code == 200



