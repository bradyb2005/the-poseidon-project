# python3 -m pytest backend/tests/cart/unit_tests/test_cart_item_model.py

import pytest
from unittest.mock import MagicMock
from backend.models.cart.cart_item_model import CartItem
from backend.models.restaurant.menu_item_model import MenuItem

@pytest.fixture
def mock_menu_item():
    """Creates a fake MenuItem so we don't depend on its internal logic."""
    return MagicMock(spec=MenuItem)

## --- Valid Case Tests ---

def test_cart_item_creation_valid(mock_menu_item):
    # Action
    cart_item = CartItem(id=1, menu_item=mock_menu_item, quantity=5)
    
    # Assert
    assert cart_item.id == 1
    assert cart_item.menu_item == mock_menu_item
    assert cart_item.quantity == 5

## --- Validation (Error) Tests ---

def test_cart_item_invalid_id(mock_menu_item):
    with pytest.raises(ValueError, match="id must be a non-negative integer"):
        CartItem(id=-1, menu_item=mock_menu_item, quantity=1)

def test_cart_item_invalid_menu_item_type():
    with pytest.raises(ValueError, match="menu_item must be a MenuItem object"):
        # Passing a string instead of a MenuItem object
        CartItem(id=1, menu_item="NotAMenuItem", quantity=1)

def test_cart_item_invalid_quantity_zero(mock_menu_item):
    with pytest.raises(ValueError, match="quantity must be a positive integer"):
        CartItem(id=1, menu_item=mock_menu_item, quantity=0)

def test_cart_item_invalid_quantity_negative(mock_menu_item):
    with pytest.raises(ValueError, match="quantity must be a positive integer"):
        CartItem(id=1, menu_item=mock_menu_item, quantity=-5)

def test_cart_item_invalid_quantity_type(mock_menu_item):
    with pytest.raises(ValueError, match="quantity must be a positive integer"):
        # Testing what happens if a float is passed
        CartItem(id=1, menu_item=mock_menu_item, quantity=1.5)