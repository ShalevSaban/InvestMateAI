from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_agent():
    agent_data = {
        "full_name": "Test Agent",
        "email": "agent@example.com",
        "password": "123456",
        "phone_number": "0521234567"
    }

    res = client.post("/agents/", json=agent_data)
    assert res.status_code == 201
    return res.json()["id"]


def test_property_crud():
    agent_id = create_agent()

    new_property = {
        "agent_id": agent_id,
        "city": "Tel Aviv",
        "address": "beeri",
        "price": 20000,
        "yield_percent": 1,
        "property_type": "apartment",
        "rooms": 2,
        "floor": 4,
        "description": "string",
        "rental_estimate": 0
    }

    # CREATE
    res = client.post("/properties/", json=new_property)
    assert res.status_code == 201
    prop_id = res.json()["id"]

    # GET ALL
    res = client.get("/properties/")
    assert res.status_code == 200
    assert any(p["id"] == prop_id for p in res.json())

    # GET ONE
    res = client.get(f"/properties/{prop_id}")
    assert res.status_code == 200
    assert res.json()["city"] == "Tel Aviv"

    # UPDATE
    updated = new_property.copy()
    updated["price"] = 2000000
    res = client.put(f"/properties/{prop_id}", json=updated)
    assert res.status_code == 200
    assert res.json()["price"] == 2000000

    # DELETE
    res = client.delete(f"/properties/{prop_id}")
    assert res.status_code == 204

    # VERIFY DELETE
    res = client.get(f"/properties/{prop_id}")
    assert res.status_code == 404
