from unittest.mock import MagicMock
import pytest

from backend.services.feat1.user_service import UserService


def test_create_user_success():
    repo = MagicMock()
    repo.load_all.return_value = []

    service = UserService(repo)
    created_user = service.create_user("anjana", "anjana@gmail.com", "password123")

    assert created_user["username"] == "anjana"
    assert created_user["email"] == "anjana@gmail.com"
    assert created_user["id"] == "1"
    assert created_user["password_hash"] != "password123"
    repo.save_all.assert_called_once()


def test_create_user_raises_error_for_duplicate_username():
    repo = MagicMock()
    repo.load_all.return_value = [
        {"id": "1", "username": "anjana", "email": "old@gmail.com", "password_hash": "hash"}
    ]

    service = UserService(repo)

    with pytest.raises(ValueError, match="username already exists"):
        service.create_user("anjana", "new@gmail.com", "password123")


def test_update_username_success():
    repo = MagicMock()
    repo.load_all.return_value = [
        {"id": "1", "username": "oldname", "email": "a@test.com", "password_hash": "hash"}
    ]

    service = UserService(repo)
    updated_user = service.update_username("1", "newname")

    assert updated_user["username"] == "newname"
    repo.save_all.assert_called_once()


def test_update_username_raises_error_for_duplicate_username():
    repo = MagicMock()
    repo.load_all.return_value = [
        {"id": "1", "username": "oldname", "email": "a@test.com", "password_hash": "hash"},
        {"id": "2", "username": "takenname", "email": "b@test.com", "password_hash": "hash"}
    ]

    service = UserService(repo)

    with pytest.raises(ValueError, match="username already exists"):
        service.update_username("1", "takenname")


def test_update_email_success():
    repo = MagicMock()
    repo.load_all.return_value = [
        {"id": "1", "username": "anjana", "email": "old@test.com", "password_hash": "hash"}
    ]

    service = UserService(repo)
    updated_user = service.update_email("1", "new@test.com")

    assert updated_user["email"] == "new@test.com"
    repo.save_all.assert_called_once()


def test_update_password_success():
    repo = MagicMock()
    service = UserService(repo)

    current_hash = service.hash_password("oldpassword")
    repo.load_all.return_value = [
        {"id": "1", "username": "anjana", "email": "a@test.com", "password_hash": current_hash}
    ]

    updated_user = service.update_password("1", "oldpassword", "newpassword123")

    assert updated_user["password_hash"] != current_hash
    assert service.verify_password("newpassword123", updated_user["password_hash"])
    repo.save_all.assert_called_once()


def test_update_password_raises_error_for_incorrect_current_password():
    repo = MagicMock()
    service = UserService(repo)

    current_hash = service.hash_password("oldpassword")
    repo.load_all.return_value = [
        {"id": "1", "username": "anjana", "email": "a@test.com", "password_hash": current_hash}
    ]

    with pytest.raises(ValueError, match="current password is incorrect"):
        service.update_password("1", "wrongpassword", "newpassword123")


def test_update_username_raises_error_when_user_not_found():
    repo = MagicMock()
    repo.load_all.return_value = []

    service = UserService(repo)

    with pytest.raises(ValueError, match="user not found"):
        service.update_username("1", "newname")


def test_update_email_raises_error_when_user_not_found():
    repo = MagicMock()
    repo.load_all.return_value = []

    service = UserService(repo)

    with pytest.raises(ValueError, match="user not found"):
        service.update_email("1", "new@test.com")


def test_update_password_raises_error_when_user_not_found():
    repo = MagicMock()
    repo.load_all.return_value = []

    service = UserService(repo)

    with pytest.raises(ValueError, match="user not found"):
        service.update_password("1", "oldpassword", "newpassword123")


def test_forgot_password_updates_password_hash_by_email():
    repo = MagicMock()
    service = UserService(repo)

    old_hash = service.hash_password("oldpassword")
    repo.load_all.return_value = [
        {
            "id": "1",
            "username": "anjana",
            "email": "anjana@gmail.com",
            "password_hash": old_hash
        }
    ]

    updated_user = service.forgot_password("anjana@gmail.com", "newpassword123")

    assert updated_user["password_hash"] != old_hash
    assert service.verify_password("newpassword123", updated_user["password_hash"])
    repo.save_all.assert_called_once()


def test_forgot_password_raises_error_when_email_not_found():
    repo = MagicMock()
    repo.load_all.return_value = []

    service = UserService(repo)

    with pytest.raises(ValueError, match="user not found"):
        service.forgot_password("anjana@gmail.com", "newpassword123")
