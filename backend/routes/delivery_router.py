from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from backend.schemas.delivery_schema import (
    DeliverySchema,
    DeliveryStatusUpdateSchema,
)
from backend.services.delivery_service import DeliveryService

router = APIRouter(prefix="/deliveries", tags=["Delivery"])
delivery_service = DeliveryService()


@router.post("/", response_model=DeliverySchema, status_code=status.HTTP_201_CREATED)
def create_delivery(delivery: DeliverySchema) -> DeliverySchema:
    try:
        return delivery_service.create_delivery(delivery)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get("/", response_model=list[DeliverySchema])
def get_all_deliveries() -> list[DeliverySchema]:
    return delivery_service.get_all_deliveries()


@router.get("/{delivery_id}", response_model=DeliverySchema)
def get_delivery(delivery_id: int) -> DeliverySchema:
    delivery = delivery_service.get_delivery(delivery_id)
    if delivery is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery not found.",
        )
    return delivery


@router.put("/{delivery_id}/status", response_model=DeliverySchema)
def update_delivery_status(
    delivery_id: int,
    update_data: DeliveryStatusUpdateSchema,
) -> DeliverySchema:
    updated_delivery = delivery_service.update_delivery_status(delivery_id, update_data)

    if updated_delivery is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery not found.",
        )

    return updated_delivery


@router.delete("/{delivery_id}", status_code=status.HTTP_200_OK)
def delete_delivery(delivery_id: int) -> dict[str, str]:
    deleted = delivery_service.delete_delivery(delivery_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery not found.",
        )

    return {"message": "Delivery deleted successfully."}