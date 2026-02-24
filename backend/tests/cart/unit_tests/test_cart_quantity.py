from backend.models.cart.cart_item_model import CartItem


def test_update_quantity():
    item = CartItem(1, "Burger", 10.0, 1)
    item.update_quantity(5)

    assert item.quantity == 5
    assert item.subtotal() == 50.0