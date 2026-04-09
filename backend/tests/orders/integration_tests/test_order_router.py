# backend/tests/orders/integration_tests/test_order_router.py
import pytest
from backend.main import app
from backend.routes.order_router import get_order_service

@pytest.fixture
def mock_order_service(client):
    """
    Injects the mock service into the FastAPI dependency system
    """
    from unittest.mock import MagicMock
    mock = MagicMock()
    
    app.dependency_overrides[get_order_service] = lambda: mock
    
    yield mock

    app.dependency_overrides = {}

# --- POST tests ---

def test_post_create_order_success(client, mock_order_service, valid_uuids):
    """
    Equivalence Partitioning
    Ensures an order can be created successfully
    """
    mock_order = {
        "id": valid_uuids["item_1"], 
        "customer_id": "user_1", 
        "restaurant_id": 1,
        "items": [], 
        "status": "unpaid", 
        "order_date": "2026-04-08T12:00:00",
        "delivery_latitude": 49.88, 
        "delivery_longitude": -119.49,
        "delivery_postal_code": "V1V 1V1", 
        "cost_breakdown": {
            "_subtotal": 10.0, "_delivery_fee": 5.0, "_service_fee": 1.0, "_tax": 0.80, "_total": 16.80
        }
    }
    mock_order_service.create_order.return_value = mock_order

    payload = {
        "customer_id": "user_1",
        "restaurant_id": 1,
        "items": [],
        "delivery_latitude": 49.88,
        "delivery_longitude": -119.49,
        "delivery_postal_code": "V1V 1V1"
    }
    response = client.post("/orders", json=payload)

    assert response.status_code == 201
    assert response.json()["id"] == valid_uuids["item_1"]

# --- PUT tests ---

def test_put_update_order_success(client, mock_order_service, valid_uuids):
    """
    Equivalence Partitioning
    Ensures an order can be updated successfully
    """
    mock_order = {
        "id": valid_uuids["item_1"], 
        "customer_id": "user_1", 
        "restaurant_id": 1,
        "items": [], 
        "status": "completed", 
        "order_date": "2026-04-08T12:00:00",
        "delivery_latitude": 49.88, 
        "delivery_longitude": -119.49,
        "delivery_postal_code": "V1V 1V1", 
        "cost_breakdown": {
            "_subtotal": 10.0, "_delivery_fee": 5.0, "_service_fee": 1.0, "_tax": 0.80, "_total": 16.80
        }
    }
    mock_order_service.update_order.return_value = mock_order

    payload = {"status": "completed"}
    response = client.put(f"/orders/{valid_uuids['item_1']}", json=payload)

    assert response.status_code == 200
    assert response.json()["status"] == "completed"

    # --- GET tests ---

def test_get_order_by_id_success(client, mock_order_service, valid_uuids):
    """Ensures a specific order can be retrieved by ID."""
    order_id = valid_uuids["item_1"]
    mock_order = {
        "id": order_id, 
        "customer_id": "user_1", 
        "restaurant_id": 1,
        "items": [], 
        "status": "unpaid", 
        "order_date": "2026-04-08T12:00:00",
        "delivery_latitude": 49.88, 
        "delivery_longitude": -119.49,
        "delivery_postal_code": "V1V 1V1", 
        "cost_breakdown": {
            "_subtotal": 10.0, "_delivery_fee": 5.0, "_service_fee": 1.0, "_tax": 0.80, "_total": 16.80
        }
    }
    # Tell the mock service what to return when called
    mock_order_service.get_order_by_id.return_value = mock_order

    response = client.get(f"/orders/{order_id}")

    assert response.status_code == 200
    assert response.json()["id"] == order_id
    mock_order_service.get_order_by_id.assert_called_once_with(order_id)

def test_get_user_orders_success(client, mock_order_service):
    """Ensures all orders for a specific user can be retrieved."""
    customer_id = "user_1"
    mock_orders = [
        {
            "id": "order_A", "customer_id": customer_id, "restaurant_id": 1,
            "items": [], "status": "completed", "order_date": "2026-04-08T10:00:00",
            "delivery_latitude": 49.8, "delivery_longitude": -119.4, "delivery_postal_code": "V1V 1V1",
            "cost_breakdown": {"_subtotal": 10.0, "_delivery_fee": 5.0, "_service_fee": 1.0, "_tax": 0.80, "_total": 16.80}
        },
        {
            "id": "order_B", "customer_id": customer_id, "restaurant_id": 2,
            "items": [], "status": "unpaid", "order_date": "2026-04-08T11:00:00",
            "delivery_latitude": 49.8, "delivery_longitude": -119.4, "delivery_postal_code": "V1V 1V1",
            "cost_breakdown": {"_subtotal": 20.0, "_delivery_fee": 5.0, "_service_fee": 1.0, "_tax": 1.60, "_total": 27.60}
        }
    ]
    # Tell the mock service to return a list
    mock_order_service.get_orders_by_customer.return_value = mock_orders

    response = client.get(f"/orders/user/{customer_id}")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["id"] == "order_A"
    mock_order_service.get_orders_by_customer.assert_called_once_with(customer_id)