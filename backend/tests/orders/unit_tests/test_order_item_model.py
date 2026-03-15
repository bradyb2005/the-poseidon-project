# python3 -m pytest backend/tests/orders/unit_tests/test_order_item_model.py

import pytest
from unittest.mock import Mock

from backend.models.orders.order_item_model import OrderItem, MenuItem

# --- FIXTURES ---

@pytest.fixture
def mock_menu_item():
    """Creates a mock that will pass the isinstance(..., MenuItem) check."""
    return Mock(spec=MenuItem)

@pytest.fixture
def valid_order_item_data(mock_menu_item):
    """Provides a valid dictionary of kwargs to successfully create an OrderItem."""
    return {
        "id": 1,
        "menu_item": mock_menu_item,
        "quantity": 2,
        "price_at_time": 14.99
    }


# --- TESTS ---

def test_order_item_creation_success(valid_order_item_data):
    """Test that a valid OrderItem is created without raising any exceptions."""
    item = OrderItem(**valid_order_item_data)
    
    assert item.id == 1
    assert item.quantity == 2
    assert item.price_at_time == 14.99
    assert item.menu_item is valid_order_item_data["menu_item"]

# --- ID Validation Tests ---

def test_invalid_id_type_raises_error(valid_order_item_data):
    """Test that a non-integer ID triggers a ValueError."""
    valid_order_item_data["id"] = "1"
    
    with pytest.raises(ValueError, match="id must be a non-negative integer"):
        OrderItem(**valid_order_item_data)

def test_invalid_id_negative_raises_error(valid_order_item_data):
    """Test that a negative ID triggers a ValueError."""
    valid_order_item_data["id"] = -1
    
    with pytest.raises(ValueError, match="id must be a non-negative integer"):
        OrderItem(**valid_order_item_data)

# --- MenuItem Validation Tests ---

def test_invalid_menu_item_type_raises_error(valid_order_item_data):
    """Test that passing a non-MenuItem object triggers a ValueError."""
    valid_order_item_data["menu_item"] = "Not a MenuItem"
    
    with pytest.raises(ValueError, match="menu_item must be a MenuItem object"):
        OrderItem(**valid_order_item_data)

# --- Quantity Validation Tests ---

def test_invalid_quantity_type_raises_error(valid_order_item_data):
    """Test that a non-integer quantity triggers a ValueError."""
    valid_order_item_data["quantity"] = 2.5
    
    with pytest.raises(ValueError, match="quantity must be a positive integer"):
        OrderItem(**valid_order_item_data)

def test_invalid_quantity_zero_raises_error(valid_order_item_data):
    """Test that a quantity of zero triggers a ValueError."""
    valid_order_item_data["quantity"] = 0
    
    with pytest.raises(ValueError, match="quantity must be a positive integer"):
        OrderItem(**valid_order_item_data)

def test_invalid_quantity_negative_raises_error(valid_order_item_data):
    """Test that a negative quantity triggers a ValueError."""
    valid_order_item_data["quantity"] = -5
    
    with pytest.raises(ValueError, match="quantity must be a positive integer"):
        OrderItem(**valid_order_item_data)

# --- Price Validation Tests ---

def test_invalid_price_type_raises_error(valid_order_item_data):
    """Test that a non-numeric price triggers a ValueError."""
    valid_order_item_data["price_at_time"] = "14.99"
    
    with pytest.raises(ValueError, match="price_at_time must be a non-negative number"):
        OrderItem(**valid_order_item_data)

def test_invalid_price_negative_raises_error(valid_order_item_data):
    """Test that a negative price triggers a ValueError."""
    valid_order_item_data["price_at_time"] = -14.99
    
    with pytest.raises(ValueError, match="price_at_time must be a non-negative number"):
        OrderItem(**valid_order_item_data)