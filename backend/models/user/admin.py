from __future__ import annotations

from typing import Any, Dict, List, Optional

from backend.models.user.user_model import User


class Admin(User):
    # Inherit info from User

    # -------------------------
    # Admin "Administrator" page
    # -------------------------
    def get_admin_dashboard(self) -> Dict[str, Any]:
        return {"message": "Admin dashboard placeholder"}

    # -------------------------
    # Credentials
    # -------------------------
    def modify_credentials(
        self,
        user: User,
        new_username: Optional[str] = None,
        new_password: Optional[str] = None,
    ) -> None:
        if new_username is not None:
            user.username = new_username
        if new_password is not None:
            user.password_hash = User.hash_password(new_password)

    # -------------------------
    # Orders / verification
    # -------------------------
    def generate_order_list(self) -> List["Order"]:
        return []

    def access_submitted_order_records(self) -> List["Order"]:
        return []

    def view_active_order_quantities(self) -> Dict[Any, int]:
        return {}

    def view_subtotal_for_verification(self, order: "Order") -> float:
        return float(getattr(order, "subtotal", 0.0))

    def verify_fees_and_taxes_applied_consistently(self, order: "Order") -> bool:
        return True

    def store_final_total_with_order_record(self, order: "Order", total: float) -> None:
        setattr(order, "total", float(total))

    # -------------------------
    # Delivery information access
    # -------------------------
    def access_delivery_information(self, order: "Order") -> Optional[Any]:
        return getattr(order, "delivery_info", None)

    def access_delivery_information_for_complaints(self, order: "Order") -> Optional[Any]:
        return getattr(order, "delivery_info", None)

    def verify_delivery_information_format(self, delivery_info: Any) -> bool:
        return delivery_info is not None

    # -------------------------
    # Menu availability / edits
    # -------------------------
    def manage_menu_availability(self, item: "MenuItem", available: bool) -> None:
        if hasattr(item, "availability"):
            item.availability = available
        else:
            setattr(item, "availability", available)

    def add_menu_item(self, restaurant: "Restaurant", item: "MenuItem") -> None:
        if not hasattr(restaurant, "menu") or restaurant.menu is None:
            restaurant.menu = []
        restaurant.menu.append(item)

    def edit_menu_item(
        self,
        item: "MenuItem",
        name: Optional[str] = None,
        description: Optional[str] = None,
        price: Optional[float] = None,
        category: Optional[str] = None,
        available: Optional[bool] = None,
    ) -> None:
        if name is not None:
            item.name = name
        if description is not None:
            item.description = description
        if price is not None:
            if price < 0:
                raise ValueError("Price cannot be negative")
            item.price = float(price)
        if category is not None:
            item.category = category
        if available is not None:
            self.manage_menu_availability(item, available)

    # -------------------------
    # Popular restaurants
    # -------------------------
    def generate_most_popular_restaurants(self) -> List["Restaurant"]:
        return []

    # -------------------------
    # Reviews
    # -------------------------
    def view_ratings_and_reviews_for_monitoring(self) -> List["Review"]:
        return []

    def list_flagged_reviews(self) -> List["Review"]:
        return []

    def moderate_flagged_review(self, review: "Review", action: str) -> None:
        setattr(review, "moderation_action", action)

    def send_flagged_review_notifications(self) -> None:
        return

    # -------------------------
    # Pagination helper
    # -------------------------
    def list_paginated_results(self, items: List[Any], page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 10
        start = (page - 1) * page_size
        end = start + page_size
        return {
            "page": page,
            "page_size": page_size,
            "total": len(items),
            "results": items[start:end],
        }
