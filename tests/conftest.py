import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app.main import app
from fastapi.testclient import TestClient
from datetime import datetime, timezone

@pytest.fixture
def client():
    client = TestClient(app)
    return client

@pytest.fixture
def mock_user():
    fixed_date = datetime(2025,1,1,12,0,0,tzinfo=timezone.utc)
    mock_user = {
        "_id": "user123",
        "username":"test_user",
        "email": "test@example.com",
        "hashed_password": "hashed_password_123",
        "created_at":fixed_date
    }
    return mock_user

@pytest.fixture
def mock_payload():
    mock_payload = {
            "sub":"507f1f77bcf86cd799439011"
            }

    return mock_payload

@pytest.fixture
def mock_verify_token(mocker, mock_payload):
    mock_verify_token = mocker.MagicMock()
    mock_verify_token.return_value = mock_payload

    mocker.patch("app.utils.dependencies.verify_token", mock_verify_token)
    return mock_verify_token

@pytest.fixture
def mock_token(mocker, mock_user, client):
    mock_get_collection = mocker.MagicMock()
    mock_get_collection.find_one.return_value = mock_user

    mock_verify_password = mocker.MagicMock(return_value=True)
    
    mock_create_access_token = mocker.MagicMock()
    mock_token = "falsetoken"
    mock_create_access_token.return_value = mock_token

    mocker.patch("app.routes.auth.get_collection", return_value=mock_get_collection)
    mocker.patch("app.routes.auth.verify_password", mock_verify_password)
    mocker.patch("app.routes.auth.create_access_token", mock_create_access_token)
    
    login_data = {
        "email": "test@example.com",
        "password": "correctpassword123"
    }

    response = client.post("/auth/login", json=login_data)
    return response.json()["access_token"]


