import pytest

from backend.schemas.user_schema import User


def test_user_valid_creation():
    """Create a valid user with default values."""
    user = User(
        id="1",
        username="anjana",
        email="anjana@gmail.com",
        password_hash="hashed_password",
    )

    assert user.id == "1"
    assert user.username == "anjana"
    assert user.email == "anjana@gmail.com"
    assert user.password_hash == "hashed_password"
    assert user.phone == ""
    assert user.address == ""
    assert user.location == ""
    assert user.postal_code == ""
    assert user.latitude is None
    assert user.longitude is None
    
    # Assert against the newly generated Cart object instead of a list!
    assert user.cart.customer_id == "1"
    assert user.cart.items == []
    
    assert user.orders == []
    assert user.owned_restaurants_id == []


def test_user_valid_creation_with_all_fields():
    """Create a valid user when all fields are provided."""
    user = User(
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
        # 'cart' is removed from here since the model auto-generates it now
        orders=["order1"],
        owned_restaurants_id=["rest1", "rest2"],
    )

    assert user.phone == "1234567890"
    assert user.address == "123 Main St"
    assert user.location == "reykjavik"
    assert user.postal_code == "V1V1V1"
    assert user.latitude == 64.14
    assert user.longitude == -21.94
    
    # Verify the cart generated properly for this user
    assert user.cart.customer_id == "2"
    assert user.cart.items == []
    
    assert user.orders == ["order1"]
    assert user.owned_restaurants_id == ["rest1", "rest2"]


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("id", ""),
        ("id", "   "),
        ("id", 1),
        ("username", ""),
        ("username", "   "),
        ("username", 123),
        ("email", ""),
        ("email", "   "),
        ("email", 123),
        ("password_hash", ""),
        ("password_hash", "   "),
        ("password_hash", 123),
    ],
)
def test_required_fields_validation(field_name, value):
    """Reject invalid required user fields."""
    user_data = {
        "id": "1",
        "username": "anjana",
        "email": "anjana@gmail.com",
        "password_hash": "hashed_password",
    }
    user_data[field_name] = value

    with pytest.raises(ValueError):
        User(**user_data)


@pytest.mark.parametrize(
    "email",
    [
        "invalidemail",
        "abc@gmail",
    ],
)
def test_invalid_email_formats(email):
    """Reject invalid email formats."""
    with pytest.raises(ValueError):
        User(
            id="1",
            username="anjana",
            email=email,
            password_hash="hashed_password",
        )


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("phone", 123),
        ("address", []),
        ("location", {}),
        ("postal_code", 999),
    ],
)
def test_optional_string_fields_validation(field_name, value):
    """Reject invalid optional string fields."""
    user_data = {
        "id": "1",
        "username": "anjana",
        "email": "anjana@gmail.com",
        "password_hash": "hashed_password",
    }
    user_data[field_name] = value

    with pytest.raises(ValueError):
        User(**user_data)


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("latitude", "north"),
        ("longitude", "west"),
    ],
)
def test_coordinate_validation(field_name, value):
    """Reject invalid coordinate values."""
    user_data = {
        "id": "1",
        "username": "anjana",
        "email": "anjana@gmail.com",
        "password_hash": "hashed_password",
    }
    user_data[field_name] = value

    with pytest.raises(ValueError):
        User(**user_data)


def test_user_valid_numeric_coordinates():
    """Allow numeric latitude and longitude values."""
    user = User(
        id="3",
        username="mapuser",
        email="map@gmail.com",
        password_hash="hashed_password",
        latitude=64.14,
        longitude=-21.94,
    )

    assert user.latitude == 64.14
    assert user.longitude == -21.94


@pytest.mark.parametrize(
    "field_name,value",
    [
        # "cart" is removed from this test because it is no longer an input list field
        ("orders", "notalist"),
        ("owned_restaurants_id", "bakeryone"),
    ],
)
def test_list_fields_validation(field_name, value):
    """Reject invalid list fields."""
    user_data = {
        "id": "1",
        "username": "anjana",
        "email": "anjana@gmail.com",
        "password_hash": "hashed_password",
    }
    user_data[field_name] = value

    with pytest.raises(ValueError):
        User(**user_data)


def test_user_valid_empty_lists():
    """Allow empty list defaults for user collections."""
    user = User(
        id="4",
        username="emptylists",
        email="empty@gmail.com",
        password_hash="hashed_password",
        # 'cart' is removed from here too
        orders=[],
        owned_restaurants_id=[],
    )

    assert user.cart.customer_id == "4"
    assert user.cart.items == []
    assert user.orders == []
    assert user.owned_restaurants_id == []


def test_user_with_owned_restaurants():
    """Store owned restaurant ids on a user."""
    user = User(
        id="5",
        username="owner1",
        email="owner@gmail.com",
        password_hash="hashed_password",
        owned_restaurants_id=["rest1", "rest2"],
    )

    assert user.owned_restaurants_id == ["rest1", "rest2"]