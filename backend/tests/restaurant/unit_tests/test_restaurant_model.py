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
def sample_restaurant(sample_menu):
    return Restaurant(
        name="Testaurant",
        open_time="09:00",
        close_time="17:00",
        distance_from_user=2.5,
        menu=sample_menu
    )


''' Create restaurant initialization'''


# Positive Functional Test: The restaurant model initializes correctly with attributes
def test_restaurant_initialization(sample_restaurant):
    assert sample_restaurant.name == "Testaurant"
    assert sample_restaurant.open_time == "09:00"
    assert sample_restaurant.close_time == "17:00"
    assert sample_restaurant.distance_from_user == 2.5
    assert len(sample_restaurant.menu) == 2

# Positive Functional Test: Tests that user can store before publishing
def test_owner_publish_flow(sample_restaurant):
    assert sample_restaurant.is_published == False is False

    success = sample_restaurant.publish()
    assert success is True
    assert sample_restaurant.is_published is True

# Positive Functional Test: Tests that different perspectives can be used
def test_admin_customer_perspective(sample_restaurant):
    # Customer perspective should not see unpublished restaurant
    assert sample_restaurant.get_view("Customer") is None

    # Restaurant owner/ admin should see unpublished restaurant
    owner_view = sample_restaurant.get_view("Restaurant")
    assert owner_view is not None
    assert owner_view["name"] == "Testaurant"

    sample_restaurant.publish()
    assert sample_restaurant.get_view("Customer") is not None

# Negative Edge Case: Cannot publish without menu
def test_publish_without_menu():
    empty_menu_restaurant = Restaurant("EmptyMenu", "10:00", "20:00", 1.0, [])
    success = empty_menu_restaurant.publish()
    assert success is False
    assert empty_menu_restaurant.is_published is False
    assert empty_menu_restaurant.get_view("Customer") is None

# Positive Functional Test: The menu item models are stored correctly
def test_menu_item_initialization(sample_menu):
    item = sample_menu[0]
    assert item.name == "Burger"
    assert item.price == 9.99
    assert isinstance(item.id, str)