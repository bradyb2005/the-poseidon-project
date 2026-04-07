# backend/services/admin_service.py

from backend.repositories.user_repository import UserRepository
from backend.repositories.notifications_repository import NotificationRepository


class AdminService:
    """Service layer for admin-only business logic."""

    def __init__(self, user_repo: UserRepository,
                 notification_repo: NotificationRepository):
        self.user_repo = user_repo
        self.notification_repo = notification_repo

    # ── Users ────────────────────────────────────────────────

    def get_all_users(
        self,
        role: str = None,
        is_suspended: bool = None,
        search: str = None,
        sort_by: str = "username",
        sort_order: str = "asc",
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """Return a filtered, sorted, paginated list of users."""
        users = self.user_repo.load_all()

        if role:
            users = [u for u in users if u.get("role") == role]

        if is_suspended is not None:
            users = [u for u in users
                     if u.get("is_suspended", False) == is_suspended]

        if search:
            q = search.lower()
            users = [
                u for u in users
                if q in u.get("username", "").lower()
                or q in u.get("email", "").lower()
            ]

        reverse = sort_order == "desc"
        users.sort(key=lambda u: str(u.get(sort_by, "")), reverse=reverse)

        total = len(users)
        start = (page - 1) * page_size
        end = start + page_size

        return {
            "users": users[start:end],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(1, -(-total // page_size)),
        }

    def get_user_by_id(self, user_id: str) -> dict:
        """Return a single user by ID."""
        users = self.user_repo.load_all()
        for user in users:
            if user["id"] == user_id:
                return user
        raise ValueError(f"User {user_id} not found")

    def suspend_user(self, user_id: str) -> dict:
        """Suspend a user account (admin action)."""
        users = self.user_repo.load_all()
        for user in users:
            if user["id"] == user_id:
                if user.get("role") == "admin":
                    raise ValueError("Cannot suspend an admin account")
                user["is_suspended"] = True
                self.user_repo.save_all(users)
                return user
        raise ValueError(f"User {user_id} not found")

    def unsuspend_user(self, user_id: str) -> dict:
        """Unsuspend a user account (admin action)."""
        users = self.user_repo.load_all()
        for user in users:
            if user["id"] == user_id:
                user["is_suspended"] = False
                self.user_repo.save_all(users)
                return user
        raise ValueError(f"User {user_id} not found")

    def update_user(self, user_id: str, updates: dict) -> dict:
        """Update allowed fields on a user record."""
        allowed_fields = {"username", "email", "role", "phone", "address"}
        users = self.user_repo.load_all()
        for user in users:
            if user["id"] == user_id:
                for key, value in updates.items():
                    if key in allowed_fields:
                        user[key] = value
                self.user_repo.save_all(users)
                return user
        raise ValueError(f"User {user_id} not found")

    def delete_user(self, user_id: str) -> dict:
        """Delete a user record entirely."""
        users = self.user_repo.load_all()
        for user in users:
            if user["id"] == user_id:
                users.remove(user)
                self.user_repo.save_all(users)
                return {"deleted": True, "user_id": user_id}
        raise ValueError(f"User {user_id} not found")

    # ── Orders ───────────────────────────────────────────────

    def get_all_orders(
        self,
        status: str = None,
        restaurant_id: int = None,
        customer_id: str = None,
        date_from: str = None,
        date_to: str = None,
        min_value: float = None,
        max_value: float = None,
        sort_by: str = "order_time",
        sort_order: str = "desc",
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """Return filtered, sorted, paginated orders."""
        import json, os
        orders_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "orders.json"
        )
        with open(orders_path, "r", encoding="utf-8") as f:
            orders = json.load(f)

        if status:
            orders = [o for o in orders if o.get("status") == status]

        if restaurant_id is not None:
            orders = [o for o in orders
                      if o.get("restaurant_id") == restaurant_id]

        if customer_id:
            orders = [o for o in orders
                      if o.get("customer_id") == customer_id]

        if date_from:
            orders = [o for o in orders
                      if o.get("order_time", "") >= date_from]

        if date_to:
            orders = [o for o in orders
                      if o.get("order_time", "") <= date_to]

        if min_value is not None:
            orders = [o for o in orders
                      if float(o.get("order_value", 0)) >= min_value]

        if max_value is not None:
            orders = [o for o in orders
                      if float(o.get("order_value", 0)) <= max_value]

        reverse = sort_order == "desc"
        try:
            orders.sort(
                key=lambda o: o.get(sort_by, ""),
                reverse=reverse
            )
        except TypeError:
            pass

        total = len(orders)
        start = (page - 1) * page_size
        end = start + page_size

        return {
            "orders": orders[start:end],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(1, -(-total // page_size)),
        }

    # ── Analytics ────────────────────────────────────────────

    def get_analytics_summary(self) -> dict:
        """Return aggregated metrics for the admin dashboard."""
        import json, os
        orders_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "orders.json"
        )
        with open(orders_path, "r", encoding="utf-8") as f:
            orders = json.load(f)

        users = self.user_repo.load_all()
        notifications = self.notification_repo.load_all()

        total_revenue = sum(
            float(o.get("order_value", 0)) for o in orders
        )
        avg_order_value = total_revenue / len(orders) if orders else 0

        restaurant_counts: dict = {}
        for order in orders:
            rid = str(order.get("restaurant_id", "unknown"))
            restaurant_counts[rid] = restaurant_counts.get(rid, 0) + 1

        top_restaurants = sorted(
            restaurant_counts.items(), key=lambda x: x[1], reverse=True
        )[:5]

        orders_by_month: dict = {}
        for order in orders:
            month = str(order.get("order_time", ""))[:7]
            if month:
                orders_by_month[month] = orders_by_month.get(month, 0) + 1

        return {
            "total_users": len(users),
            "suspended_users": sum(
                1 for u in users if u.get("is_suspended", False)
            ),
            "total_orders": len(orders),
            "total_revenue": round(total_revenue, 2),
            "avg_order_value": round(avg_order_value, 2),
            "total_notifications": len(notifications),
            "top_restaurants": [
                {"restaurant_id": r, "order_count": c}
                for r, c in top_restaurants
            ],
            "orders_by_month": [
                {"month": m, "count": c}
                for m, c in sorted(orders_by_month.items())
            ],
        }
    
    