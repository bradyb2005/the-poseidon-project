# backend/tests/repositories/test_user_repository.py
import json

from backend.repositories.user_repository import UserRepository


def test_load_all_returns_empty_list_if_file_does_not_exist(monkeypatch, tmp_path):
    """load_all should return an empty list if the file does not exist."""
    fake_file = tmp_path / "users.json"
    monkeypatch.setattr("backend.repositories.user_repository.DATA_FILE", str(fake_file))

    repo = UserRepository()
    users = repo.load_all()

    assert users == []


def test_save_all_writes_users_to_file(monkeypatch, tmp_path):
    """save_all should write users to the JSON file."""
    fake_file = tmp_path / "users.json"
    monkeypatch.setattr("backend.repositories.user_repository.DATA_FILE", str(fake_file))

    repo = UserRepository()
    users = [
        {
            "id": "1",
            "username": "anjana",
            "email": "anjana@gmail.com",
            "password_hash": "hashed_password"
        }
    ]

    repo.save_all(users)

    with open(fake_file, "r", encoding="utf-8") as f:
        saved_data = json.load(f)

    assert saved_data == users


def test_load_all_returns_users_from_file(monkeypatch, tmp_path):
    """load_all should return the user data stored in the file."""
    fake_file = tmp_path / "users.json"
    monkeypatch.setattr("backend.repositories.user_repository.DATA_FILE", str(fake_file))

    users = [
        {
            "id": "1",
            "username": "anjana",
            "email": "anjana@gmail.com",
            "password_hash": "hashed_password"
        },
        {
            "id": "2",
            "username": "john",
            "email": "john@gmail.com",
            "password_hash": "another_hash"
        }
    ]

    with open(fake_file, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

    repo = UserRepository()
    loaded_users = repo.load_all()

    assert loaded_users == users


def test_save_all_overwrites_old_data(monkeypatch, tmp_path):
    """save_all should overwrite existing file contents."""
    fake_file = tmp_path / "users.json"
    monkeypatch.setattr("backend.repositories.user_repository.DATA_FILE", str(fake_file))

    old_users = [
        {
            "id": "1",
            "username": "olduser",
            "email": "old@gmail.com",
            "password_hash": "old_hash"
        }
    ]

    new_users = [
        {
            "id": "2",
            "username": "newuser",
            "email": "new@gmail.com",
            "password_hash": "new_hash"
        }
    ]

    with open(fake_file, "w", encoding="utf-8") as f:
        json.dump(old_users, f, indent=2)

    repo = UserRepository()
    repo.save_all(new_users)

    with open(fake_file, "r", encoding="utf-8") as f:
        saved_data = json.load(f)

    assert saved_data == new_users


def test_save_all_and_load_all_work_together(monkeypatch, tmp_path):
    """save_all and load_all should preserve the same data."""
    fake_file = tmp_path / "users.json"
    monkeypatch.setattr("backend.repositories.user_repository.DATA_FILE", str(fake_file))

    users = [
        {
            "id": "1",
            "username": "anjana",
            "email": "anjana@gmail.com",
            "password_hash": "hashed_password",
            "owned_restaurants_id": ["rest1"]
        }
    ]

    repo = UserRepository()
    repo.save_all(users)
    loaded_users = repo.load_all()

    assert loaded_users == users

def test_load_all_returns_empty_list_if_file_is_empty(monkeypatch, tmp_path):
    """load_all should return an empty list if the file is empty."""
    fake_file = tmp_path / "users.json"
    fake_file.write_text("", encoding="utf-8")
    monkeypatch.setattr("backend.repositories.user_repository.DATA_FILE", str(fake_file))

    repo = UserRepository()

    assert repo.load_all() == []

def test_find_by_id_success(monkeypatch):
    """find_by_id should return the correct user dictionary when the ID exists."""
    repo = UserRepository()

    monkeypatch.setattr(repo, "load_all", lambda: [
        {"id": "1", "username": "anjana"},
        {"id": "2", "username": "brady"}
    ])

    result = repo.find_by_id("1")
    
    assert result == {"id": "1", "username": "anjana"}


def test_find_by_id_not_found(monkeypatch):
    """find_by_id should return None when the ID does not exist."""
    repo = UserRepository()

    monkeypatch.setattr(repo, "load_all", lambda: [
        {"id": "1", "username": "anjana"}
    ])

    result = repo.find_by_id("99")
    
    assert result is None