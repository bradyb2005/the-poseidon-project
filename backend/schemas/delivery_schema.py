from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DeliveryStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    PICKED_UP = "picked_up"
    ON_THE_WAY = "on_the_way"
    DELIVERED = "delivered"


class DeliverySchema(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )

    delivery_id: int = Field(..., description="Unique identifier for the delivery")
    order_id: int = Field(..., description="Order associated with this delivery")
    status: DeliveryStatus = Field(..., description="Current delivery status")
    estimated_arrival: Optional[str] = Field(
        default=None,
        description="Estimated arrival time for the delivery",
    )
    driver_name: Optional[str] = Field(
        default=None,
        description="Name of the assigned driver",
    )
    driver_contact: Optional[str] = Field(
        default=None,
        description="Contact information for the assigned driver",
    )

    @field_validator("delivery_id", "order_id")
    @classmethod
    def validate_positive_ids(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("IDs must be positive integers.")
        return value

    @field_validator("estimated_arrival", "driver_name", "driver_contact")
    @classmethod
    def validate_optional_strings(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("Optional string fields cannot be blank if provided.")
        return value


class DeliveryStatusUpdateSchema(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    status: DeliveryStatus = Field(..., description="Updated delivery status")
    estimated_arrival: Optional[str] = Field(
        default=None,
        description="Updated estimated arrival time",
    )

    @field_validator("estimated_arrival")
    @classmethod
    def validate_estimated_arrival(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("Estimated arrival cannot be blank if provided.")
        return value