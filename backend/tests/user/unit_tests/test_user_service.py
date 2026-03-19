import pytest
from unittest.mock import MagicMock

from backend.services.user_service import UserService
from backend.models.user.user_model import User


@pytest.fixture
def user_service():
    service = UserService()
    service.repo = MagicMock()
    return service


def test_register_success(user_service):
    username = "anjana"
    password = "Password1!"
    email    = "anjana@email.com"

    user_service.repo.find_by_username.return_value = None
    user_service.repo.create.return_value = {
        "id": 1,
        "username": username,
        "email": email,
        "password_hash": User.hash_password(password),
        "user_type": "User",
    }

    result = user_service.register(username, email, password)

    user_service.repo.find_by_username.assert_called_once_with(username)
    user_service.repo.create.assert_called_once()

    created_data = user_service.repo.create.call_args[0][0]

    assert result["id"] == 1
    assert result["username"] == username
    assert result["email"] == email
    assert created_data["password_hash"] != password
    assert User.verify_password(password, created_data["password_hash"])


def test_register_raises_error_if_username_exists(user_service):
    user_service.repo.find_by_username.return_value = {
        "id": 1,
        "username": "anjana",
        "email": "anjana@email.com",
        "password_hash": "hashed_pw",
        "user_type": "User",
    }

    with pytest.raises(ValueError, match="Username already exists"):
        user_service.register("anjana", "anjana@email.com", "Password1!")

    user_service.repo.create.assert_not_called()


def test_login_returns_true_for_valid_credentials(user_service):
    username = "anjana"
    password = "Password1!"
    hashed_password = User.hash_password(password)

    user_service.repo.find_by_username.return_value = {
        "id": 1,
        "username": username,
        "email": "anjana@email.com",
        "password_hash": hashed_password,
        "user_type": "User",
    }

    result = user_service.login(username, password)

    assert result is True
    user_service.repo.find_by_username.assert_called_once_with(username)


def test_login_returns_false_when_user_not_found(user_service):
    user_service.repo.find_by_username.return_value = None

    result = user_service.login("ghost", "Password1!")

    assert result is False


def test_login_returns_false_for_wrong_password(user_service):
    username = "anjana"
    real_password = "Password1!"
    wrong_password = "WrongPass1!"
    hashed_password = User.hash_password(real_password)

    user_service.repo.find_by_username.return_value = {
        "id": 1,
        "username": username,
        "email": "anjana@email.com",
        "password_hash": hashed_password,
        "user_type": "User",
    }

    result = user_service.login(username, wrong_password)

    assert result is False
