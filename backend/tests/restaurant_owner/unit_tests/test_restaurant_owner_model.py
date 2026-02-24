# tests/restaurant_owner/unit_tests/test_restaurant_owner_model.py
import pytest
from unittest.mock import MagicMock
from backend.models.user.restaurant_owner_model import RestaurantOwner

'''Fixtures to create mock data for testing'''


@pytest.fixture
def owner():
    return RestaurantOwner(
        name="John_Doe",
        password_hash="SecurePass123"
    )


@pytest.fixture
def restaurant(owner):
    return owner.create_restaurant("John's Diner")


@pytest.fixture
def menu_item():
    item = MagicMock()
    item.id = 1
    item.name = "Burger"
    item.price = 9.99
    item.availability = True
    return item


'''Create restaurant'''


# Positive Functional Test: Check if restaurant is created successfully
def test_create_restaurant(owner):
    restaurant = owner.create_restaurant("John's Diner")
    assert restaurant is not None
    assert restaurant.name == "John's Diner"
    assert isinstance(restaurant.id, str)
    assert len(restaurant.id) > 0


# Negative Validation Test: Create restaurant with empty name
# should raise ValueError
def test_create_restaurant_empty_name(owner):
    with pytest.raises(ValueError, match="Restaurant name cannot be empty"):
        owner.create_restaurant("")


'''Update restaurant info'''


# Functional Test: Updating address
def test_update_restaurant_address(owner, restaurant):
    owner.update_info(restaurant, address="123 Main St")
    assert restaurant.address == "123 Main St"


# Functional Test: Updating multiple fields at once
def test_update_restaurant_multiple_fields(owner, restaurant):
    owner.update_info(restaurant, address="123 Main St", phone="555-1234")
    assert restaurant.address == "123 Main St"
    assert restaurant.phone == "555-1234"


'''Adding/removing menu items'''


# Functional Test: Adding a menu item
def test_add_menu_item(owner, restaurant, menu_item):
    owner.add_menu_item(restaurant, menu_item)
    assert menu_item in restaurant.menu


# Functional Test: Removing a menu item
def test_remove_menu_item(owner, restaurant, menu_item):
    owner.add_menu_item(restaurant, menu_item)
    owner.remove_menu_item(restaurant, menu_item)
    assert menu_item not in restaurant.menu


'''Updating menu items'''


# Functional Test: Updating price and availability of a menu item
def test_update_menu_item(owner, menu_item):
    owner.update_menu_item(menu_item, price=10.99, available=False)
    assert menu_item.price == 10.99  # Check if price was updated
    assert menu_item.availability is False


# Negative Test: Updating negative price of a menu item
def test_update_menu_item_negative_price(owner, menu_item):
    with pytest.raises(ValueError, match="Price cannot be negative"):
        owner.update_menu_item(menu_item, price=-5.99)


# Edge Case: Test updating price of a menu item to zero for free items
def test_update_menu_item_zero_price(owner, menu_item):
    owner.update_menu_item(menu_item, price=0.00)  # Set price to zero
    assert menu_item.price == 0.00  # Check if price was updated to zero


'''Set item availability'''


# Functional Test: Setting item availability
def test_set_item_availability(owner, menu_item):
    owner.set_item_availability(menu_item, True)
    assert menu_item.availability is True  # Check if item is available
    owner.set_item_availability(menu_item, False)
    assert menu_item.availability is False  # Check if item is unavailable


'''Set restaurant open/closed'''


# Functional Test: Setting restaurant to open and then closed
def test_set_open_closed(owner, restaurant):
    owner.set_open_closed(restaurant, True)
    assert restaurant.is_open is True
    owner.set_open_closed(restaurant, False)
    assert restaurant.is_open is False


# Negative Test: Setting restaurant open/closed with invalid status
def test_set_open_closed_invalid_status(owner, restaurant):
    with pytest.raises(ValueError, match="Status must be a boolean"):
        owner.set_open_closed(restaurant, "open")


'''Test restaurant operating hours'''


# Functional Test: Updating restaurant operating hours
def test_update_restaurant_hours(owner, restaurant):
    owner.update_info(restaurant, open_time="09:00", close_time="21:00")
    assert restaurant.open_time == "09:00"  # Check if open time was updated
    assert restaurant.close_time == "21:00"  # Check if close time was updated


# Edge Case: Test updating only one time field
def test_update_restaurant_hours_partial(owner, restaurant):
    restaurant.open_time = "08:00"  # Set initial open time
    restaurant.close_time = "20:00"  # Set initial close time
    owner.update_info(restaurant, open_time="10:00")  # Update only open time
    assert restaurant.open_time == "10:00"  # Check if open time was updated
    assert restaurant.close_time == "20:00"
