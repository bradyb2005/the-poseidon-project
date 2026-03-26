import pytest

from backend.services.notification_service import (
    notify_order_status_change,
    notify_payment_result,
    notify_owner_new_paid_order,
    get_recent_notifications,
)


def test_notify_order_status_change():
    message = notify_order_status_change("123", "Delivered")
    assert message == "Order 123 status updated to Delivered."


def test_notify_payment_result_success():
    message = notify_payment_result("123", True)
    assert message == "Payment for order 123 was successful."


def test_notify_payment_result_failure():
    message = notify_payment_result("123", False)
    assert message == "Payment for order 123 failed."


def test_notify_owner_new_paid_order():
    message = notify_owner_new_paid_order("123")
    assert message == "New paid order received: 123."


def test_get_recent_notifications_default_limit():
    notifications = [
        "n1",
        "n2",
        "n3",
        "n4",
        "n5",
        "n6",
    ]
    result = get_recent_notifications(notifications)
    assert result == ["n2", "n3", "n4", "n5", "n6"]


def test_get_recent_notifications_custom_limit():
    notifications = [
        "n1",
        "n2",
        "n3",
        "n4",
    ]
    result = get_recent_notifications(notifications, limit=2)
    assert result == ["n3", "n4"]

    