from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


# Import FastAPI app
from app.main import app


# Import database
from app.database import get_db, Base


# Import ALL models to register them
from app.models.agent import Agent
from app.models.property import Property
from app.models.conversation import Conversation, Message
from app.models.cached_criteria import CachedCriteria
from app.models.insight_log import InsightLog


# 🔧 FIX: Use StaticPool to ensure same database connection
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # 👈 This ensures same connection is reused!
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def flexible_client():
    """Test client where you can control GPT responses in individual tests"""
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db

    # Mock external services but don't set default return values
    with patch('app.services.gpt_service.GPTService.extract_search_criteria') as mock_gpt, \
            patch('app.utils.aws_s3.upload_file_to_s3') as mock_s3_upload, \
            patch('app.utils.aws_s3.generate_presigned_view_url') as mock_s3_url:
        # Set defaults for AWS but let tests control GPT
        mock_s3_upload.return_value = True
        mock_s3_url.return_value = "https://test-image-url.com/image.jpg"

        with TestClient(app) as test_client:
            yield test_client, mock_gpt

    app.dependency_overrides.clear()

@pytest.fixture
def client():

    # Check what's registered before creating tables

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Check what tables were actually created
    inspector = inspect(engine)
    created_tables = inspector.get_table_names()

    # Override database BEFORE creating TestClient
    app.dependency_overrides[get_db] = override_get_db

    # Create test client
    with TestClient(app) as test_client:
        yield test_client

    # Cleanup
    app.dependency_overrides.clear()


@pytest.fixture
def auth_token(client):

    # Create test user
    user_data = {
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "testpass123",
        "phone_number": "0501234567"
    }

    response = client.post("/agents/", json=user_data)
    if response.status_code != 201:
        print(f"Registration error: {response.json()}")

    login_response = client.post("/auth/login", data={
        "username": user_data["email"],
        "password": user_data["password"]
    })
    print(f"Login response: {login_response.status_code}")
    if login_response.status_code != 200:
        print(f"Login error: {login_response.json()}")

    return login_response.json()["access_token"]