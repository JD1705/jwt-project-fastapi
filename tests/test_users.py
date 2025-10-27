import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from datetime import datetime, timezone

# tests for GET /users/me
def test_successful_response(mocker, client, mock_user, mock_verify_token, mock_token):
    
    mock_get_collection_dependencies = mocker.MagicMock()
    mock_get_collection_dependencies.find_one.return_value = mock_user

    mocker.patch("app.utils.dependencies.get_collection", return_value=mock_get_collection_dependencies)
    mock_dependency = mocker.patch("app.routes.users.get_current_user")
    mock_dependency.return_value = mock_user

    response = client.get("/users/me", headers={"authorization":f"bearer {mock_token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == mock_user["username"]
    assert data["email"] == mock_user["email"]
    assert data["id"] == mock_user["_id"]

def test_call_without_token(client):

    response = client.get("/users/me")

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"

def test_if_user_not_found(client, mock_token, mock_verify_token, mocker):

    mock_get_collection_dependencies = mocker.MagicMock()
    mock_get_collection_dependencies.find_one.return_value = None

    mocker.patch("app.utils.dependencies.get_collection", return_value=mock_get_collection_dependencies)

    response = client.get("/users/me", headers={"authorization":f"bearer {mock_token}"})

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User Not Found"

# tests for PUT /users/me
def test_if_update_username_correctly(client, mocker, mock_verify_token, mock_token, mock_user):
    
    mock_get_collection_dependencies = mocker.MagicMock()
    mock_get_collection_dependencies.find_one.return_value = mock_user
    
    mock_update_data = {
            "username":"updated_username"
            }

    mock_get_collection = mocker.MagicMock()
    mock_get_collection.update_one.return_value = None

    mocker.patch("app.routes.users.get_collection", return_value=mock_get_collection)
    mocker.patch("app.utils.dependencies.get_collection", return_value=mock_get_collection_dependencies)
    mock_dependency = mocker.patch("app.routes.users.get_current_user")
    mock_dependency.return_value = mock_user
 
    fixed_date = datetime(2025,1,1,12,0,0,tzinfo=timezone.utc)
    mock_user_updated = {
        "_id": "user123",
        "username":mock_update_data["username"],
        "email": "test@example.com",
        "hashed_password": "hashed_password_123",
        "created_at":fixed_date
            }
    
    mock_get_collection.find_one.return_value = mock_user_updated

    response = client.put("/users/me", json=mock_update_data, headers={"authorization":f"bearer {mock_token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == mock_update_data["username"]
    assert data["email"] == "test@example.com"
    mock_get_collection.update_one.assert_called_once_with({"_id":"user123"},{"$set": mock_update_data})

def test_if_update_email_correctly(client, mocker, mock_user, mock_verify_token, mock_token):

    mock_get_collection_dependencies = mocker.MagicMock()
    mock_get_collection_dependencies.find_one.return_value = mock_user
    
    mock_update_data = {
            "email":"test_example_updated@gmail.com"
            }

    mock_get_collection = mocker.MagicMock()
    mock_get_collection.update_one.return_value = None

    mocker.patch("app.routes.users.get_collection", return_value=mock_get_collection)
    mocker.patch("app.utils.dependencies.get_collection", return_value=mock_get_collection_dependencies)
    mock_dependency = mocker.patch("app.routes.users.get_current_user")
    mock_dependency.return_value = mock_user
 
    fixed_date = datetime(2025,1,1,12,0,0,tzinfo=timezone.utc)
    mock_user_updated = {
        "_id": "user123",
        "username":"test_user",
        "email": mock_update_data["email"],
        "hashed_password": "hashed_password_123",
        "created_at":fixed_date
            }
    
    mock_get_collection.find_one.side_effect = [None, mock_user_updated]

    response = client.put("/users/me", json=mock_update_data, headers={"authorization":f"bearer {mock_token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test_user"
    assert data["email"] == mock_update_data["email"]
    mock_get_collection.update_one.assert_called_once_with({"_id":"user123"},{"$set": mock_update_data})

def test_if_update_email_and_username_correctly(client, mocker, mock_user, mock_verify_token, mock_token):

    mock_get_collection_dependencies = mocker.MagicMock()
    mock_get_collection_dependencies.find_one.return_value = mock_user
    
    mock_update_data = {
            "username":"updated_username",
            "email":"test_example_updated@gmail.com"
            }

    mock_get_collection = mocker.MagicMock()
    mock_get_collection.update_one.return_value = None

    mocker.patch("app.routes.users.get_collection", return_value=mock_get_collection)
    mocker.patch("app.utils.dependencies.get_collection", return_value=mock_get_collection_dependencies)
    mock_dependency = mocker.patch("app.routes.users.get_current_user")
    mock_dependency.return_value = mock_user
 
    fixed_date = datetime(2025,1,1,12,0,0,tzinfo=timezone.utc)
    mock_user_updated = {
        "_id": "user123",
        "username":mock_update_data["username"],
        "email": mock_update_data["email"],
        "hashed_password": "hashed_password_123",
        "created_at":fixed_date
            }
    
    mock_get_collection.find_one.side_effect = [None, mock_user_updated]

    response = client.put("/users/me", json=mock_update_data, headers={"authorization":f"bearer {mock_token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == mock_update_data["username"]
    assert data["email"] == mock_update_data["email"]
    mock_get_collection.update_one.assert_called_once_with({"_id":"user123"},{"$set": mock_update_data})

def test_if_email_already_exist(client, mocker, mock_user, mock_verify_token, mock_token):

    mock_get_collection_dependencies = mocker.MagicMock()
    mock_get_collection_dependencies.find_one.return_value = mock_user
    
    mock_update_data = {
            "email":"existing@gmail.com"
            }

    mock_get_collection = mocker.MagicMock()
    mock_get_collection.update_one.return_value = None

    mocker.patch("app.routes.users.get_collection", return_value=mock_get_collection)
    mocker.patch("app.utils.dependencies.get_collection", return_value=mock_get_collection_dependencies)
    mock_dependency = mocker.patch("app.routes.users.get_current_user")
    mock_dependency.return_value = mock_user
 
    fixed_date = datetime(2025,1,1,12,0,0,tzinfo=timezone.utc)
    mock_user_updated = {
        "_id": "user123",
        "username":"test_user",
        "email": mock_update_data["email"],
        "hashed_password": "hashed_password_123",
        "created_at":fixed_date
            }
    
    mock_get_collection.find_one.return_value = mock_user_updated

    response = client.put("/users/me", json=mock_update_data, headers={"authorization":f"bearer {mock_token}"})

    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "Incorrect Credentials"
    mock_get_collection.update_one.assert_not_called()

def test_that_fields_are_not_empty(client, mocker, mock_user, mock_verify_token, mock_token):

    mock_get_collection_dependencies = mocker.MagicMock()
    mock_get_collection_dependencies.find_one.return_value = mock_user
    
    mock_update_data = {
            "username":None,
            "email":None
            }

    mock_get_collection = mocker.MagicMock()

    mocker.patch("app.routes.users.get_collection", return_value=mock_get_collection)
    mocker.patch("app.utils.dependencies.get_collection", return_value=mock_get_collection_dependencies)
    mock_dependency = mocker.patch("app.routes.users.get_current_user")
    mock_dependency.return_value = mock_user

    response = client.put("/users/me", json=mock_update_data, headers={"authorization":f"bearer {mock_token}"})

    assert response.status_code == 422
    mock_get_collection.update_one.assert_not_called()
    mock_get_collection.find_one.assert_not_called()

