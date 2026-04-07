from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class PaymentStatus(str, Enum):
    ACCEPTED = "accepted"
    DENIED = "denied"


class CostBreakdown(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        validate_assignment=True,
    )

    subtotal: float = Field(alias="_subtotal")
    delivery_fee: float = Field(alias="_delivery_fee")
    service_fee: float = Field(alias="_service_fee")
    tax: float = Field(alias="_tax")
    total: float = Field(alias="_total")

    @field_validator("subtotal", "delivery_fee", "service_fee", "tax", "total")
    @classmethod
    def validate_non_negative_amounts(cls, value: float) -> float:
        if value < 0:
            raise ValueError("Cost values cannot be negative")
        return float(value)

    @model_validator(mode="after")
    def validate_total(self) -> "CostBreakdown":
        expected_total = self.subtotal + self.delivery_fee + self.service_fee + self.tax
        if round(self.total, 2) != round(expected_total, 2):
            raise ValueError("total must equal subtotal + delivery_fee + service_fee + tax")
        return self


class PaymentBase(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        validate_assignment=True,
    )

    order: Optional[Any] = Field(default=None, alias="_order")
    card_name: Optional[str] = Field(default=None, alias="_card_name")
    card_number: Optional[int] = Field(default=None, alias="_card_number")
    security_number: Optional[int] = Field(default=None, alias="_security_number")
    expiration: Optional[str] = Field(default=None, alias="_expiration")
    status: Optional[PaymentStatus] = Field(default=None, alias="_status")
    amount: Optional[float] = Field(default=None, alias="_amount")

    @field_validator("card_name")
    @classmethod
    def validate_card_name(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("card_name cannot be blank")
        return value.strip() if isinstance(value, str) else value

    @field_validator("card_number")
    @classmethod
    def validate_card_number(cls, value: Optional[int]) -> Optional[int]:
        if value is not None and value <= 0:
            raise ValueError("card_number must be positive")
        return value

    @field_validator("security_number")
    @classmethod
    def validate_security_number(cls, value: Optional[int]) -> Optional[int]:
        if value is not None and value <= 0:
            raise ValueError("security_number must be positive")
        return value

    @field_validator("expiration")
    @classmethod
    def validate_expiration(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("expiration cannot be blank")
        return value.strip() if isinstance(value, str) else value

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: Optional[float]) -> Optional[float]:
        if value is not None and value < 0:
            raise ValueError("amount cannot be negative")
        return float(value) if value is not None else value


class PaymentSchema(PaymentBase):
    id: int

    @model_validator(mode="after")
    def validate_required_payment_fields(self) -> "PaymentSchema":
        if self.order is None:
            raise ValueError("order is required")
        if self.card_name is None:
            raise ValueError("card_name is required")
        if self.card_number is None:
            raise ValueError("card_number is required")
        if self.security_number is None:
            raise ValueError("security_number is required")
        if self.expiration is None:
            raise ValueError("expiration is required")
        if self.status is None:
            raise ValueError("status is required")
        if self.amount is None:
            raise ValueError("amount is required")
        return self


class UpdatePaymentSchema(PaymentBase):
    pass