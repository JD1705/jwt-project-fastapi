import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

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

