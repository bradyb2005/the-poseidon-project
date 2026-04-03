# backend/tests/orders/unit_tests/test_order_schema.py
import pytest
from pydantic import ValidationError
from backend.schemas.order_schema import OrderCreate, OrderUpdate, OrderStatus

# --- Order Schema Tests ---

def test_order_create_success():
    """Tests that a full valid payload creates an OrderCreate object."""
    payload = {
        "customer_id": "user_55",
        "restaurant_id": 10,
        "items": [{"menu_item_id": "11111111-1111-1111-1111-111111111111", "quantity": 1, "price_at_time": 9.99}],
        "delivery_latitude": 49.88,
        "delivery_longitude": -119.49,
        "delivery_postal_code": "V1V 1V1"
    }
    order = OrderCreate(**payload)
    assert order.customer_id == "user_55"
    assert len(order.items) == 1

def test_order_create_missing_coordinates():
    """Tests that missing attributes raise a ValidationError."""
    with pytest.raises(ValidationError):
        OrderCreate(
            customer_id="test_customer",
            restaurant_id=10,
            items=[{"menu_item_id": 1, "quantity": 1}],
            delivery_postal_code="V1V 1V1"
            # Missing lat/long
        )

def test_order_update_valid_status():
    """Tests that updating the status with a valid Enum value works."""
    update = OrderUpdate(status=OrderStatus.IN_PROGRESS)
    assert update.status == "in_progress"

def test_order_update_invalid_status_string():
    """Tests that a random string not in the Enum fails."""
    with pytest.raises(ValidationError):
        OrderUpdate(status="on_the_way")

def test_order_update_partial_fields():
    """Tests that OrderUpdate only modifies specified fields."""
    update = OrderUpdate(delivery_instructions="Leave at the side door")
    assert update.delivery_instructions == "Leave at the side door"
    assert update.status is None  # Verify other fields remain optional