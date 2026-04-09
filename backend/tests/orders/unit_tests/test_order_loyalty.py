# backend/tests/orders/unit_tests/test_order_loyalty.py
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from uuid import uuid4
from backend.services.order_service import OrderService
from backend.schemas.order_schema import OrderCreate, OrderUpdate, OrderStatus
from backend.schemas.loyalty_schema import LoyaltyTier

@pytest.fixture
def mock_repos():
    return {
        "order": MagicMock(),
        "user": MagicMock(),
        "item": MagicMock(),
        "restaurant": MagicMock()
    }

@pytest.fixture
def order_service(mock_repos):
    return OrderService(
        order_repository=mock_repos["order"],
        user_repository=mock_repos["user"],
        items_repository=mock_repos["item"],
        restaurant_repository=mock_repos["restaurant"]
    )

# --- Integration: Order Creation ---

@patch("backend.services.order_service.PaymentService")
def test_create_order_stores_loyalty_attribute(mock_payment_class, order_service, mock_repos):
    item_id = str(uuid4())
    mock_repos["user"].find_by_id.return_value = {
        "id": "user_123",
        "loyalty_tier": LoyaltyTier.BRONZE.value,
        "cart": {"items": [{"menu_item_id": item_id, "price_at_time": 10.0, "quantity": 2}]}
    }
    mock_payment = mock_payment_class.return_value
    mock_payment.calculate_subtotal.return_value = 20.0
    mock_payment.calculate_fees_and_taxes.return_value = {"delivery_fee": 5.0, "service_fee": 2.0, "tax": 1.0}
    mock_payment.calculate_total.return_value = MagicMock(total=28.0)
    
    mock_repos["item"].find_by_id.return_value = MagicMock(restaurant_id=1)
    mock_repos["restaurant"].find_by_id.return_value = {"is_published": True}
    mock_repos["order"].find_by_id.return_value = None
    mock_repos["order"].load_all.return_value = []

    payload = OrderCreate(
        customer_id="user_123",
        restaurant_id=1,
        delivery_latitude=49.9,
        delivery_longitude=-119.4,
        delivery_postal_code="V1V 1V1"
    )

    order = order_service.create_order(payload)
    assert order.loyalty_points_earned == 200

# --- Integration: Order Updates ---

def test_update_order_to_completed_finalizes_points(order_service, mock_repos):
    order_id = "ORD_PAYOUT"
    item_id = str(uuid4())
    mock_repos["order"].find_by_id.return_value = {
        "id": order_id,
        "customer_id": "user_123",
        "restaurant_id": 1,
        "items": [{"menu_item_id": item_id, "price_at_time": 50.0, "quantity": 1}],
        "status": OrderStatus.UNPAID,
        "order_date": datetime.now(),
        "delivery_latitude": 49.9,
        "delivery_longitude": -119.4,
        "delivery_postal_code": "V1V 1V1",
        "cost_breakdown": {
            "subtotal": 50.0, "_subtotal": 50.0,
            "delivery_fee": 5.0, "_delivery_fee": 5.0,
            "service_fee": 2.0, "_service_fee": 2.0,
            "tax": 1.0, "_tax": 1.0,
            "total": 58.0, "_total": 58.0
        },
        "loyalty_points_earned": 500
    }
    mock_repos["order"].load_all.return_value = []
    mock_repos["user"].load_all.return_value = [{"id": "user_123", "loyalty_points": 0, "loyalty_tier": "Bronze"}]

    order_service.update_order(order_id, OrderUpdate(status=OrderStatus.COMPLETED))
    
    updated_user = mock_repos["user"].save_all.call_args[0][0][0]
    assert updated_user["loyalty_points"] == 500
    assert updated_user["loyalty_tier"] == LoyaltyTier.SILVER.value

def test_update_order_to_cancelled_no_points(order_service, mock_repos):
    order_id = "ORD_CANCEL"
    item_id = str(uuid4())
    mock_repos["order"].find_by_id.return_value = {
        "id": order_id,
        "customer_id": "user_123",
        "restaurant_id": 1,
        "items": [{"menu_item_id": item_id, "price_at_time": 50.0, "quantity": 1}],
        "status": OrderStatus.UNPAID,
        "order_date": datetime.now(),
        "delivery_latitude": 49.9,
        "delivery_longitude": -119.4,
        "delivery_postal_code": "V1V 1V1",
        "cost_breakdown": {
            "subtotal": 50.0, "_subtotal": 50.0,
            "delivery_fee": 5.0, "_delivery_fee": 5.0,
            "service_fee": 2.0, "_service_fee": 2.0,
            "tax": 1.0, "_tax": 1.0,
            "total": 58.0, "_total": 58.0
        },
        "loyalty_points_earned": 500
    }
    mock_repos["order"].load_all.return_value = []
    users_list = [{"id": "user_123", "loyalty_points": 0, "loyalty_tier": "Bronze"}]
    mock_repos["user"].load_all.return_value = users_list

    order_service.update_order(order_id, OrderUpdate(status=OrderStatus.CANCELLED))

    assert users_list[0]["loyalty_points"] == 0
    mock_repos["user"].save_all.assert_not_called()