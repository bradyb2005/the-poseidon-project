import os
import sys
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.models.user.user_model import User
from backend.models.user.admin_model import Admin, ReviewModerationAction


def test_admin_valid_creation():
    # Use dummy hash to avoid bcrypt cost here
    a = Admin(id=1, username="admin1", password_hash="dummy_hash")
    assert a.id == 1
    assert a.username == "admin1"
    assert isinstance(a, User)


def test_admin_modify_credentials_updates_username():
    admin = Admin(id=1, username="admin", password_hash="dummy_hash")
    user = User(id=2, username="oldname", password_hash="oldhash")

    admin.modify_credentials(user, new_username="newname")

    assert user.username == "newname"
    assert user.password_hash == "oldhash"  # unchanged


def test_admin_modify_credentials_rejects_blank_username():
    admin = Admin(id=1, username="admin", password_hash="dummy_hash")
    user = User(id=2, username="oldname", password_hash="oldhash")

    with pytest.raises(ValueError):
        admin.modify_credentials(user, new_username="   ")


def test_admin_modify_credentials_updates_password_hash_fast(monkeypatch):
    # monkeypatch hashing so we don't run bcrypt in unit test
    monkeypatch.setattr(User, "hash_password", staticmethod(lambda pw: f"hashed:{pw}"))

    admin = Admin(id=1, username="admin", password_hash="dummy_hash")
    user = User(id=2, username="u", password_hash="oldhash")

    admin.modify_credentials(user, new_password="pw123")

    assert user.password_hash == "hashed:pw123"


def test_admin_moderate_review_uses_enum_and_sets_action():
    class DummyReview:
        pass

    admin = Admin(id=1, username="admin", password_hash="dummy_hash")
    r = DummyReview()

    admin.moderate_review(r, ReviewModerationAction.DELETE)

    assert getattr(r, "moderation_action") == "delete"