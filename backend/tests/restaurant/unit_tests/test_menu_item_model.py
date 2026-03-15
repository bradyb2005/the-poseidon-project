# backend/tests/restaurant/unit_tests/test_menu_item_model.py
import pytest
from backend.models.restaurant.menu_item_model import MenuItem


def test_menu_item_initialization():
    """
    Positive Functional Test: Verify a MenuItem can be created
    """
    item = MenuItem(name="Tacos", price=10.50, restaurant_id=1)

    assert item.name == "Tacos"
    assert item.price == 10.50
    assert item.restaurant_id == 1
    assert item.id is None  # Confirms our Optional[int] = None update


def test_menu_item_missing_restaurant_id():
    """
    Negative Edge Case: A menu item must belong to a restaurant
    """
    with pytest.raises(TypeError):
        # Missing the mandatory restaurant_id argument
        MenuItem(name="Ghost Burger", price=5.00)

def test_menu_item_repr():
    """
    Functional test: Verify the string representation
    includes the restaurant_id
    Will help with searching
    """
    item = MenuItem(name="Taco", price=5.0, restaurant_id=10, id=1)
    repr_str = repr(item)
    assert "name='Taco'" in repr_str
    assert "restaurant_id=10" in repr_str
