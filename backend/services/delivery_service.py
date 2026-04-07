from __future__ import annotations

from typing import Dict, Optional

from backend.schemas.delivery_schema import (
    DeliverySchema,
    DeliveryStatus,
    DeliveryStatusUpdateSchema,
)


class DeliveryService:
    def __init__(self) -> None:
        self.deliveries: Dict[int, DeliverySchema] = {}

    def create_delivery(self, delivery: DeliverySchema) -> DeliverySchema:
        if delivery.delivery_id in self.deliveries:
            raise ValueError(f"Delivery with ID {delivery.delivery_id} already exists.")

        self.deliveries[delivery.delivery_id] = delivery
        return delivery

    def get_delivery(self, delivery_id: int) -> Optional[DeliverySchema]:
        return self.deliveries.get(delivery_id)

    def get_all_deliveries(self) -> list[DeliverySchema]:
        return list(self.deliveries.values())

    def update_delivery_status(
        self,
        delivery_id: int,
        update_data: DeliveryStatusUpdateSchema,
    ) -> Optional[DeliverySchema]:
        delivery = self.deliveries.get(delivery_id)
        if delivery is None:
            return None

        delivery.status = update_data.status

        if update_data.estimated_arrival is not None:
            delivery.estimated_arrival = update_data.estimated_arrival

        return delivery

    def assign_driver(
        self,
        delivery_id: int,
        driver_name: str,
        driver_contact: str,
    ) -> Optional[DeliverySchema]:
        delivery = self.deliveries.get(delivery_id)
        if delivery is None:
            return None

        delivery.driver_name = driver_name
        delivery.driver_contact = driver_contact

        if delivery.status == DeliveryStatus.PENDING:
            delivery.status = DeliveryStatus.ASSIGNED

        return delivery

    def delete_delivery(self, delivery_id: int) -> bool:
        if delivery_id not in self.deliveries:
            return False

        del self.deliveries[delivery_id]
        return True