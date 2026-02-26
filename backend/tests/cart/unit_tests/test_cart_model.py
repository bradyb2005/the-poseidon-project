import pytest

from backend.models.cart.cart_model import Cart


def test_cart_valid_creation():
    c = Cart(id=1, user_id=10)
    assert c.id == 1
    assert c.user_id == 10
    assert c.restaurant_id is None
    assert c.items == []


def test_cart_invalid_ids():
    with pytest.raises(ValueError):
        Cart(id=-1, user_id=1)
    with pytest.raises(ValueError):
        Cart(id=1, user_id=-1)
    with pytest.raises(ValueError):
        Cart(id=1, user_id=1, restaurant_id=-5)


def test_add_item_new_and_increment():
    c = Cart(id=1, user_id=10)

    c.add_item(menu_item_id=99, quantity=2)
    assert len(c.items) == 1
    assert c.items[0].menu_item_id == 99
    assert c.items[0].quantity == 2

    c.add_item(menu_item_id=99, quantity=3)
    assert len(c.items) == 1
    assert c.items[0].quantity == 5


def test_add_item_rejects_bad_quantity():
    c = Cart(id=1, user_id=10)
    with pytest.raises(ValueError):
        c.add_item(menu_item_id=1, quantity=0)


def test_update_quantity_and_missing_item():
    c = Cart(id=1, user_id=10)
    c.add_item(menu_item_id=5, quantity=1)

    c.update_quantity(menu_item_id=5, quantity=4)
    assert c.items[0].quantity == 4

    with pytest.raises(ValueError):
        c.update_quantity(menu_item_id=5, quantity=0)

    with pytest.raises(ValueError):
        c.update_quantity(menu_item_id=123, quantity=2)


def test_remove_item():
    c = Cart(id=1, user_id=10)
    c.add_item(1, 1)
    c.add_item(2, 1)

    c.remove_item(1)
    assert [it.menu_item_id for it in c.items] == [2]


def test_cart_to_dict_roundtrip():
    c1 = Cart(id=1, user_id=10, restaurant_id=7)
    c1.add_item(3, 2)

    data = c1.to_dict()
    c2 = Cart.from_dict(data)

    assert c2.id == c1.id
    assert c2.user_id == c1.user_id
    assert c2.restaurant_id == c1.restaurant_id
    assert len(c2.items) == 1
    assert c2.items[0].menu_item_id == 3
    assert c2.items[0].quantity == 2