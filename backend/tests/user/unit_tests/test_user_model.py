# this file contains unit tests for the user model.

import pytest
from backend.models.user.user_model import User


def test_user_valid_creation():
    """
    this test checks that we can create a valid merged user object.
    """
    u = User(
        id="1",
        username="anjana",
        email="anjana@gmail.com",
        password_hash="hashed_password"
    )

    assert u.id == "1"
    assert u.username == "anjana"
    assert u.email == "anjana@gmail.com"
    assert u.password_hash == "hashed_password"
    assert u.phone == ""
    assert u.address == ""
    assert u.location == ""
    assert u.postal_code == ""
    assert u.latitude is None
    assert u.longitude is None
    assert u.cart == []
    assert u.orders == []
    assert u.owned_restaurants_id == []


def test_user_valid_creation_with_all_fields():
    """
    this test checks that a user can be created
    when all fields are provided.
    """
    u = User(
        id="2",
        username="owner1",
        email="owner@gmail.com",
        password_hash="hashed_password",
        phone="1234567890",
        address="123 Main St",
        location="reykjavik",
        postal_code="V1V1V1",
        latitude=64.14,
        longitude=-21.94,
        cart=["item1"],
        orders=["order1"],
        owned_restaurants_id=["rest1", "rest2"]
    )

    assert u.phone == "1234567890"
    assert u.address == "123 Main St"
    assert u.location == "reykjavik"
    assert u.postal_code == "V1V1V1"
    assert u.latitude == 64.14
    assert u.longitude == -21.94
    assert u.cart == ["item1"]
    assert u.orders == ["order1"]
    assert u.owned_restaurants_id == ["rest1", "rest2"]


def test_user_invalid_id_empty():
    """
    this test checks that empty ids are rejected.
    """
    with pytest.raises(ValueError):
        User(id="", username="a", email="a@gmail.com", password_hash="hash")


def test_user_invalid_id_blank():
    """
    this test checks that blank ids are rejected.
    """
    with pytest.raises(ValueError):
        User(id="   ", username="a", email="a@gmail.com", password_hash="hash")


def test_user_invalid_id_wrong_type():
    """
    this test checks that id must be a string, not an int.
    """
    with pytest.raises(ValueError):
        User(id=1, username="a", email="a@gmail.com", password_hash="hash")


def test_user_invalid_username_empty():
    """
    this test checks that empty usernames are rejected.
    """
    with pytest.raises(ValueError):
        User(id="1", username="", email="a@gmail.com", password_hash="hash")


def test_user_invalid_username_blank():
    """
    this test checks that blank usernames are rejected.
    """
    with pytest.raises(ValueError):
        User(id="1", username="   ", email="a@gmail.com", password_hash="hash")


def test_user_invalid_username_wrong_type():
    """
    this test checks that username must be a string.
    """
    with pytest.raises(ValueError):
        User(id="1", username=123, email="a@gmail.com", password_hash="hash")


def test_user_invalid_password_hash_empty():
    """
    this test checks that empty password hashes are rejected.
    """
    with pytest.raises(ValueError):
        User(id="1", username="a", email="a@gmail.com", password_hash="")


def test_user_invalid_password_hash_blank():
    """
    this test checks that blank password hashes are rejected.
    """
    with pytest.raises(ValueError):
        User(id="1", username="a", email="a@gmail.com", password_hash="   ")


def test_user_invalid_password_hash_wrong_type():
    """
    this test checks that password_hash must be a string.
    """
    with pytest.raises(ValueError):
        User(id="1", username="a", email="a@gmail.com", password_hash=123)


def test_user_invalid_email_empty():
    """
    this test checks that empty emails are rejected.
    """
    with pytest.raises(ValueError):
        User(id="1", username="a", email="", password_hash="hash")


def test_user_invalid_email_blank():
    """
    this test checks that blank emails are rejected.
    """
    with pytest.raises(ValueError):
        User(id="1", username="a", email="   ", password_hash="hash")


def test_user_invalid_email_missing_at():
    """
    this test checks that email must contain @.
    """
    with pytest.raises(ValueError):
        User(id="1", username="a", email="invalidemail", password_hash="hash")


def test_user_invalid_email_missing_dot():
    """
    this test checks that the email domain must contain a dot.
    """
    with pytest.raises(ValueError):
        User(id="1", username="a", email="abc@gmail", password_hash="hash")


def test_user_invalid_email_wrong_type():
    """
    this test checks that email must be a string.
    """
    with pytest.raises(ValueError):
        User(id="1", username="a", email=123, password_hash="hash")


def test_user_invalid_phone_type():
    """
    this test checks that phone must be a string.
    """
    with pytest.raises(ValueError):
        User(id="1", username="a", email="a@gmail.com", password_hash="hash", phone=123)


def test_user_invalid_address_type():
    """
    this test checks that address must be a string.
    """
    with pytest.raises(ValueError):
        User(id="1", username="a", email="a@gmail.com", password_hash="hash", address=[])


def test_user_invalid_location_type():
    """
    this test checks that location must be a string.
    """
    with pytest.raises(ValueError):
        User(id="1", username="a", email="a@gmail.com", password_hash="hash", location={})


def test_user_invalid_postal_code_type():
    """
    this test checks that postal_code must be a string.
    """
    with pytest.raises(ValueError):
        User(id="1", username="a", email="a@gmail.com", password_hash="hash", postal_code=999)


def test_user_invalid_latitude_type():
    """
    this test checks that latitude must be a number or None.
    """
    with pytest.raises(ValueError):
        User(id="1", username="a", email="a@gmail.com", password_hash="hash", latitude="north")


def test_user_invalid_longitude_type():
    """
    this test checks that longitude must be a number or None.
    """
    with pytest.raises(ValueError):
        User(id="1", username="a", email="a@gmail.com", password_hash="hash", longitude="west")


def test_user_valid_numeric_coordinates():
    """
    this test checks that latitude and longitude work
    when valid numbers are given.
    """
    u = User(
        id="3",
        username="mapuser",
        email="map@gmail.com",
        password_hash="hashed_password",
        latitude=64.14,
        longitude=-21.94
    )

    assert u.latitude == 64.14
    assert u.longitude == -21.94


def test_user_invalid_cart_type():
    """
    this test checks that cart must be a list.
    """
    with pytest.raises(ValueError):
        User(id="1", username="a", email="a@gmail.com", password_hash="hash", cart="notalist")


def test_user_invalid_orders_type():
    """
    this test checks that orders must be a list.
    """
    with pytest.raises(ValueError):
        User(id="1", username="a", email="a@gmail.com", password_hash="hash", orders="notalist")


def test_user_invalid_owned_restaurants_id_type():
    """
    this test checks that owned_restaurants_id must be a list.
    """
    with pytest.raises(ValueError):
        User(
            id="1",
            username="a",
            email="a@gmail.com",
            password_hash="hash",
            owned_restaurants_id="bakeryone"
        )


def test_user_valid_empty_lists():
    """
    this test checks that empty lists are valid
    for cart, orders, and owned_restaurants_id.
    """
    u = User(
        id="4",
        username="emptylists",
        email="empty@gmail.com",
        password_hash="hashed_password",
        cart=[],
        orders=[],
        owned_restaurants_id=[]
    )

    assert u.cart == []
    assert u.orders == []
    assert u.owned_restaurants_id == []


def test_user_with_owned_restaurants():
    """
    this test checks that restaurant ownership can be stored
    using owned_restaurants_id in the merged user model.
    """
    u = User(
        id="5",
        username="owner1",
        email="owner@gmail.com",
        password_hash="hashed_password",
        owned_restaurants_id=["rest1", "rest2"]
    )

    assert u.owned_restaurants_id == ["rest1", "rest2"]