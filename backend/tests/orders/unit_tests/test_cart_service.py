# backend/tests/orders/unit_tests/test_cart_service.py
import pytest
from unittest.mock import MagicMock
from backend.services.cart_service import CartService
from backend.schemas.items_schema import MenuItem


@pytest.fixture
def mock_users(valid_uuids):
    return [
        {
            "id": "brady_123",
            "cart": {
                "customer_id": "brady_123",
                "items": [
                    {"menu_item_id": valid_uuids["item_1"], 
                     "quantity": 1, 
                     "price_at_time": 10.0}
                ]
            }
        },
        {
            "id": "empty_user",
            "cart": {"customer_id": "empty_user", "items": []}
        }
    ]

@pytest.fixture
def mock_menu_items(valid_uuids):
    item1 = MagicMock(spec=MenuItem)
    item1.item_id = valid_uuids["item_1"]
    item1.restaurant_id = "rest_A"
    item1.price = 10.0
    item1.availability = True

    item2 = MagicMock(spec=MenuItem)
    item2.item_id = valid_uuids["item_2"]
    item2.restaurant_id = "rest_A"
    item2.price = 15.0
    item2.availability = False # Unavailable item

    item3 = MagicMock(spec=MenuItem)
    item3.item_id = valid_uuids["item_3"]
    item3.restaurant_id = "rest_B" # Different restaurant
    item3.price = 20.0
    item3.availability = True

    item4 = MagicMock(spec=MenuItem)
    item4.item_id = valid_uuids["item_4"]
    item4.restaurant_id = "rest_A" # Must be the same restaurant as item_1!
    item4.price = 12.0
    item4.availability = True
    
    return [item1, item2, item3, item4]

@pytest.fixture
def cart_service(mock_users, mock_menu_items):
    service = CartService()
    
    service.user_repo = MagicMock()
    service.user_repo.load_all.return_value = mock_users
    
    service.menu_repo = MagicMock()
    service.menu_repo.load_all.return_value = mock_menu_items
    
    return service

# --- Tests ---

def test_add_to_cart_new_item_success(cart_service, valid_uuids):
    """Test adding a brand new item to an empty cart."""
    response, status = cart_service.add_to_cart("empty_user", valid_uuids["item_1"], 2)
    
    assert status == 200
    assert len(response["cart"]["items"]) == 1
    assert response["cart"]["items"][0]["quantity"] == 2
    cart_service.user_repo.save_all.assert_called_once() # Verify we tried to save

def test_add_to_cart_different_restaurant_fails(cart_service, valid_uuids):
    """Test the cross-restaurant ordering block."""
    # brady_123 already has item_1 (from rest_A). We try to add item_3 (from rest_B).
    response, status = cart_service.add_to_cart("brady_123", valid_uuids["item_3"], 1)
    
    assert status == 400
    assert "same restaurant" in response["error"]
    cart_service.user_repo.save_all.assert_not_called()

def test_add_to_cart_menu_item_not_found(cart_service):
    """Test the 404 handler when a non-existent menu item ID is added."""
    response, status = cart_service.add_to_cart("empty_user", "ghost_item", 1)
    
    assert status == 404
    assert "Menu item not found" in response["error"]
    cart_service.user_repo.save_all.assert_not_called()

def test_update_quantity_to_zero_removes_item(cart_service, valid_uuids):
    """Test the new UX tweak where setting quantity to 0 calls remove_from_cart."""
    response, status = cart_service.update_quantity("brady_123", valid_uuids["item_1"], 0)
    
    assert status == 200
    assert len(response["cart"]["items"]) == 0 # Item should be removed
    cart_service.user_repo.save_all.assert_called_once()

def test_update_quantity_item_not_in_cart(cart_service, valid_uuids):
    """Test updating the quantity of an item that isn't in the user's cart."""
    # empty_user has no items in their cart
    response, status = cart_service.update_quantity("empty_user", valid_uuids["item_1"], 2)
    
    assert status == 404
    assert "Menu item not found in cart" in response["error"]
    cart_service.user_repo.save_all.assert_not_called()

def test_add_to_cart_unavailable_item_fails(cart_service, valid_uuids):
    """Test that unavailable items are rejected."""
    # item_2 is explicitly marked as availability = False in the fixture
    response, status = cart_service.add_to_cart("empty_user", valid_uuids["item_2"], 1)
    
    assert status == 400
    assert "not available" in response["error"]
    cart_service.user_repo.save_all.assert_not_called()

def test_add_to_cart_existing_item_increments(cart_service, valid_uuids):
    """Test that adding an item already in the cart just increases the quantity."""
    # brady_123 already has 1 of item_1. Adding 3 more should equal 4.
    response, status = cart_service.add_to_cart("brady_123", valid_uuids["item_1"], 3)
    
    assert status == 200
    assert len(response["cart"]["items"]) == 1 # Still only one unique item
    assert response["cart"]["items"][0]["quantity"] == 4
    cart_service.user_repo.save_all.assert_called_once()

def test_update_quantity_success(cart_service, valid_uuids):
    """Test a standard quantity update."""
    response, status = cart_service.update_quantity("brady_123", valid_uuids["item_1"], 5)
    
    assert status == 200
    assert response["cart"]["items"][0]["quantity"] == 5
    cart_service.user_repo.save_all.assert_called_once()

def test_remove_from_cart_success(cart_service, valid_uuids):
    """Test removing a specific item from the cart."""
    response, status = cart_service.remove_from_cart("brady_123", valid_uuids["item_1"])
    
    assert status == 200
    assert len(response["cart"]["items"]) == 0
    cart_service.user_repo.save_all.assert_called_once()

def test_remove_item_not_in_cart(cart_service, valid_uuids):
    """Test removing an item that isn't in the user's cart."""
    response, status = cart_service.remove_from_cart("empty_user", valid_uuids["item_1"])
    
    assert status == 404
    assert "Menu item not found in cart" in response["error"]
    cart_service.user_repo.save_all.assert_not_called()

def test_remove_from_cart_keeps_other_items(cart_service, valid_uuids):
    """Test removing an item from the cart when multiple items are present."""
    cart_service.add_to_cart("brady_123", valid_uuids["item_4"], 1)
    cart_service.user_repo.save_all.reset_mock()

    response, status = cart_service.remove_from_cart("brady_123", valid_uuids["item_1"])
    
    assert status == 200
    assert len(response["cart"]["items"]) == 1 
    assert str(response["cart"]["items"][0]["menu_item_id"]) == valid_uuids["item_4"]
    cart_service.user_repo.save_all.assert_called_once()

def test_clear_cart_success(cart_service):
    """Test that clearing the cart removes all items but keeps the customer_id."""
    response, status = cart_service.clear_cart("brady_123")
    
    assert status == 200
    assert len(response["cart"]["items"]) == 0
    assert response["cart"]["customer_id"] == "brady_123"
    cart_service.user_repo.save_all.assert_called_once()

def test_user_not_found(cart_service, valid_uuids):
    """Test the 404 handler when a bad user ID is provided.
        The same test can be applied to all cart operations,
        but we'll just test add_to_cart because the other methods have the same user lookup logic."""
    response, status = cart_service.add_to_cart("ghost_user", valid_uuids["item_1"], 1)
    
    assert status == 404
    assert "User not found" in response["error"]