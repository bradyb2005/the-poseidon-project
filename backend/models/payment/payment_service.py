from typing import Any


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

    def calculate_fees_and_taxes(self, subtotal: float) -> dict:
        """
        Calculates delivery fee, service fee, and tax based on subtotal
        """
        self._validate_subtotal(subtotal)

        delivery_fee = self._calculate_delivery_fee(subtotal)
        service_fee = self._calculate_service_fee(subtotal)
        tax = self._calculate_tax(subtotal)

        return {
            "delivery_fee": delivery_fee,
            "service_fee": service_fee,
            "tax": tax,
        }

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

    def _validate_subtotal(self, subtotal: float) -> None:
        if not isinstance(subtotal, (int, float)):
            raise ValueError("subtotal must be a number")
        if subtotal < 0:
            raise ValueError("subtotal cannot be negative")

    def _calculate_delivery_fee(self, subtotal: float) -> float:
        return 5.00 if subtotal < 50 else 0.00

    def _calculate_service_fee(self, subtotal: float) -> float:
        return round(subtotal * 0.05, 2)

    def _calculate_tax(self, subtotal: float) -> float:
        return round(subtotal * 0.12, 2)