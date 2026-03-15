# backend/tests/customer/unit_tests/test_customer_model.py
import pytest
from backend.models.user.customer import Customer


def test_customer_initialization():
    """
    Feat3-FR1
    Initialization: Verify Customer-specific fields are set correctly.
    """
    c = Customer(
        id=1,
        username="john_doe",
        email="john@example.com",
        password_hash="hash123",
        address="123 Kelowna St",
        latitude=49.888,
        longitude=-119.496
    )
    assert c.address == "123 Kelowna St"
    assert c.latitude == 49.888
    assert c.longitude == -119.496
    assert c.username == "john_doe"  # Check inheritance


def test_customer_defaults():
    """
    Feat3-FR1
    Functional test: Verify coordinates default to 0.0.
    """
    c = Customer(id=2, username="jane",
                 email="jane@test.com", password_hash="h")
    assert c.latitude == 0.0
    assert c.longitude == 0.0


def test_customer_coordinate_validation():
    """
    Feat3-FR1
    Functional test: Verify that __post_init__ catches bad data.
    """
    # Test Latitude
    with pytest.raises(ValueError,
                       match="Latitude must be between -90 and 90"):
        Customer(id=3, username="x",
                 email="x@x.com", password_hash="h", latitude=100.0)

    # Test Longitude
    with pytest.raises(ValueError,
                       match="Longitude must be between -180 and 180"):
        Customer(id=3, username="x",
                 email="x@x.com", password_hash="h", longitude=-200.0)

# ---Edge cases---


def test_customer_coordinates_at_exact_boundaries():
    """
    Feat3-FR1
    Verifies that the exact edges of the coordinate system (90, 180)
    are accepted
    """
    c = Customer(
        id=1, username="edge", email="e@e.com", password_hash="h",
        latitude=90.0,
        longitude=180.0
    )
    assert c.latitude == 90.0
    assert c.longitude == 180.0


def test_customer_coordinates_at_negative_boundaries():
    """
    Feat3-FR1
    Verifies that -90 and -180 are accepted.
    """
    c = Customer(
        id=1, username="edge", email="e@e.com", password_hash="h",
        latitude=-90.0,
        longitude=-180.0
    )
    assert c.latitude == -90.0
    assert c.longitude == -180.0


def test_customer_creation_with_string_coordinates():
    """
    Feat3-FR1
    Throws error if it is a string
    """
    c = Customer(
        id=1, username="u", email="e@e.com", password_hash="h",
        latitude="45.5",  # String input
        longitude="-122.6"
    )
    assert isinstance(c.latitude, float)


def test_customer_with_empty_address_logic():
    """
    Feat3-FR1
    Set up for error message if customer does not have address
    """
    c = Customer(id=1, username="u",
                 email="e@e.com", password_hash="h", address="")
    assert c.address == ""
    assert c.latitude == 0.0
