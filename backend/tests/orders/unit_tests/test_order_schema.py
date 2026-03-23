# backend/tests/orders/unit_tests/test_order_schema.py
import pytest
from pydantic import ValidationError
from backend.schemas.order_schema import (
    Order, 
    OrderCreate, 
    OrderUpdate, 
    OrderItem, 
    OrderItemCreate, 
    OrderItemUpdate, 
    OrderStatus)

# -- OrderItem Tests --
def test_create_order_item_success():
    """Test that creating an OrderItem with valid data succeeds."""
    item = OrderItemCreate(menu_item_id=1, quantity=2)
    assert item.menu_item_id == 1
    assert item.quantity == 2

def test_create_order_item_invalid_quantity():
    """Test that creating an OrderItem with a quantity of 0 or less raises a ValidationError."""
    with pytest.raises(ValidationError):
        OrderItemCreate(menu_item_id=1, quantity=0)

def test_update_order_item_success():
    """Test that updating an OrderItem with valid data succeeds."""
    item = OrderItemUpdate(quantity=3)
    assert item.quantity == 3

def test_update_order_item_invalid_quantity():
    """Test that updating an OrderItem with a quantity of 0 or less raises a ValidationError."""
    with pytest.raises(ValidationError):
        OrderItemUpdate(quantity=0)

# -- Order Tests --
def test_create_order_success():
    """Test that creating an Order with valid data succeeds."""
    order = OrderCreate(
        customer_id="testcustomer123",
        restaurant_id=1,
        items=[OrderItemCreate(menu_item_id=1, quantity=2)],
        delivery_latitude=49.9423,
        delivery_longitude=-119.3960,
        delivery_postal_code="V1V 1V7"
    )
    assert order.customer_id == "testcustomer123"
    assert order.restaurant_id == 1
    assert len(order.items) == 1
    assert order.items[0].menu_item_id == 1
    assert order.items[0].quantity == 2 
    assert order.delivery_latitude == 49.9423
    assert order.delivery_longitude == -119.3960
    assert order.delivery_postal_code == "V1V 1V7"

    # Check for one of the attributes in Order that OrderCreate doesn't have, to ensure it's not accidentally initialized.
    # Checking for "status":
    assert not hasattr(order, "status")

@pytest.mark.parametrize("valid_latitude", [90.0, -90.0])
def test_create_order_valid_latitude(valid_latitude):
    """Edge Case Test:
    Test that creating an Order with a valid latitude succeeds.
    Valid values: 90.0, -90.0 (boundary values)"""
    order = OrderCreate(
        customer_id="testcustomer123",
        restaurant_id=1,
        items=[OrderItemCreate(menu_item_id=1, quantity=2)],
        delivery_latitude=valid_latitude,
        delivery_longitude=-119.3960,
        delivery_postal_code="V1V 1V7"
    )
    assert order.delivery_latitude == valid_latitude

@pytest.mark.parametrize("invalid_latitude", [90.1, -90.1])
def test_create_order_invalid_latitude(invalid_latitude):
    """Boundary Test:
    Test that creating an Order with an invalid latitude raises a ValidationError.
    Invalid values: 90.1, -90.1 (outside valid range)"""
    with pytest.raises(ValidationError):
        OrderCreate(
            customer_id="testcustomer123",
            restaurant_id=1,
            items=[OrderItemCreate(menu_item_id=1, quantity=2)],
            delivery_latitude=invalid_latitude,
            delivery_longitude=-119.3960,
            delivery_postal_code="V1V 1V7"
        )

@pytest.mark.parametrize("valid_longitude", [180.0, -180.0])
def test_create_order_valid_longitude(valid_longitude):
    """Edge Case Test: 
    Test that creating an Order with a valid longitude succeeds.
    Valid values: 180.0, -180.0 (boundary values)"""
    order = OrderCreate(
        customer_id="testcustomer123",
        restaurant_id=1,
        items=[OrderItemCreate(menu_item_id=1, quantity=2)],
        delivery_latitude=49.9423,
        delivery_longitude=valid_longitude,
        delivery_postal_code="V1V 1V7"
    )
    assert order.delivery_longitude == valid_longitude

@pytest.mark.parametrize("invalid_longitude", [180.1, -180.1])
def test_create_order_invalid_longitude(invalid_longitude):
    """Boundary Test: 
    Test that creating an Order with an invalid longitude raises a ValidationError.
    Invalid values: 180.1, -180.1 (outside valid range)"""
    with pytest.raises(ValidationError):
        OrderCreate(
            customer_id="testcustomer123",
            restaurant_id=1,
            items=[OrderItemCreate(menu_item_id=1, quantity=2)],
            delivery_latitude=49.9423,
            delivery_longitude=invalid_longitude,
            delivery_postal_code="V1V 1V7"
        )

postal_base_data = {
    "customer_id": "testcustomer123",
    "restaurant_id": 1,
    "items": [{"menu_item_id": 1, "quantity": 2}],
    "delivery_latitude": 49.9423,
    "delivery_longitude": -119.3960
}
@pytest.mark.parametrize("valid_postal_code", [
    "V1V 1V1",  # Valid with space
    "V1V-1V1",  # Valid with hyphen
    "V1V1V1"    # Valid with no space or hyphen
])
def test_create_order_valid_postal_codes(valid_postal_code):
    """ Equivalence Partitioning Test:
    Test that creating an Order with valid postal codes succeeds.
    Valid values:
    - "V1V 1V1" (valid with space)
    - "V1V-1V1" (valid with hyphen)
    - "V1V1V1" (valid with no space or hyphen)
    """
    order = OrderCreate(**postal_base_data, delivery_postal_code=valid_postal_code)
    assert order.delivery_postal_code == valid_postal_code

@pytest.mark.parametrize("invalid_postal_code", [
    "11V 1V1",  # Invalid: first character not a letter
    "VAV 1V1",  # Invalid: second character not a number
    "V11 1V1",  # Invalid: third character not a letter
    "V1V_1V1",  # Invalid: fourth character is not space or hyphen
    "V1V AV1",  # Invalid: fifth character not a number
    "V1V 11V",  # Invalid: sixth character not a letter
    "V1V 1VA",  # Invalid: seventh character not a number
    "V1V 1V1V", # Invalid: extra character at the end
    "V1 1V1",   # Invalid: missing character (only 6 characters instead of 7)
])
def test_create_order_invalid_postal_codes(invalid_postal_code):
    """ Equivalence Partitioning Test:
    Test that creating an Order with invalid postal codes raises a ValidationError.
    Invalid values:
    - "11V 1V1" (first character not a letter)
    - "VAV 1V1" (second character not a number)
    - "V11 1V1" (third character not a letter)
    - "V1V_1V1" (fourth character is not space or hyphen)
    - "V1V AV1" (fifth character not a number)
    - "V1V 11V" (sixth character not a letter)
    - "V1V 1VA" (seventh character not a number)
    - "V1V 1V1V" (extra character at the end)
    - "V1 1V1" (missing character)
    """
    with pytest.raises(ValidationError):
        OrderCreate(**postal_base_data, delivery_postal_code=invalid_postal_code)

def test_update_order_success():
    """Test that updating an Order with valid data succeeds."""
    old_order = OrderCreate(
        customer_id="testcustomer123",
        restaurant_id=1,
        items=[OrderItemCreate(menu_item_id=1, quantity=2)],
        delivery_latitude=49.9423,
        delivery_longitude=-119.3960,
        delivery_postal_code="V1V 1V7"
    )
    update_data = OrderUpdate(
        delivery_postal_code="V1V 1V8"
    )
    assert update_data.delivery_postal_code == "V1V 1V8"

def test_update_order_catches_invalid_data():
    """Proves that the validators in OrderUpdate are attached.
    The exact logic isn't tested here, since the tests for OrderCreate already cover that.
    Because of this, we only do one "invalid" test for each field."""
    
    # Test invalid postal code
    with pytest.raises(ValidationError):
        OrderUpdate(
            delivery_postal_code="11V 1V1"
        )
    # Test invalid latitude
    with pytest.raises(ValidationError):
        OrderUpdate(
            delivery_latitude=90.1
        )
    # Test invalid longitude
    with pytest.raises(ValidationError):
        OrderUpdate(
            delivery_longitude=-180.1
        )