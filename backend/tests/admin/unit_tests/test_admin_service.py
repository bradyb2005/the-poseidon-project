# backend/tests/admin/unit_tests/test_admin_service.py

import pytest
from unittest.mock import MagicMock
from backend.services.admin_service import AdminService


@pytest.fixture
def users():
    return [
        {"id": "1", "username": "alice", "email": "alice@test.com",
         "role": "customer", "is_suspended": False},
        {"id": "2", "username": "bob", "email": "bob@test.com",
         "role": "owner", "is_suspended": True},
        {"id": "3", "username": "admin1", "email": "admin@test.com",
         "role": "admin", "is_suspended": False},
    ]


@pytest.fixture
def service(users):
    user_repo = MagicMock()
    notification_repo = MagicMock()
    user_repo.load_all.return_value = users
    notification_repo.load_all.return_value = []
    return AdminService(user_repo, notification_repo)


def test_get_all_users_no_filter(service):
    result = service.get_all_users()
    assert result["total"] == 3


def test_get_all_users_filter_by_role(service):
    result = service.get_all_users(role="customer")
    assert result["total"] == 1
    assert result["users"][0]["username"] == "alice"


def test_get_all_users_filter_suspended(service):
    result = service.get_all_users(is_suspended=True)
    assert result["total"] == 1
    assert result["users"][0]["username"] == "bob"


def test_get_all_users_search(service):
    result = service.get_all_users(search="alice")
    assert result["total"] == 1


def test_get_all_users_pagination(service):
    result = service.get_all_users(page=1, page_size=2)
    assert len(result["users"]) == 2
    assert result["total_pages"] == 2


def test_get_user_by_id_found(service):
    result = service.get_user_by_id("1")
    assert result["username"] == "alice"


def test_get_user_by_id_not_found(service):
    with pytest.raises(ValueError, match="not found"):
        service.get_user_by_id("999")


def test_suspend_user(service):
    result = service.suspend_user("1")
    assert result["is_suspended"] is True


def test_suspend_admin_raises(service):
    with pytest.raises(ValueError, match="Cannot suspend an admin"):
        service.suspend_user("3")


def test_unsuspend_user(service):
    result = service.unsuspend_user("2")
    assert result["is_suspended"] is False


def test_update_user_allowed_fields(service):
    result = service.update_user("1", {"username": "alice_new"})
    assert result["username"] == "alice_new"


def test_update_user_blocked_field_ignored(service):
    # password_hash is not in allowed_fields, should be silently ignored
    result = service.update_user("1", {"password_hash": "hacked"})
    assert result.get("password_hash") != "hacked"


def test_delete_user(service):
    result = service.delete_user("1")
    assert result["deleted"] is True