# backend/tests/restaurant/unit_tests/test_menu_item_model.py
import pytest
from backend.models.restaurant.menu_item_model import MenuItem


def test_menu_item_initialization():
    """
    Positive Functional Test: Verify a MenuItem can be created
    """
    item = MenuItem(
        id=1,
        restaurant_id=1,
        name="Tacos",
        price=12.99,
        availability=True,
        tags=["Main", "Vegetarian"]

    )
    assert item.id == 1
    assert item.restaurant_id == 1
    assert item.name == "Tacos"
    assert item.price == 12.99
    assert item.tags == ["Main", "Vegetarian"]
    assert item.description is None


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

def test_menu_item_availability_toggle():
    """
    Functional Test: Test toggling availability of a menu item
    """
    menu_item = MenuItem(
        id=3,
        restaurant_id=1,
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
        MenuItem(name="", restaurant_id=1, price=10.00)
    with pytest.raises(ValueError, match="Name cannot be empty"):
        MenuItem(name="  ", restaurant_id=1, price=10.00)


def test_menu_item_zero_price():
    """
    Edge Case Test: Price can be zero (e.g., for free items)
    """
    menu_item = MenuItem(
        id=6,
        restaurant_id=1,
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
            restaurant_id=1,
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
        restaurant_id=1,
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
        restaurant_id=1,
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
        MenuItem(name="Pizza", restaurant_id=1, price=10.00, tags="Vegetarian")

    # Case 2: Tags is a list but not all strings
    with pytest.raises(TypeError, match="Tags must be a list of strings"):
        MenuItem(name="Pizza", restaurant_id=1, price=10.00, tags=["Vegetarian", 123])
