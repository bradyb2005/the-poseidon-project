import json
import pytest
from backend.repositories import user_repository

@pytest.fixture
def repo(tmp_path):
    user_repository.DATA_FILE = tmp_path / "users.json"
    return user_repository.UserRepository()

def test_create_assigns_id_and_saves(repo):
    user_data = {
        "username": "anjana",
        "email": "anjanaoned@gmail.com",
        "password": "SuperSecret123!"
    }
    created_user = repo.create(user_data)

    assert created_user["id"] == 1
    assert created_user["username"] == "anjana"
    assert "password_hash" in created_user
    assert "password" not in created_user

def test_create_stores_hash_not_raw(repo):
    raw_pw = "SuperSecret123!"
    repo.create({
        "username": "anjana",
        "email": "anjanaoned@gmail.com",
        "password": raw_pw
    })

    # read the actual saved JSON file
    with open(user_repository.DATA_FILE, "r", encoding="utf-8") as f:
        saved = json.load(f)

    assert len(saved) == 1
    assert "password_hash" in saved[0]
    assert saved[0]["password_hash"] != raw_pw
    assert "password" not in saved[0]

def test_find_by_username(repo):
    repo.create({
        "username": "anjana",
        "email": "anjanaoned@gmail.com",
        "password": "pw123!!"
    })
    found_user = repo.find_by_username("anjana")
    assert found_user["username"] == "anjana"
    assert found_user["id"] == 1

def test_find_by_id(repo):
    repo.create({
        "username": "anjana",
        "email": "anjanaoned@gmail.com",
        "password": "pw123!!"
    })
    found_user = repo.find_by_id(1)
    assert found_user["username"] == "anjana"
    assert found_user["id"] == 1

def test_find_missing_returns_none(repo):
    assert repo.find_by_username("nope") is None
    assert repo.find_by_id(999) is None



def test_update_username_changes_only_username(repo):
        created = repo.create({
            "username": "anjana",
            "email": "anjana.ubco@gmail.com",
            "password": "SecurePw123!!"
        })

        updated = repo.update_username(created["id"], "anjana_r")

        assert updated["username"] == "anjana_r"
        assert updated["email"] == "anjana.ubco@gmail.com"
        assert updated["id"] == created["id"]



def test_update_email_changes_only_email(repo):
    created = repo.create({
        "username": "anjana",
        "email": "oldanjana@gmail.com",
        "password": "SecurePw123!!"
    })

    updated = repo.update_email(created["id"], "newanjana@gmail.com")

    assert updated["email"] == "newanjana@gmail.com"
    assert updated["username"] == "anjana"
    assert updated["id"] == created["id"]


def test_update_password_hashes_and_never_stores_raw(repo):
    created = repo.create({
        "username": "anjana",
        "email": "anjana.ubco@gmail.com",
        "password": "InitialPw123!!"
    })

    new_pw = "NewSecurePw456!!"
    updated = repo.update_password(created["id"], new_pw)

    # ensure password_hash exists
    assert "password_hash" in updated

    # ensure raw password not stored
    assert updated["password_hash"] != new_pw
    assert "password" not in updated

    # double-check persisted file
    import json
    from backend.repositories import user_repository

    with open(user_repository.DATA_FILE, "r", encoding="utf-8") as f:
        saved = json.load(f)

    assert saved[0]["password_hash"] != new_pw
    assert "password" not in saved[0]


def test_update_returns_none_if_user_not_found(repo):
    assert repo.update_username(999, "ghost_user") is None
    assert repo.update_email(999, "ghost@gmail.com") is None
    assert repo.update_password(999, "Nope123!!") is None