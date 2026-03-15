from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.order.order_model import Order


class PaymentStatus(Enum):
    ACCEPTED = "accepted"
    DENIED = "denied"


@dataclass
class Payment:
    id: int
    order: "Order"
    card_name: str
    card_number: int
    security_number: int
    expiration: str
    status: PaymentStatus
    amount: float

    def validate(self) -> bool:
        return (
            self.card_name.strip() != ""
            and self.card_number > 0
            and self.security_number > 0
            and self.expiration.strip() != ""
            and self.amount > 0
        )

    def get_payment_info(self) -> dict:
        return {
            "id": self.id,
            "order_id": self.order.id,
            "card_name": self.card_name,
            "status": self.status.value,
            "amount": self.amount,
            "expiration": self.expiration,
        }

    def processPayment(self) -> bool:
        if self.status == PaymentStatus.ACCEPTED:
            return False

        if not self.validate():
            self.status = PaymentStatus.DENIED
            return False

        gateway_response = True

        if gateway_response:
            self.status = PaymentStatus.ACCEPTED
            return True

        self.status = PaymentStatus.DENIED
        return False

    def request_fulfillment(self) -> bool:
        return self.status == PaymentStatus.ACCEPTED