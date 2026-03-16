# backend/tests/restaurant/unit_tests/test_restaurant_model.py
import pytest
from unittest.mock import MagicMock
from backend.models.restaurant.restaurant_model import Restaurant
from backend.models.restaurant.menu_item_model import MenuItem


@pytest.fixture
def mock_owner():
    return MagicMock()


@pytest.fixture
def sample_menu():
    return [
        MenuItem(name="Burger", price=9.99, restaurant_id=1),
        MenuItem(name="Pizza", price=12.99, restaurant_id=1)
    ]


@pytest.fixture
def sample_restaurant(mock_owner, sample_menu):
    return Restaurant(
        name="Testaurant",
        owner=mock_owner,
        open_time=900,
        close_time=1700,
        address="123 Test St",
        phone="555-555-5555",
        distance_from_user=2.5,
        menu=sample_menu
    )


''' Create restaurant initialization'''


def test_restaurant_initialization(sample_restaurant):
    # Positive Functional Test:
    # The restaurant model initializes correctly
    assert sample_restaurant.name == "Testaurant"
    assert sample_restaurant.address == "123 Test St"
    assert sample_restaurant.id is None
    assert sample_restaurant.open_time == 900
    assert sample_restaurant.close_time == 1700
    assert sample_restaurant.distance_from_user == 2.5
    assert len(sample_restaurant.menu) == 2


def test_menu_item_initialization(sample_menu):
    # Positive Functional Test:
    # The menu item models are stored correctly
    item = sample_menu[0]
    assert item.name == "Burger"
    assert item.price == 9.99
    assert item.restaurant_id == 1
    assert item.id is None


def test_get_view_includes_address(sample_restaurant):
    # Positive Functional test:
    # Verify search results show location
    sample_restaurant.is_published = True
    view = sample_restaurant.get_view("Customer")
    assert "address" in view
    assert view["address"] == "123 Test St"

# F2FR3: Validation tests


def test_validate_for_publish_success(mock_owner):
    # Positive functional test:
    # Valid restaurant should pass validation
    restaurant = Restaurant(
        name="Testaurant",
        owner=mock_owner,
        address="123 Test St",
        phone="123-456-7890",
        open_time=900,
        close_time=2100,
        menu=[MenuItem(name="Burger",
                       price=9.99, restaurant_id=1)]
    )
    restaurant.validate_for_publish()


def test_validate_for_publish_missing_field(mock_owner):
    # Negative functional test:
    # Should not pass if missing a field
    restaurant = Restaurant(
        name="Testaurant",
        owner=mock_owner,
        phone="123-456-7890",
        open_time=900,
        close_time=2100,
        menu=[MenuItem(name="Burger",
                       price=9.99, restaurant_id=1)]
    )
    with pytest.raises(ValueError,
                       match="'address' is required."):
        restaurant.validate_for_publish()


def test_validate_for_publish_invalid_types(mock_owner):
    # Negative functional test: Should not pass if
    # type check fails
    restaurant = Restaurant(
        name="Testaurant",
        owner=mock_owner,
        address="123 Test St",
        phone="123-456-7890",
        open_time="900",
        close_time=2100,
        menu=[MenuItem(name="Burger",
                       price=9.99, restaurant_id=1)]
    )
    with pytest.raises(ValueError,
                       match="must be numbers"):
        restaurant.validate_for_publish()


def test_validate_for_publish_logic_error(mock_owner):
    # Negative funtional test: Should not pass if logic check fails
    restaurant = Restaurant(
        name="Testaurant",
        owner=mock_owner,
        address="123 Test St",
        phone="123-456-7890",
        open_time=2200,
        close_time=2100,
        menu=[MenuItem(name="Burger",
                       price=9.99, restaurant_id=1)]
    )
    with pytest.raises(ValueError,
                       match="must be before 'close_time'"):
        restaurant.validate_for_publish()

# --- F3-FR2: Searching ---


def test_validate_for_publish_empty_address(mock_owner):
    # Edge Case: Address is an empty string instead of None
    restaurant = Restaurant(
        name="Testaurant",
        owner=mock_owner,
        address="   ",
        phone="123-456-7890",
        open_time=900,
        close_time=2100,
        menu=[MenuItem(name="Burger",
                       price=9.99, restaurant_id=1)]
    )
    with pytest.raises(ValueError,
                       match="'address' is required"):
        restaurant.validate_for_publish()


def test_menu_item_without_restaurant_id():
    # Edge Case: Attempting to create a menu item
    # without required owner link
    with pytest.raises(TypeError):
        MenuItem(name="Ghost Burger", price=5.00)
