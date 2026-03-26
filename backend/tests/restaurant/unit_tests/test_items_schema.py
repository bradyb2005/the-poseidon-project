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


# --- Validation & Boundary Tests ---

def test_menu_item_missing_mandatory_fields():
    """
    Exception Handling
    Ensures a ValidationError is raised when required fields are missing
    """
    with pytest.raises(ValidationError) as exc_info:
        # Missing price and restaurant_id
        MenuItem(item_name="Empty Item")

    assert "restaurant_id" in str(exc_info.value)
    assert "price" in str(exc_info.value)


def test_menu_item_negative_price(raw_menu_item_data):
    """
    Boundary Value Analysis
    Tests that the price validator prevents negative values
    """
    raw_menu_item_data["price"] = "-0.01"
    with pytest.raises(ValidationError, match="Price cannot be negative"):
        MenuItem(**raw_menu_item_data)


def test_menu_item_empty_name(raw_menu_item_data):
    """
    Fault Injection
    Tests that names cannot be empty strings or just whitespace
    """
    raw_menu_item_data["item_name"] = "   "
    with pytest.raises(ValidationError, match="Name cannot be empty"):
        MenuItem(**raw_menu_item_data)


# --- UUID Logic Tests ---

def test_menu_item_invalid_uuid(raw_menu_item_data):
    """
    Fault Injection
    Tests that a malformed UUID string triggers a validation error
    """
    raw_menu_item_data["id"] = "not-a-uuid-123"
    with pytest.raises(ValidationError, match="item_id must be a valid UUID string"):
        MenuItem(**raw_menu_item_data)


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


def test_update_item_invalid_price():
    """
    Constraint Test
    Ensures that even in the Update schema, a negative price is rejected.
    """
    with pytest.raises(ValidationError):
        UpdateMenuItemSchema(price="-5.00")

# --- Tag logic tests ---

def test_menu_item_tags_standardization(raw_menu_item_data):
    """
    Data Transformation
    Ensures tags are lowercased, stripped, and deduplicated.
    """
    raw_menu_item_data["tags"] = [" Spicy ", "spicy", "VEGAN", "  "]
    item = MenuItem(**raw_menu_item_data)

    assert item.tags == ["spicy", "vegan"]


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
