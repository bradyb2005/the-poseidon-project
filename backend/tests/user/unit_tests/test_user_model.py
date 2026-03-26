# this file contains unit tests for the user model.

import pytest

# Import requirements.txt before testing
# pip install -r requirements.txt
from backend.models.user.user_model import User

def test_user_valid_creation():
    """
    This test checks that we can create a valid user object without errors.
    this also checks that the password is hashed and not placed in plain text.
    """
    u = User(
        id=1,
        username="anjana",
        email="anjana@gmail.com",
        password_hash=User.hash_password("secretPWhehe")
    )

    assert u.id == 1
    assert u.username == "anjana"
    assert u.email == "anjana@gmail.com"

    # password_hash should be a string, should not equal the raw password
    assert isinstance(u.password_hash, str)
    assert u.password_hash != "secretPWhehe"


def test_user_invalid_id():
    """
    This test checks that negative IDs are rejected.
    id must be a non-negative integer.
    """
    with pytest.raises(ValueError):
        User(id=-1, username="a", email="a@gmail.com", password_hash="hash")


def test_user_invalid_username():
    """
    This test checks that empty/blank usernames are rejected.
    username must be a non-empty string.
    """
    with pytest.raises(ValueError):
        User(id=1, username="   ", email="a@gmail.com", password_hash="hash")


def test_user_invalid_password_hash():
    """
    This test checks that empty/blank password_hash is rejected.
    password_hash must be a non-empty string.
    """
    with pytest.raises(ValueError):
        User(id=1, username="a", email="a@gmail.com", password_hash="   ")


def test_user_invalid_email_empty():
    with pytest.raises(ValueError):
        User(id=1, username="a", email="   ", password_hash="hash")


def test_user_invalid_email_format():
    with pytest.raises(ValueError):
        User(id=1, username="a", email="invalidemail", password_hash="hash")


def test_hash_password_rejects_empty():
    with pytest.raises(ValueError):
        User.hash_password("")


def test_check_password_true_and_false():
    raw_pw = "secretPWhehe"
    u = User(
        id=1,
        username="anjana",
        email="anjana@gmail.com",
        password_hash=User.hash_password(raw_pw)
    )

    assert u.check_password("secretPWhehe") is True
    assert u.check_password("wrong") is False


def test_update_password_changes_hash_and_validates():
    """
    This test checks that update_password() change
    the stored password_hash,
    and that the new password works while the old one stops working.
    """
    u = User(
        id=1,
        username="anjana",
        email="anjana@gmail.com",
        password_hash=User.hash_password("oldPW")
    )
    old_hash = u.password_hash

    u.update_password("newPW")

    # hash should change after updating password
    assert u.password_hash != old_hash

    # new password should work, old should not
    assert u.check_password("newPW") is True
    assert u.check_password("oldPW") is False
