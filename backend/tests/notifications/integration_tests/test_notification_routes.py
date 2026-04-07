from unittest.mock import patch
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


@patch("backend.routes.notifications_router.notification_service")
def test_get_notifications_success(mock_notification_service):
    mock_notification_service.get_notifications_for_user.return_value = [
        {
            "id": "1",
            "user_id": "1",
            "type": "payment_status",
            "message": "Payment successful",
            "enabled": True,
            "is_read": False,
        }
    ]

    response = client.get("/notifications/1")

    assert response.status_code == 200
    assert len(response.json()["notifications"]) == 1


@patch("backend.routes.notifications_router.notification_service")
def test_set_notification_preference_success(mock_notification_service):
    mock_notification_service.set_notification_enabled.return_value = {
        "user_id": "1",
        "type": "payment_status",
        "enabled": False,
    }

    response = client.put(
        "/notifications/preferences",
        json={
            "user_id": "1",
            "notification_type": "payment_status",
            "enabled": False,
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "notification preference updated"
    assert response.json()["preference"]["enabled"] is False


@patch("backend.routes.notifications_router.notification_service")
def test_trigger_order_status_notification_success(mock_notification_service):
    mock_notification_service.notify_order_status_change.return_value = {
        "id": "1",
        "user_id": "1",
        "type": "order_status",
        "message": "Order ORD-001 status updated to: delivered",
        "enabled": True,
        "is_read": False,
    }

    response = client.post(
        "/notifications/trigger/order-status",
        json={
            "user_id": "1",
            "order_id": "ORD-001",
            "status": "delivered",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "order status notification created"


@patch("backend.routes.notifications_router.notification_service")
def test_trigger_payment_status_notification_success(mock_notification_service):
    mock_notification_service.notify_payment_status.return_value = {
        "id": "1",
        "user_id": "1",
        "type": "payment_status",
        "message": "Payment successful for order ORD-001",
        "enabled": True,
        "is_read": False,
    }

    response = client.post(
        "/notifications/trigger/payment-status",
        json={
            "user_id": "1",
            "order_id": "ORD-001",
            "success": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "payment status notification created"


@patch("backend.routes.notifications_router.notification_service")
def test_trigger_new_order_notification_success(mock_notification_service):
    mock_notification_service.notify_restaurant_new_order.return_value = {
        "id": "1",
        "user_id": "owner-1",
        "type": "new_order",
        "message": "New paid order received: ORD-001",
        "enabled": True,
        "is_read": False,
    }

    response = client.post(
        "/notifications/trigger/new-order",
        json={
            "owner_id": "owner-1",
            "order_id": "ORD-001",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "new order notification created"