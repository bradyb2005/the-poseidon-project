# backend/tests/orders/unit_tests/test_order_service.py
import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from backend.services.order_service import OrderService, OrderValidate
from backend.schemas.order_schema import OrderCreate, OrderStatus, OrderUpdate

# --- Validator Tests ---

@pytest.mark.parametrize("valid_lat", [90.0, -90.0, 49.9423])
def test_validate_latitude_success(valid_lat):
    """Boundary Value Analysis: Valid range [-90, 90]"""
    assert OrderValidate.validate_delivery_latitude(valid_lat) == valid_lat

@pytest.mark.parametrize("invalid_lat", [90.1, -90.1])
def test_validate_latitude_failure(invalid_lat):
    """Boundary Value Analysis: Just outside valid range"""
    with pytest.raises(ValueError, match="Latitude must be between -90 and 90"):
        OrderValidate.validate_delivery_latitude(invalid_lat)

@pytest.mark.parametrize("valid_pc", ["V1V 1V1", "V1V1V1", "v1v 1v1"])
def test_validate_postal_code_success(valid_pc):
    """Equivalence Partitioning: Valid Canadian PC formats"""
    result = OrderValidate.validate_delivery_postal_code(valid_pc)
    # Ensuring it strips and uppers correctly
    assert result == valid_pc.strip().upper()

# --- Order Creation Tests ---

def test_create_order_success(valid_uuids):
    mock_order_repo = MagicMock()
    mock_order_repo.find_by_id.return_value = None
    mock_order_repo.load_all.return_value = [] 
    
    mock_user_repo = MagicMock()
    user_dict = {
        "id": valid_uuids["user_uuid"],
        "cart": {
            "items": [{"menu_item_id": valid_uuids["item_1"], "quantity": 1, "price_at_time": 9.99}]
        }
    }
    mock_user_repo.find_by_id.return_value = user_dict
    mock_user_repo.load_all.return_value = [user_dict]
    
    mock_item = MagicMock()
    mock_item.restaurant_id = 99
    mock_item_repo = MagicMock()
    mock_item_repo.find_by_id.return_value = mock_item 
    
    mock_rest = MagicMock()
    mock_rest.is_published = True
    mock_rest_repo = MagicMock()
    mock_rest_repo.find_by_id.return_value = mock_rest

    service = OrderService(
        order_repository=mock_order_repo,
        user_repository=mock_user_repo,
        items_repository=mock_item_repo,
        restaurant_repository=mock_rest_repo
    )

    payload = OrderCreate(
        customer_id=valid_uuids["user_uuid"],
        restaurant_id=99,
        items=[], 
        delivery_latitude=49.88,
        delivery_longitude=-119.49,
        delivery_postal_code="V1V 1V1",
        delivery_address="1234 University Way",
        delivery_instructions="Leave at door"
    )

    result = service.create_order(payload)

    assert result.customer_id == valid_uuids["user_uuid"]
    assert result.restaurant_id == 99
    assert result.delivery_postal_code == "V1V 1V1"
    
    mock_order_repo.save_all.assert_called_once()
    mock_user_repo.save_all.assert_called_once()


def test_create_order_invalid_data_handling():
    """Ensure HTTPException is raised when validation fails"""
    service = OrderService(MagicMock(), MagicMock(), MagicMock(), MagicMock())
    
    payload = OrderCreate(
        customer_id="brady_123",
        restaurant_id=1, # <-- Changed to int
        items=[],
        delivery_latitude=150.0, 
        delivery_longitude=-119.4,
        delivery_postal_code="V1V 1V1"
    )
    
    with pytest.raises(HTTPException) as exc:
        service.create_order(payload)

    assert exc.value.status_code == 400


# --- Update Order Tests ---

def test_update_order_status_success(valid_uuids):
    """Ensure order status can be updated"""
    mock_repo = MagicMock()
    
    existing_order = {
        "id": valid_uuids["item_3"],
        "customer_id": valid_uuids["user_uuid"],
        "restaurant_id": 1,                 
        "status": OrderStatus.UNPAID,
        "delivery_latitude": 49.8,              
        "delivery_longitude": -119.4,          
        "delivery_postal_code": "V1V 1V1",      
        "order_date": "2026-03-25T12:00:00",    
        "cost_breakdown": {
            "_subtotal": 30.00,
            "_delivery_fee": 5.00,
            "_service_fee": 2.00,
            "_tax": 3.60,
            "_total": 40.60,
        },                    
        "items": []
    }
    mock_repo.find_by_id.return_value = existing_order
    mock_repo.load_all.return_value = [existing_order]
    
    service = OrderService(mock_repo, MagicMock(), MagicMock(), MagicMock())
    
    update_data = OrderUpdate(status=OrderStatus.PENDING)

    result = service.update_order(valid_uuids["item_3"], update_data)

    assert result.status == OrderStatus.PENDING
    mock_repo.save_all.assert_called_once()

def test_update_order_not_found():
    """Test updating an order that doesn't exist"""
    mock_repo = MagicMock()
    mock_repo.find_by_id.return_value = None
    mock_repo.load_all.return_value = []
    
    service = OrderService(mock_repo, MagicMock(), MagicMock(), MagicMock())
    
    update_data = OrderUpdate(status=OrderStatus.PENDING)
    
    with pytest.raises(HTTPException) as exc:
        service.update_order("fake_id", update_data)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Order not found"

def test_update_completed_order_fails(valid_uuids):
    """Ensure a completed order cannot be edited (e.g., changing address)"""
    mock_repo = MagicMock()
    
    existing_order = {
        "id": valid_uuids["item_3"],
        "customer_id": valid_uuids["user_uuid"],
        "restaurant_id": 1,                 
        "status": OrderStatus.COMPLETED, # <-- Order is already completed
        "delivery_latitude": 49.8,              
        "delivery_longitude": -119.4,          
        "delivery_postal_code": "V1V 1V1",      
        "order_date": "2026-03-25T12:00:00",    
        "cost_breakdown": {
            "_subtotal": 30.00,
            "_delivery_fee": 5.00,
            "_service_fee": 2.00,
            "_tax": 3.60,
            "_total": 40.60,
        },                    
        "items": []
    }
    mock_repo.find_by_id.return_value = existing_order
    
    service = OrderService(mock_repo, MagicMock(), MagicMock(), MagicMock())
    
    # Try to change the postal code
    update_data = OrderUpdate(delivery_postal_code="V2V 2V2")

    with pytest.raises(HTTPException) as exc:
        service.update_order(valid_uuids["item_3"], update_data)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Cannot update a completed or cancelled order"


def test_update_cancelled_order_fails(valid_uuids):
    """Ensure a cancelled order cannot be marked as complete"""
    mock_repo = MagicMock()
    
    existing_order = {
        "id": valid_uuids["item_3"],
        "customer_id": valid_uuids["user_uuid"],
        "restaurant_id": 1,                 
        "status": OrderStatus.CANCELLED, # <-- Order is already cancelled
        "delivery_latitude": 49.8,              
        "delivery_longitude": -119.4,          
        "delivery_postal_code": "V1V 1V1",      
        "order_date": "2026-03-25T12:00:00",    
        "cost_breakdown": {
            "_subtotal": 30.00,
            "_delivery_fee": 5.00,
            "_service_fee": 2.00,
            "_tax": 3.60,
            "_total": 40.60,
        },                    
        "items": []
    }
    mock_repo.find_by_id.return_value = existing_order
    
    service = OrderService(mock_repo, MagicMock(), MagicMock(), MagicMock())
    
    # Try to mark it as completed
    update_data = OrderUpdate(status=OrderStatus.COMPLETED)

    with pytest.raises(HTTPException) as exc:
        service.update_order(valid_uuids["item_3"], update_data)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Cannot update a completed or cancelled order"