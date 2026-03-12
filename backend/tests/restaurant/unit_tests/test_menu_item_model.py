# backend/tests/restaurant/unit_tests/test_menu_item_model.py
import pytest
from backend.models.restaurant.menu_item_model import MenuItem


# --- Initialization Test ---

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


def test_menu_item_availability_toggle():
    """
    Functional Test: Test toggling availability of a menu item
    """
    menu_item = MenuItem(
        id=3,
        name="Spaghetti Carbonara",
        price=14.99,
        availability=True,
        tags=["Pasta", "Main"]
    )
    menu_item.availability = False
    assert menu_item.availability is False

# --- Validation tests ---


def test_menu_item_invalid_name():
    """
    Edge case test: Test that empty or whitespace only name raises ValueError
    """
    with pytest.raises(ValueError, match="Name cannot be empty"):
        MenuItem(name="", price=10.00)
    with pytest.raises(ValueError, match="Name cannot be empty"):
        MenuItem(name="  ", price=10.00)


def test_menu_item_zero_price():
    """
    Edge Case Test: Price can be zero (e.g., for free items)
    """
    menu_item = MenuItem(
        id=6,
        name="Complimentary Breadsticks",
        price=0.00,
        availability=True,
    )
    assert menu_item.price == 0.00
    assert isinstance(menu_item.price, float)


def test_menu_item_negative_price():
    """
    Edge Case Test: Price cannot be negative
    """
    with pytest.raises(ValueError, match="Price cannot be negative"):
        MenuItem(
            id=7,
            name="Negative Price Item",
            price=-5.00,
        )


# --- Tagging tests ---


def test_menu_item_tagging():
    """
    Functional Test: Feat2-FR2: Test that tags are correctly assigned
    """
    menu_item = MenuItem(
        id=4,
        name="Tiramisu",
        price=6.50,
        tags=["Dessert", "Vegetarian"]
    )
    assert menu_item.tags == ["Dessert", "Vegetarian"]
    assert "Dessert" in menu_item.tags
    assert len(menu_item.tags) == 2


def test_menu_item_default_tags():
    """
    Edge Case Test: Default tags should be an empty list if not provided
    """
    menu_item = MenuItem(
        id=5,
        name="Garlic Bread",
        price=4.99,
        availability=True
    )
    assert isinstance(menu_item.tags, list)
    assert len(menu_item.tags) == 0


def test_menu_item_invalid_tags_type():
    """
    Edge Case: Ensure Typeerror is raised if tags are not a list of strings
    """
    # Case 1: Tags is a string instead of list
    with pytest.raises(TypeError, match="Tags must be a list of strings"):
        MenuItem(name="Pizza", price=10.00, tags="Vegetarian")

    # Case 2: Tags is a list but not all strings
    with pytest.raises(TypeError, match="Tags must be a list of strings"):
        MenuItem(name="Pizza", price=10.00, tags=["Vegetarian", 123])
