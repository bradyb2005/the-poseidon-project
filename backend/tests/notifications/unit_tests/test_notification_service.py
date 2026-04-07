from unittest.mock import MagicMock

from backend.services.notifications_services import NotificationService


def test_create_notification_success():
    repo = MagicMock()
    repo.load_all.return_value = []

    service = NotificationService(repo)
    notification = service.create_notification("1", "payment_status", "Payment successful")

    assert notification["id"] == "1"
    assert notification["user_id"] == "1"
    assert notification["type"] == "payment_status"
    assert notification["message"] == "Payment successful"
    assert notification["enabled"] is True
    assert notification["is_read"] is False
    repo.save_all.assert_called_once()


def test_get_notifications_for_user_returns_only_matching_user():
    repo = MagicMock()
    repo.load_all.return_value = [
        {"id": "1", "user_id": "1", "type": "payment_status", "message": "A", "enabled": True, "is_read": False},
        {"id": "2", "user_id": "2", "type": "order_status", "message": "B", "enabled": True, "is_read": False},
        {"id": "3", "user_id": "1", "type": "new_review", "message": "C", "enabled": True, "is_read": False},
    ]

    service = NotificationService(repo)
    notifications = service.get_notifications_for_user("1")

    assert len(notifications) == 2
    assert all(n["user_id"] == "1" for n in notifications)


def test_notify_order_status_change_creates_notification():
    repo = MagicMock()
    repo.load_all.return_value = []

    service = NotificationService(repo)
    notification = service.notify_order_status_change("1", "ORD-001", "delivered")

    assert notification["user_id"] == "1"
    assert notification["type"] == "order_status"
    assert notification["message"] == "Order ORD-001 status updated to: delivered"


def test_notify_payment_status_success_creates_notification():
    repo = MagicMock()
    repo.load_all.return_value = []

    service = NotificationService(repo)
    notification = service.notify_payment_status("1", "ORD-001", True)

    assert notification["type"] == "payment_status"
    assert notification["message"] == "Payment successful for order ORD-001"


def test_notify_payment_status_failure_creates_notification():
    repo = MagicMock()
    repo.load_all.return_value = []

    service = NotificationService(repo)
    notification = service.notify_payment_status("1", "ORD-001", False)

    assert notification["type"] == "payment_status"
    assert notification["message"] == "Payment failed for order ORD-001"


def test_notify_restaurant_new_order_creates_notification():
    repo = MagicMock()
    repo.load_all.return_value = []

    service = NotificationService(repo)
    notification = service.notify_restaurant_new_order("owner-1", "ORD-001")

    assert notification["user_id"] == "owner-1"
    assert notification["type"] == "new_order"
    assert notification["message"] == "New paid order received: ORD-001"


def test_notify_admin_flagged_review_creates_notification():
    repo = MagicMock()
    repo.load_all.return_value = []

    service = NotificationService(repo)
    notification = service.notify_admin_flagged_review("admin-1", "REV-001")

    assert notification["user_id"] == "admin-1"
    assert notification["type"] == "flagged_review"
    assert notification["message"] == "Review REV-001 has been flagged for admin review"


def test_notify_restaurant_new_review_creates_notification():
    repo = MagicMock()
    repo.load_all.return_value = []

    service = NotificationService(repo)
    notification = service.notify_restaurant_new_review("owner-1", "REV-001")

    assert notification["user_id"] == "owner-1"
    assert notification["type"] == "new_review"
    assert notification["message"] == "New review submitted: REV-001"


def test_set_notification_enabled_updates_existing_type():
    repo = MagicMock()
    repo.load_all.return_value = [
        {"id": "1", "user_id": "1", "type": "payment_status", "message": "old", "enabled": True, "is_read": False}
    ]

    service = NotificationService(repo)
    result = service.set_notification_enabled("1", "payment_status", False)

    assert result["user_id"] == "1"
    assert result["type"] == "payment_status"
    assert result["enabled"] is False
    repo.save_all.assert_called_once()


def test_disabled_notification_type_prevents_creation():
    repo = MagicMock()
    repo.load_all.return_value = [
        {"id": "1", "user_id": "1", "type": "payment_status", "message": "pref", "enabled": False, "is_read": False}
    ]

    service = NotificationService(repo)
    notification = service.notify_payment_status("1", "ORD-001", True)

    assert notification is None