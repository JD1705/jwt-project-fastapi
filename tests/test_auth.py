import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app.main import app
from fastapi.testclient import TestClient
from bson import ObjectId
from datetime import datetime, timezone

client = TestClient(app)

def test_successful_registration(mocker):

    mock_get_collection = mocker.patch("app.routes.auth.get_collection")
    mock_collection = mocker.MagicMock()
    mock_get_collection.return_value = mock_collection

    mock_collection.find_one.return_value = None

    test_id = ObjectId("507f1f77bcf86cd799439011")
    mock_object_id = mocker.patch("app.routes.auth.ObjectId")
    mock_object_id.return_value = test_id

    fixed_date = datetime(2025,1,1,12,0,0,tzinfo=timezone.utc)
    mock_datetime = mocker.patch("app.routes.auth.datetime")
    mock_datetime.now.return_value = fixed_date
    mock_datetime.timezone.utc = timezone.utc

    mock_hash = mocker.patch("app.routes.auth.hash_password")
    mock_hash.return_value = "hashed_password_123"

    response = client.post("/auth/register", json={
        "email":"testemail@example.com",
        "username":"test_user",
        "password":"12345",
        "confirm_password":"12345"
        })


    assert response.status_code == 201

    data = response.json()
    assert data["id"] == "507f1f77bcf86cd799439011"
    assert data["email"] == "testemail@example.com"
    assert data["username"] == "test_user"

    mock_collection.find_one.assert_called_once_with({"email":"testemail@example.com"})
    mock_hash.assert_called_once_with("12345")

def test_if_user_already_exists(mocker):

    mock_get_collection = mocker.MagicMock()
    mock_find_one = mocker.MagicMock(return_value={"_id":"existing_id","email":"testemail@example.com"})

    mock_get_collection.find_one = mock_find_one

    mocker.patch("app.routes.auth.get_collection", return_value=mock_get_collection)

    user_data = {
        "email":"testemail@example.com",
        "username":"test_user",
        "password":"12345",
        "confirm_password":"12345"
        }

    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 409
    assert response.json()["detail"] == "User already exist"

    assert not mock_get_collection.insert_one.called

# Login tests
def test_login_success(mocker):
    
    mock_get_collection = mocker.MagicMock()
    mock_user = {
        "_id": "user123",
        "email": "test@example.com",
        "hashed_password": "hashed_password_123"
    }
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

    assert response.status_code == 200
    assert response.json()["access_token"] == mock_token
    assert response.json()["token_type"] == "bearer"

    mock_get_collection.find_one.assert_called_once_with({"email":"test@example.com"})
    mock_create_access_token.assert_called_once_with({"sub":mock_user["_id"], "email":mock_user["email"]})
    mock_verify_password.assert_called_once_with("correctpassword123", "hashed_password_123")

def test_login_user_not_found(mocker):
    
    mock_get_collection = mocker.MagicMock()
    mock_get_collection.find_one.return_value = None

    mocker.patch("app.routes.auth.get_collection", return_value=mock_get_collection)

    login_data = {
        "email": "nonexistent@example.com",
        "password": "somepassword123"
    }

    response = client.post("/auth/login", json=login_data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect Credentials"

    mock_get_collection.find_one.assert_called_once_with({"email":"nonexistent@example.com"})

def test_login_with_wrong_password(mocker):

    mock_get_collection = mocker.MagicMock()
    user_data = {
        "_id": "user123", 
        "email": "test@example.com",
        "hashed_password": "hashed_password_123"
    }
    
    mock_get_collection.find_one.return_value = user_data

    mock_verify_password = mocker.MagicMock(return_value=False)

    mocker.patch("app.routes.auth.get_collection", return_value=mock_get_collection)
    mocker.patch("app.routes.auth.verify_password", mock_verify_password)

    login_data = {
            "email":"test@example.com",
            "password":"wrongpassword"
            }

    response = client.post("/auth/login", json=login_data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect Credentials"

    mock_verify_password.assert_called_once_with("wrongpassword", "hashed_password_123")
