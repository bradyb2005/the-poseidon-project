# backend/tests/user/integration_tests/test_user_routes.py

from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from backend.main import app

client = TestClient(app)


@patch("backend.routes.user_routes.get_service")
def test_register_user_success(mock_get_service):
    mock_service = MagicMock()
    mock_get_service.return_value = mock_service
    mock_service.create_user.return_value = {
        "id": "1",
        "username": "anjana",
        "email": "anjana@gmail.com",
        "password_hash": "hashed_pw",
    }

    response = client.post(
        "/users/register",
        json={"username": "anjana", "email": "anjana@gmail.com", "password": "password123"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "user registered successfully"
    assert response.json()["user"]["username"] == "anjana"


@patch("backend.routes.user_routes.get_service")
def test_register_user_duplicate_username(mock_get_service):
    mock_service = MagicMock()
    mock_get_service.return_value = mock_service
    mock_service.create_user.side_effect = ValueError("username already exists")

    response = client.post(
        "/users/register",
        json={"username": "anjana", "email": "anjana@gmail.com", "password": "password123"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "username already exists"


@patch("backend.routes.user_routes.get_service")
def test_login_user_success(mock_get_service):
    mock_service = MagicMock()
    mock_get_service.return_value = mock_service
    mock_service.authenticate_user.return_value = {
        "id": "1",
        "username": "anjana",
        "email": "anjana@gmail.com",
        "password_hash": "hashed_pw",
    }

    response = client.post(
        "/users/login",
        json={"username": "anjana", "password": "password123"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "login successful"
    assert response.json()["user"]["username"] == "anjana"


@patch("backend.routes.user_routes.get_service")
def test_login_user_invalid_credentials(mock_get_service):
    mock_service = MagicMock()
    mock_get_service.return_value = mock_service
    mock_service.authenticate_user.side_effect = ValueError("invalid credentials")

    response = client.post(
        "/users/login",
        json={"username": "anjana", "password": "wrongpassword"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "invalid credentials"

    