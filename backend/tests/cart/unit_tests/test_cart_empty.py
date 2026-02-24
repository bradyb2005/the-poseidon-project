from backend.models.cart.cart_model import Cart


def test_cart_starts_empty():
    cart = Cart(id=1, user_id=1)

    assert cart.items == []
    assert len(cart.items) == 0