from backend.repositories.notifications_repository import NotificationRepository


class NotificationService:
    """Service layer for notification logic."""

    def __init__(self, notification_repo: NotificationRepository):
        self.notification_repo = notification_repo

    def create_notification(self, user_id: str, notification_type: str, message: str) -> dict:
        """Create and store a notification."""
        notifications = self.notification_repo.load_all()

        new_id = str(len(notifications) + 1)
        notification = {
            "id": new_id,
            "user_id": user_id,
            "type": notification_type,
            "message": message,
            "enabled": True,
            "is_read": False,
        }

        notifications.append(notification)
        self.notification_repo.save_all(notifications)
        return notification

    def get_notifications_for_user(self, user_id: str) -> list[dict]:
        """Return all notifications for one user."""
        notifications = self.notification_repo.load_all()
        return [n for n in notifications if n["user_id"] == user_id]

    def set_notification_enabled(self, user_id: str, notification_type: str, enabled: bool) -> dict:
        """Enable or disable a notification type for a user."""
        notifications = self.notification_repo.load_all()

        preference_found = False
        for notification in notifications:
            if notification["user_id"] == user_id and notification["type"] == notification_type:
                notification["enabled"] = enabled
                preference_found = True

        if not preference_found:
            new_id = str(len(notifications) + 1)
            notifications.append({
                "id": new_id,
                "user_id": user_id,
                "type": notification_type,
                "message": f"{notification_type} notifications preference updated",
                "enabled": enabled,
                "is_read": False,
            })

        self.notification_repo.save_all(notifications)

        return {
            "user_id": user_id,
            "type": notification_type,
            "enabled": enabled,
        }

    def _is_notification_type_enabled(self, user_id: str, notification_type: str) -> bool:
        """Check if a notification type is enabled for a user."""
        notifications = self.notification_repo.load_all()

        matching = [
            n for n in notifications
            if n["user_id"] == user_id and n["type"] == notification_type
        ]

        if not matching:
            return True

        return matching[-1].get("enabled", True)

    def notify_order_status_change(self, user_id: str, order_id: str, status: str) -> dict | None:
        """Notify customer when an order status changes."""
        notification_type = "order_status"

        if not self._is_notification_type_enabled(user_id, notification_type):
            return None

        message = f"Order {order_id} status updated to: {status}"
        return self.create_notification(user_id, notification_type, message)

    def notify_payment_status(self, user_id: str, order_id: str, success: bool) -> dict | None:
        """Notify customer when payment succeeds or fails."""
        notification_type = "payment_status"

        if not self._is_notification_type_enabled(user_id, notification_type):
            return None

        if success:
            message = f"Payment successful for order {order_id}"
        else:
            message = f"Payment failed for order {order_id}"

        return self.create_notification(user_id, notification_type, message)

    def notify_restaurant_new_order(self, owner_id: str, order_id: str) -> dict | None:
        """Notify restaurant owner when a new paid order is received."""
        notification_type = "new_order"

        if not self._is_notification_type_enabled(owner_id, notification_type):
            return None

        message = f"New paid order received: {order_id}"
        return self.create_notification(owner_id, notification_type, message)

    def notify_admin_flagged_review(self, admin_id: str, review_id: str) -> dict | None:
        """Notify admin when a review is flagged."""
        notification_type = "flagged_review"

        if not self._is_notification_type_enabled(admin_id, notification_type):
            return None

        message = f"Review {review_id} has been flagged for admin review"
        return self.create_notification(admin_id, notification_type, message)

    def notify_restaurant_new_review(self, owner_id: str, review_id: str) -> dict | None:
        """Notify restaurant owner when a new review is submitted."""
        notification_type = "new_review"

        if not self._is_notification_type_enabled(owner_id, notification_type):
            return None

        message = f"New review submitted: {review_id}"
        return self.create_notification(owner_id, notification_type, message)
    