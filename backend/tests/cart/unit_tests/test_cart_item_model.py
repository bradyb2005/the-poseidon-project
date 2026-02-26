import pytest
from backend.models.cart.cart_item_model import CartItem


def test_cart_item_creation():
    item = CartItem(1, "Burger", 10.0, 2)

    assert item.product_id == 1
    assert item.quantity == 2
    assert item.subtotal() == 20.0


def test_invalid_quantity():
    with pytest.raises(ValueError):
        CartItem(1, "Burger", 10.0, 0)