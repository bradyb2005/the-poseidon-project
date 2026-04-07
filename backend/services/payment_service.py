from typing import Any
from backend.schemas.payment_schema import CostBreakdown, PaymentSchema, PaymentStatus


class PaymentService:
    """
    Handles payment-related calculations and processing logic
    """

    def calculate_subtotal(self, order: Any) -> float:
        """
        Calculates subtotal from order items

        Supports both:
        - dict-style orders from frontend JSON
        - object-style orders used in unit tests
        """
        self._validate_order(order)

        subtotal = 0.0
        items = order["items"] if isinstance(order, dict) else order.items

        for item in items:
            self._validate_item(item)

            price = item["price"] if isinstance(item, dict) else item.price
            quantity = item["quantity"] if isinstance(item, dict) else item.quantity

            subtotal += price * quantity

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

    def calculate_total(self, subtotal: float) -> CostBreakdown:
        """
        Combines subtotal, fees, and tax into a CostBreakdown object
        """
        self._validate_subtotal(subtotal)

        fees = self.calculate_fees_and_taxes(subtotal)
        total = subtotal + fees["delivery_fee"] + fees["service_fee"] + fees["tax"]

        return CostBreakdown(
            subtotal=subtotal,
            delivery_fee=fees["delivery_fee"],
            service_fee=fees["service_fee"],
            tax=fees["tax"],
            total=round(total, 2),
        )

    def retrieve_payment_info(self, payment: PaymentSchema) -> dict:
        """
        Retrieves key payment information in dictionary form
        """
        self._validate_payment(payment)

        return {
            "id": payment.id,
            "order": payment.order,
            "card_name": payment.card_name,
            "card_number": payment.card_number,
            "expiration": payment.expiration,
            "status": payment.status,
            "amount": payment.amount,
        }

    def process_payment(self, payment: PaymentSchema) -> PaymentSchema:
        """
        Simulates payment processing through a payment gateway
        """
        self._validate_payment(payment)

        if payment.card_number and len(str(payment.card_number)) >= 12:
            payment.status = PaymentStatus.ACCEPTED
        else:
            payment.status = PaymentStatus.DENIED

        return payment

    def create_fulfillment_request(self, payment: PaymentSchema) -> dict:
        """
        Creates a fulfillment request only for accepted payments
        """
        self._validate_payment(payment)
        self._validate_accepted_payment(payment)

        return {
            "payment_id": payment.id,
            "order": payment.order,
            "status": "fulfillment_requested",
            "message": "Fulfillment request created successfully",
        }

    # -------------------------
    # Private helpers
    # -------------------------

    def _validate_order(self, order: Any) -> None:
        if order is None:
            raise ValueError("order cannot be None")

        if isinstance(order, dict):
            if "items" not in order:
                raise ValueError("order must have items")
            if not isinstance(order["items"], list):
                raise ValueError("order items must be a list")

        elif hasattr(order, "items"):
            if not isinstance(order.items, list):
                raise ValueError("order items must be a list")

        else:
            raise ValueError("order must have items")

    def _validate_item(self, item: Any) -> None:
        if isinstance(item, dict):
            if "price" not in item or "quantity" not in item:
                raise ValueError("item must have price and quantity")

            if not isinstance(item["price"], (int, float)):
                raise ValueError("item price must be a number")

            if not isinstance(item["quantity"], int):
                raise ValueError("item quantity must be an integer")

            if item["price"] < 0:
                raise ValueError("item price cannot be negative")

            if item["quantity"] <= 0:
                raise ValueError("item quantity must be positive")

        elif hasattr(item, "price") and hasattr(item, "quantity"):
            if not isinstance(item.price, (int, float)):
                raise ValueError("item price must be a number")

            if not isinstance(item.quantity, int):
                raise ValueError("item quantity must be an integer")

            if item.price < 0:
                raise ValueError("item price cannot be negative")

            if item.quantity <= 0:
                raise ValueError("item quantity must be positive")

        else:
            raise ValueError("invalid item format")

    def _validate_subtotal(self, subtotal: float) -> None:
        if not isinstance(subtotal, (int, float)):
            raise ValueError("subtotal must be a number")
        if subtotal < 0:
            raise ValueError("subtotal cannot be negative")

    def _validate_payment(self, payment: PaymentSchema) -> None:
        if payment is None:
            raise ValueError("payment cannot be None")

    def _validate_accepted_payment(self, payment: PaymentSchema) -> None:
        if payment.status != PaymentStatus.ACCEPTED:
            raise ValueError("fulfillment request can only be created for accepted payments")

    def _calculate_delivery_fee(self, subtotal: float) -> float:
        return 5.00 if subtotal < 50 else 0.00

    def _calculate_service_fee(self, subtotal: float) -> float:
        return round(subtotal * 0.05, 2)

    def _calculate_tax(self, subtotal: float) -> float:
        return round(subtotal * 0.12, 2)