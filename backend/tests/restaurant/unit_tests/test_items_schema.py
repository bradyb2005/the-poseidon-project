# backend/tests/restaurant/unit_tests/test_items_schema.py
import pytest
from pydantic import ValidationError
from decimal import Decimal
from uuid import UUID
from backend.schemas.items_schema import MenuItem, UpdateMenuItemSchema

# --- Initialization Tests ---

def test_menu_item_initialization(raw_menu_item_data):
    """
    Equivalence Partitioning
    Ensures data from conftest is correctly mapped to schema
    """
    item = MenuItem(**raw_menu_item_data)
    assert item.name == "Beef Pie"
    assert item.restaurant_id == 10
    assert item.price == Decimal("12.50")
    assert isinstance(item.item_id, UUID)


def test_menu_item_populate_by_alias():
    """
    Functional logic test
    Tests that alias and data name are both accepted
    """
    data_alias = {"item_name": "Burger", "restaurant_id": 1, "price": 5.0}
    data_name = {"name": "Burger", "restaurant_id": 1, "price": 5.0}

    assert MenuItem(**data_alias).name == "Burger"
    assert MenuItem(**data_name).name == "Burger"


# --- UUID Logic Tests ---

def test_menu_item_invalid_uuid():
    """
    Tests that a valid string is turned into a UUID
    """
    valid_uuid_str = "550e8400-e29b-41d4-a716-446655440000"
    item = MenuItem(
        item_name="Pizza", 
        restaurant_id=1, 
        price=10.00, 
        id=valid_uuid_str
    )
    
    assert isinstance(item.item_id, UUID)
    assert str(item.item_id) == valid_uuid_str


# --- Update Schema Tests ---

def test_update_item_partial():
    """
    Functional Test
    Ensures UpdateMenuItemSchema allows updating a single field (like availability)
    without needing to send required info
    """
    update_data = {"availability": False}
    update_obj = UpdateMenuItemSchema(**update_data)

    assert update_obj.availability is False
    assert update_obj.name is None
    assert update_obj.price is None

# --- Tag logic tests ---

def test_menu_item_invalid_tags(raw_menu_item_data):
    """
    Fault Injection
    Ensures tags must be a list of strings.
    """
    raw_menu_item_data["tags"] = [123, None]
    with pytest.raises(ValidationError) as exc_info:
        MenuItem(**raw_menu_item_data)

# --- Serialization Test ---

def test_menu_item_serialization(sample_menu_item):
    """
    Serialization
    Uses the 'sample_menu_item' object fixture from conftest to test model_dump.
    """
    exported = sample_menu_item.model_dump(by_alias=True)

    assert exported["item_name"] == "Beef Pie"
    assert isinstance(exported["id"], UUID)
    assert isinstance(exported["price"], Decimal)
