# backend/tests/restaurant/unit_tests/test_menu_item_model.py
import pytest
from backend.models.restaurant.menu_item_model import MenuItem

# Initialization Test
def test_menu_item_initialization():
    """
    Test initialization of MenuItem
    """
    menu_item = MenuItem(
        id=1,
        name="Margherita Pizza",
        price=12.99,
        availability=True,
        tags=["Main", "Vegetarian"]

    )
    assert menu_item.id == 1
    assert menu_item.name == "Margherita Pizza"
    assert menu_item.price == 12.99
    assert menu_item.availability is True
    assert menu_item.tags == ["Main", "Vegetarian"]
    # Ensure that optional fields are set to None by default
    assert menu_item.description is None
    assert menu_item.category is None

# Functional Test: Price is always a float and availability is always a boolean
def test_menu_item_type_integrity():
    """
    Ensure price stays as float and availability stays as boolean
    """
    menu_item = MenuItem(
        id=2,
        name="Caesar Salad",
        price=8.50,
        availability=False,
        tags=["Salad", "Vegetarian"]
    )
    assert isinstance(menu_item.price, float)
    assert isinstance(menu_item.availability, bool)

# Functional Test: Toggling availability
def test_menu_item_availability_toggle():
    """
    Test toggling availability of a menu item
    """
    menu_item = MenuItem(
        id=3,
        name="Spaghetti Carbonara",
        price=14.99,
        availability=True,
        tags=["Pasta", "Main"]
    )
    # Toggle availability
    menu_item.availability = False
    assert menu_item.availability is False

# Functional Test: Tagging functionality
def test_menu_item_tagging():
    """
    Feat2-FR2: Test that tags are correctly assigned
    """
    menu_item = MenuItem(
        id=4,
        name="Tiramisu",
        price=6.50,
        availability=True,
        tags=["Dessert", "Vegetarian"]
    )
    assert menu_item.tags == ["Dessert", "Vegetarian"]
    assert "Dessert" in menu_item.tags
    assert len(menu_item.tags) == 2

# Edge Case Test: Default tags should be an empty list if not provided
def test_menu_item_default_tags():
    """
    Test that tags default to an empty list if not provided
    """
    menu_item = MenuItem(
        id=5,
        name="Garlic Bread",
        price=4.99,
        availability=True
    )
    assert isinstance(menu_item.tags, list)
    assert len(menu_item.tags) == 0

# Edge Case Test: Price can be zero (e.g., for free items)
def test_menu_item_zero_price():
    """
    Test that a menu item can have a price of zero (e.g., for free items)
    """
    menu_item = MenuItem(
        id=6,
        name="Complimentary Breadsticks",
        price=0.00,
        availability=True,
    )
    assert menu_item.price == 0.00
    assert isinstance(menu_item.price, float)

# Edge Case Test: Price cannot be negative
def test_menu_item_negative_price():
    """
    Test that a menu item cannot have a negative price
    """
    with pytest.raises(ValueError):
        MenuItem(
            id=7,
            name="Negative Price Item",
            price=-5.00,
            availability=True,
        )
