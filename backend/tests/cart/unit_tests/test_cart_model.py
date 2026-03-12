# python3 -m pytest backend/tests/cart/unit_tests/test_cart_model.py

import pytest
from backend.models.cart.cart_model import Cart

# -----------------------------------------------------------------------------
# Dummy Classes (Isolates the Cart test from other models)
# -----------------------------------------------------------------------------
class DummyCustomer: 
    def __init__(self):
        self.id = 1
        self.cart = None

class DummyMenuItem:
    def __init__(self, item_id: int):
        self.id = item_id

class DummyCartItem:
    def __init__(self, menu_item: DummyMenuItem, quantity: int):
        self.menu_item = menu_item
        self.quantity = quantity

# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture
def empty_cart():
    """Provides a fresh, empty cart for a dummy customer."""
    customer = DummyCustomer()
    return Cart(id=customer.id, customer=customer)

@pytest.fixture
def burger_item():
    """Provides a dummy CartItem representing 2 Burgers."""
    menu_item = DummyMenuItem(item_id=101)
    return DummyCartItem(menu_item=menu_item, quantity=2)

@pytest.fixture
def fries_item():
    """Provides a dummy CartItem representing 1 order of Fries."""
    menu_item = DummyMenuItem(item_id=102)
    return DummyCartItem(menu_item=menu_item, quantity=1)

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
def test_cart_initialization(empty_cart):
    """Tests that a cart starts with the correct ID and an empty list."""
    assert empty_cart.id == 1
    assert isinstance(empty_cart.customer, DummyCustomer)
    assert len(empty_cart.items) == 0

def test_add_new_item(empty_cart, burger_item):
    """Tests adding a brand new item to the cart."""
    empty_cart.add_item(burger_item)
    
    assert len(empty_cart.items) == 1
    assert empty_cart.items[0] == burger_item
    assert empty_cart.items[0].quantity == 2

def test_add_existing_item(empty_cart, burger_item):
    """Tests that adding an item that already exists just increases the quantity."""
    # Add the first 2 burgers
    empty_cart.add_item(burger_item)
    
    # Create another CartItem for 3 MORE burgers (same menu_item.id)
    more_burgers = DummyCartItem(menu_item=DummyMenuItem(item_id=101), quantity=3)
    empty_cart.add_item(more_burgers)
    
    # The list should still only have 1 entry, but the quantity should now be 5
    assert len(empty_cart.items) == 1
    assert empty_cart.items[0].quantity == 5

def test_remove_item(empty_cart, burger_item, fries_item):
    """Tests removing a specific item from the cart."""
    empty_cart.add_item(burger_item)
    empty_cart.add_item(fries_item)
    
    # Remove the burgers
    empty_cart.remove_item(burger_item)
    
    assert len(empty_cart.items) == 1
    assert empty_cart.items[0] == fries_item

def test_update_quantity_success(empty_cart, burger_item):
    """Tests manually updating the quantity of an item."""
    empty_cart.add_item(burger_item)
    
    # Update from 2 to 10
    empty_cart.update_quantity(burger_item, 10)
    
    assert empty_cart.items[0].quantity == 10

def test_update_quantity_to_zero_removes_item(empty_cart, burger_item):
    """Tests that updating a quantity to 0 or less completely removes the item."""
    empty_cart.add_item(burger_item)
    
    # Drop quantity to 0
    empty_cart.update_quantity(burger_item, 0)
    
    assert len(empty_cart.items) == 0

def test_clear_cart(empty_cart, burger_item, fries_item):
    """Tests that clear() completely empties the cart."""
    empty_cart.add_item(burger_item)
    empty_cart.add_item(fries_item)
    assert len(empty_cart.items) == 2
    
    empty_cart.clear()
    
    assert len(empty_cart.items) == 0