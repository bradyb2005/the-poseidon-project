# this file contains unit tests for the user model.

import pytest

from backend.models.user.user_model import User
from backend.models.user.customer import Customer
from backend.models.user.admin import Admin
from backend.models.user.restaurant_owner import RestaurantOwner


def test_user_valid_creation():
    """
    This test checks that we can create a valid user object without errors.
    this also checks that the password is hashed and not placed in plain text.   
    """
    u = User(id=1, username="anjana", password_hash=User.hash_password("secretPWhehe"))

    assert u.id == 1
    assert u.username == "anjana"

    # password_hash should be a string, should not equal the raw password
    assert isinstance(u.password_hash, str)
    assert u.password_hash != "secretPWhehe"


def test_user_invalid_id():
    """
    This test checks that negative IDs are rejected.
    id must be a non-negative integer.
    """
    with pytest.raises(ValueError):
        User(id=-1, username="a", password_hash="hash")


def test_user_invalid_username():
    """
    This test checks that empty/blank usernames are rejected.
    username must be a non-empty string.
    """
    with pytest.raises(ValueError):
        User(id=1, username="   ", password_hash="hash")


def test_user_invalid_password_hash():
    """
    This test checks that empty/blank password_hash is rejected.
    password_hash must be a non-empty string.
    """
    with pytest.raises(ValueError):
        User(id=1, username="a", password_hash="   ")


def test_hash_password_rejects_empty():
    with pytest.raises(ValueError):
        User.hash_password("")


def test_check_password_true_and_false():
    raw_pw = "secretPWhehe"
    u = User(id=1, username="anjana", password_hash=User.hash_password(raw_pw))

    assert u.check_password("secretPWhehe") is True
    assert u.check_password("wrong") is False


def test_update_password_changes_hash_and_validates():
    """This test checks that update_password() changes the stored password_hash,
    and that the new password works while the old one stops working.
    """
    u = User(id=1, username="anjana", password_hash=User.hash_password("oldPW"))
    old_hash = u.password_hash

    u.update_password("newPW")

    # hash should change after updating password
    assert u.password_hash != old_hash

    # new password should work, old should not
    assert u.check_password("newPW") is True
    assert u.check_password("oldPW") is False


def test_to_dict_includes_user_type():
    c = Customer(id=2, username="cust", password_hash=User.hash_password("pw"))
    d = c.to_dict()

    assert "user_type" in d
    assert d["user_type"] == "Customer"


@pytest.mark.parametrize("cls", [User, Customer, Admin, RestaurantOwner])
def test_from_dict_creates_correct_subclass(cls):
    """This test checks the inheritance + serialization workflow, 
    helps reduce repitative tests for each subclass. 
      1) create a user object (User or subclass)
      2) convert it to dict using to_dict()
      3) load it back using User.from_dict()
      4) confirm we got the SAME TYPE back (Customer stays Customer, etc.)
    """
    u1 = cls(id=7, username="x", password_hash=User.hash_password("pw"))
    data = u1.to_dict()

    u2 = User.from_dict(data)

    assert isinstance(u2, cls)
    assert u2.id == u1.id
    assert u2.username == u1.username
    assert u2.password_hash == u1.password_hash
