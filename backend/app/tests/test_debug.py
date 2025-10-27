def test_basic():
    """Super simple test to check if pytest works"""
    assert 1 + 1 == 2
    print("✅ Basic test works!")


def test_imports():
    """Test if we can import our app modules"""
    try:
        from app.main import app
        print("✅ Can import app.main")
        assert app is not None
    except Exception as e:
        print(f"❌ Import error: {e}")
        raise


def test_fastapi():
    """Test if FastAPI TestClient works"""
    try:
        from fastapi.testclient import TestClient
        from app.main import app

        client = TestClient(app)
        print("✅ TestClient created successfully")
        assert client is not None
    except Exception as e:
        print(f"❌ TestClient error: {e}")
        raise