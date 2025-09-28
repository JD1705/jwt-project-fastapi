import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app.main import app
from fastapi.testclient import TestClient
from bson import ObjectId
from datetime import datetime, timezone

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

    client = TestClient(app)
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

    client = TestClient(app)

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
