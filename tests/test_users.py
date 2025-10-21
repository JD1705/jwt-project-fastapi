import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app.main import app
from fastapi.testclient import TestClient
from bson import ObjectId
from datetime import datetime, timezone

client = TestClient(app)

# tests for GET /users/me
def test_successful_response(mocker):
    
    mock_payload = {
            "sub":"507f1f77bcf86cd799439011"
            }
    mock_verify_token = mocker.MagicMock()
    mock_verify_token.return_value = mock_payload

    mock_get_collection_dependencies = mocker.MagicMock()

    fixed_date = datetime(2025,1,1,12,0,0,tzinfo=timezone.utc)

    mock_get_collection = mocker.MagicMock()
    mock_user = {
        "_id": "user123",
        "username":"test_user",
        "email": "test@example.com",
        "hashed_password": "hashed_password_123",
        "created_at":fixed_date
    }
    mock_get_collection.find_one.return_value = mock_user
    mock_get_collection_dependencies.find_one.return_value = mock_user

    mock_verify_password = mocker.MagicMock(return_value=True)
    
    mock_create_access_token = mocker.MagicMock()
    mock_token = "falsetoken"
    mock_create_access_token.return_value = mock_token
    
    mocker.patch("app.utils.dependencies.get_collection", return_value=mock_get_collection_dependencies)
    mocker.patch("app.utils.dependencies.verify_token", mock_verify_token)
    mocker.patch("app.routes.auth.get_collection", return_value=mock_get_collection)
    mocker.patch("app.routes.auth.verify_password", mock_verify_password)
    mocker.patch("app.routes.auth.create_access_token", mock_create_access_token)
    
    login_data = {
        "email": "test@example.com",
        "password": "correctpassword123"
    }

    response_login = client.post("/auth/login", json=login_data)
    token = response_login.json()["access_token"]

    mock_dependency = mocker.patch("app.routes.users.get_current_user")
    mock_dependency.return_value = mock_user
    response = client.get("/users/me", headers={"authorization":f"bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == mock_user["username"]
    assert data["email"] == mock_user["email"]
    assert data["id"] == mock_user["_id"]

