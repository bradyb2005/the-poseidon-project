# backend/tests/restaurant/unit_tests/test_restaurant_model.py
import pytest
from backend.models.restaurant.restaurant_model import Restaurant
from backend.models.restaurant.menu_item_model import MenuItem


@pytest.fixture
def sample_menu():
    return [
        MenuItem(name="Burger", price=9.99),
        MenuItem(name="Pizza", price=12.99)
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
    # Positive Functional Test: The restaurant model initializes correctly
    assert sample_restaurant.name == "Testaurant"
    assert sample_restaurant.open_time == 900
    assert sample_restaurant.close_time == 1700
    assert sample_restaurant.distance_from_user == 2.5
    assert len(sample_restaurant.menu) == 2
    assert isinstance(sample_restaurant.id, int)
    assert sample_restaurant.id == 0


def test_menu_item_initialization(sample_menu):
    # Positive Functional Test: The menu item models are stored correctly
    item = sample_menu[0]
    assert item.name == "Burger"
    assert item.price == 9.99
    assert isinstance(item.id, int)


# FR3: Validation tests

def test_validate_for_publish_success(mock_owner):
    # Positive functional test: Valid restaurant should pass validation
    restaurant = Restaurant(
        name="Testaurant",
        owner=mock_owner,
        address="123 Test St",
        phone="123-456-7890",
        open_time=900,
        close_time=2100,
        menu=[MenuItem(name="Burger", price=9.99)]
    )
    restaurant.validate_for_publish()


def test_validate_for_publish_missing_field(mock_owner):
    # Negative functional test: Should not pass if missing a field
    restaurant = Restaurant(
        name="Testaurant",
        owner=mock_owner,
        phone="123-456-7890",
        open_time=900,
        close_time=2100,
        menu=[MenuItem(name="Burger", price=9.99)]
        # address missing
    )
    with pytest.raises(ValueError, match="'address' is required."):
        restaurant.validate_for_publish()


def test_validate_for_publish_invalid_types(mock_owner):
    # Negative functional test: Should not pass if type check fails
    restaurant = Restaurant(
        name="Testaurant",
        owner=mock_owner,
        address="123 Test St",
        phone="123-456-7890",
        open_time="900",
        close_time=2100,
        menu=[MenuItem(name="Burger", price=9.99)]
    )
    with pytest.raises(ValueError, match="must be numbers"):
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
        menu=[MenuItem(name="Burger", price=9.99)]
    )
    with pytest.raises(ValueError, match="must be before 'close_time'"):
        restaurant.validate_for_publish()
