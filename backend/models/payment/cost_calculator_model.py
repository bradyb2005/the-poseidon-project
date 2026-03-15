from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.order.order_model import Order


@dataclass
class CostBreakdown:
    subtotal: float
    tax: float
    deliveryFee: float
    serviceFee: float
    total: float


class CostCalculator:
    def calculateSubtotal(self, order: "Order") -> float:
        subtotal = 0.0
        for item in order.items:
            subtotal += item.price * item.quantity
        return subtotal

    def calculateTax(self, order: "Order") -> float:
        subtotal = self.calculateSubtotal(order)
        return subtotal * 0.12

    def calculateDeliveryFee(self, order: "Order") -> float:
        return 5.00

    def calculateServiceFee(self, order: "Order") -> float:
        subtotal = self.calculateSubtotal(order)
        return subtotal * 0.05

    def calculateTotal(self, order: "Order") -> float:
        subtotal = self.calculateSubtotal(order)
        tax = self.calculateTax(order)
        delivery = self.calculateDeliveryFee(order)
        service = self.calculateServiceFee(order)
        return subtotal + tax + delivery + service

    def getBreakdown(self, order: "Order") -> CostBreakdown:
        subtotal = self.calculateSubtotal(order)
        tax = self.calculateTax(order)
        delivery = self.calculateDeliveryFee(order)
        service = self.calculateServiceFee(order)
        total = subtotal + tax + delivery + service

        return CostBreakdown(
            subtotal=subtotal,
            tax=tax,
            deliveryFee=delivery,
            serviceFee=service,
            total=total,
        )