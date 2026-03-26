from typing import List, Any


class PaymentService:
    """
    Handles payment-related calculations and processing logic
    """

    def calculate_subtotal(self, order: Any) -> float:
        """
        Calculates subtotal from order items

        Assumes order has:
        - order.items → list of items
        Each item has:
        - price
        - quantity
        """
        self._validate_order(order)

        subtotal = 0.0

        for item in order.items:
            self._validate_item(item)
            subtotal += item.price * item.quantity

        return round(subtotal, 2)

    # -------------------------
    # Private helpers
    # -------------------------

    def _validate_order(self, order: Any) -> None:
        if order is None:
            raise ValueError("order cannot be None")
        if not hasattr(order, "items"):
            raise ValueError("order must have items")

    def _validate_item(self, item: Any) -> None:
        if not hasattr(item, "price") or not hasattr(item, "quantity"):
            raise ValueError("item must have price and quantity")

        if not isinstance(item.price, (int, float)):
            raise ValueError("item price must be a number")

        if not isinstance(item.quantity, int):
            raise ValueError("item quantity must be an integer")

        if item.price < 0:
            raise ValueError("item price cannot be negative")

        if item.quantity <= 0:
            raise ValueError("item quantity must be positive")