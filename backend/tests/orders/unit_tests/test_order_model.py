# python3 -m pytest backend/tests/orders/unit_tests/test_order_model.py

import pytest
from datetime import datetime
from unittest.mock import Mock

# Importing from only the Order file
from backend.models.orders.order_model import (
    Order, 
    Customer, 
    Restaurant, 
    OrderItem, 
    OrderStatus,
    DeliveryInfo
)


# --- FIXTURES ---

@pytest.fixture
def mock_customer():
    return Mock(spec=Customer)

@pytest.fixture
def mock_restaurant():
    return Mock(spec=Restaurant)

@pytest.fixture
def mock_order_item():
    return Mock(spec=OrderItem)

@pytest.fixture
def mock_order_status():
    return Mock(spec=OrderStatus)

@pytest.fixture
def mock_delivery_info():
    return Mock(spec=DeliveryInfo)

@pytest.fixture
def valid_order_data(mock_customer, mock_restaurant, mock_order_item, mock_order_status, mock_delivery_info):
    """Provides a valid dictionary of kwargs to successfully create an Order."""
    return {
        "id": 101,
        "customer": mock_customer,
        "restaurant": mock_restaurant,
        "items": [mock_order_item, mock_order_item],
        "status": mock_order_status,
        "order_date": datetime.now(),
        "subtotal": 25.50,
        "total_price": 32.00,
        "delivery_info": mock_delivery_info
    }


# --- TESTS ---

def test_order_creation_success(valid_order_data):
    """Test that a valid order is created without raising any exceptions."""
    order = Order(**valid_order_data)
    
    assert order.id == 101
    assert order.subtotal == 25.50
    assert order.total_price == 32.00
    assert len(order.items) == 2
    assert isinstance(order.order_date, datetime)

def test_update_status(valid_order_data):
    """Test that the update_status method successfully changes the status."""
    order = Order(**valid_order_data)
    
    # Create a new mock status to transition to
    new_status = Mock(spec=OrderStatus)
    order.update_status(new_status)
    
    assert order.status == new_status

def test_invalid_id_raises_error(valid_order_data):
    """Test that a negative ID triggers a ValueError."""
    valid_order_data["id"] = -5
    
    with pytest.raises(ValueError, match="id must be a non-negative integer"):
        Order(**valid_order_data)

def test_invalid_id_type_raises_error(valid_order_data):
    """Test that a string passed as ID triggers a ValueError."""
    valid_order_data["id"] = "101"
    
    with pytest.raises(ValueError, match="id must be a non-negative integer"):
        Order(**valid_order_data)

def test_invalid_subtotal_raises_error(valid_order_data):
    """Test that a negative subtotal triggers a ValueError."""
    valid_order_data["subtotal"] = -10.00
    
    with pytest.raises(ValueError, match="subtotal must be a non-negative number"):
        Order(**valid_order_data)

def test_invalid_total_price_raises_error(valid_order_data):
    """Test that a negative total price triggers a ValueError."""
    valid_order_data["total_price"] = -5.00
    
    with pytest.raises(ValueError, match="total_price must be a non-negative number"):
        Order(**valid_order_data)

def test_invalid_customer_type_raises_error(valid_order_data):
    """Test that passing a non-Customer object triggers a ValueError."""
    valid_order_data["customer"] = "Not a customer object"
    
    with pytest.raises(ValueError, match="customer must be a Customer object"):
        Order(**valid_order_data)

def test_invalid_items_list_raises_error(valid_order_data):
    """Test that a list containing non-OrderItem objects triggers a ValueError."""
    valid_order_data["items"] = ["item1", "item2"] # Strings instead of OrderItem mocks
    
    with pytest.raises(ValueError, match="items must be a list of OrderItem objects"):
        Order(**valid_order_data)

def test_invalid_restaurant_type_raises_error(valid_order_data):
    """Test that passing a non-Restaurant object triggers a ValueError."""
    valid_order_data["restaurant"] = "Not a restaurant"
    
    with pytest.raises(ValueError, match="restaurant must be a Restaurant object"):
        Order(**valid_order_data)

def test_invalid_status_type_raises_error(valid_order_data):
    """Test that passing a non-OrderStatus object triggers a ValueError."""
    valid_order_data["status"] = "Pending" # String instead of OrderStatus mock
    
    with pytest.raises(ValueError, match="status must be an OrderStatus object"):
        Order(**valid_order_data)

def test_invalid_order_date_type_raises_error(valid_order_data):
    """Test that passing a non-datetime object triggers a ValueError."""
    valid_order_data["order_date"] = "2026-03-17" # String instead of datetime object
    
    with pytest.raises(ValueError, match="order_date must be a datetime object"):
        Order(**valid_order_data)

def test_invalid_delivery_info_type_raises_error(valid_order_data):
    """Test that passing a non-DeliveryInfo object triggers a ValueError."""
    valid_order_data["delivery_info"] = {"address": "123 University Way"} # Dict instead of DeliveryInfo mock
    
    with pytest.raises(ValueError, match="delivery_info must be a DeliveryInfo object"):
        Order(**valid_order_data)