# tests/restaurant_owner/unit_tests/test_restaurant_owner_model.py
import pytest
from unittest.mock import MagicMock
from backend.models import RestaurantOwner

'''Fixtures to create mock data for testing'''

@pytest.fixture
def owner():
    return RestaurantOwner(
        id=1,
        username="John_Doe",
        password_hash= RestaurantOwner.hash_password("SecurePass123"),
        
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

#Check if restaurant is created successfully
def test_create_restaurant(owner):
    restaurant = owner.create_restaurant("John's Diner")
    assert restaurant is not None

#Set name of restaurant
def test_create_restaurant_name(owner):
    restaurant = owner.create_restaurant("John's Diner")
    assert restaurant.name == "John's Diner"

'''Update restaurant info'''

# Test updating address
def test_update_restaurant_address(owner, restaurant):
    owner.update_info(restaurant, address="123 Main St")
    assert restaurant.address == "123 Main St"

# Test updating multiple fields at once
def test_update_restaurant_multiple_fields(owner, restaurant):
    owner.update_info(restaurant, address="123 Main St", phone="555-1234")
    assert restaurant.address == "123 Main St"
    assert restaurant.phone == "555-1234"

# Test updating with no fields (should not change anything)
def test_update_restaurant_no_fields(owner, restaurant):
    restaurant.address = "123 Main St"
    owner.update_info(restaurant, phone= 555-1234)
    assert restaurant.address == "123 Main St"

'''Adding menu items'''

# Test adding a menu item
def test_add_menu_item(owner, restaurant, menu_item):
    owner.add_menu_item(restaurant, menu_item)
    assert menu_item in restaurant.menu

# Test adding multiple menu items
def test_add_multiple_menu_items(owner, restaurant, menu_item):
    item1 = MagicMock()
    item2 = MagicMock()
    owner.add_menu_item(restaurant, item1)
    owner.add_menu_item(restaurant, item2)
    assert len(restaurant.menu) == 2 # Check if both items were added

'''Removing menu items'''
# Test removing a menu item
def test_remove_menu_item(owner, restaurant, menu_item):
    owner.add_menu_item(restaurant, menu_item)
    owner.remove_menu_item(restaurant, menu_item)
    assert menu_item not in restaurant.menu # Check if item was removed
# Test removing an item that doesn't exist (should not raise an error)
def test_remove_nonexistent_menu_item(owner, restaurant, menu_item):
    item = MagicMock()
    item.id = 2
    item.name = "Fries"
    item.price = 3.99
    item.availability = True
    owner.add_menu_item(restaurant, menu_item)
    owner.remove_menu_item(restaurant, item) # Try to remove an item that was not added
    assert menu_item in restaurant.menu # Check if original item is still there
# Test removing one item when multiple items are present
def test_remove_correct_menu_item(owner, restaurant, menu_item):
    item1 = MagicMock(id=1)
    item2 = MagicMock(id=2)
    owner.add_menu_item(restaurant, item1)
    owner.add_menu_item(restaurant, item2)
    owner.remove_menu_item(restaurant, item1) # Remove first item
    assert item1 not in restaurant.menu # Check if first item was removed
    assert item2 in restaurant.menu # Check if second item is still there

'''Updating menu items'''
# Test updating price and availability of a menu item
def test_update_menu_item(owner, restaurant, menu_item):
    owner.add_menu_item(restaurant, menu_item)
    owner.update_menu_item(restaurant, menu_item.id, price=10.99, availability=False)
    assert menu_item.price == 10.99 # Check if price was updated
    assert menu_item.availability == False # Check if availability was updated
# Test updating negative price of a menu item
def test_update_menu_item_negative_price(owner, restaurant, menu_item):
    owner.add_menu_item(restaurant, menu_item)
    with pytest.raises(ValueError, match="Price cannot be negative"):
        owner.update_menu_item(restaurant, menu_item.id, price=-5.99) # Try to set a negative price
# Test updating nonexistent menu item
def test_update_menu_item_nonexistent(owner, restaurant):
    with pytest.raises(ValueError, match="Menu item not found"):
        owner.update_menu_item(restaurant, 999, price=10.99) # Try to update an item that doesn't exist

'''Set item availability'''
# Test setting item availability to false
def test_set_item_availability_false(owner, menu_item):
    owner.set_item_availability(menu_item, False) # Set item to unavailable
    assert menu_item.availability == False # Check if item is unavailable

def test_set_item_availability_true(owner, menu_item):
    owner.set_item_availability(menu_item, True) # Set item to available
    assert menu_item.availability == True # Check if item is available

'''Set restaurant open/closed'''
# Test setting restaurant to open and then closed
def test_set_open_closed(owner, restaurant):
    owner.set_open_closed(restaurant, True) # Set restaurant to open
    assert restaurant.is_open == True # Check if restaurant is open
    owner.set_open_closed(restaurant, False) # Set restaurant to closed
    assert restaurant.is_open == False # Check if restaurant is closed
# Test setting restaurant open/closed with invalid status
def test_set_open_closed_invalid_status(owner, restaurant):
    with pytest.raises(ValueError, match="Status must be a boolean"):
        owner.set_open_closed(restaurant, "open") # Try to set an invalid status