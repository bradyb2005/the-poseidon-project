# backend/models/user/user_schema.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from backend.schemas.cart_schema import Cart
from backend.schemas.loyalty_schema import LoyaltyTier

"""Represents a user and validates required user data."""

@dataclass
class User:
    id: str
    username: str
    email: str
    password_hash: str
    phone: str = ""
    address: str = ""
    location: str = ""
    postal_code: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    cart: Cart = field(init = False)
    orders: List[str] = field(default_factory=list)
    owned_restaurants_id: List[str] = field(default_factory=list)
    # ADDED IN EXTRA FEATURE: Loyalty Program
    loyalty_points: int = 0
    loyalty_tier: str = LoyaltyTier.BRONZE.value


    def __post_init__(self) -> None:
        required_string_fields = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
        }

        for field_name, value in required_string_fields.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        if "@" not in self.email:
            raise ValueError("email must contain '@'")

        if "." not in self.email.split("@", 1)[1]:
            raise ValueError("email domain must contain '.'")

        optional_string_fields = {
            "phone": self.phone,
            "address": self.address,
            "location": self.location,
            "postal_code": self.postal_code,
        }

        for field_name, value in optional_string_fields.items():
            if not isinstance(value, str):
                raise ValueError(f"{field_name} must be a string")

        if self.latitude is not None and not isinstance(self.latitude, (int, float)):
            raise ValueError("latitude must be a number or None")

        if self.longitude is not None and not isinstance(self.longitude, (int, float)):
            raise ValueError("longitude must be a number or None")

        self.cart = Cart(customer_id=self.id)

        list_fields = {
            "orders": self.orders,
            "owned_restaurants_id": self.owned_restaurants_id,
        }

        for field_name, value in list_fields.items():
            if not isinstance(value, list):
                raise ValueError(f"{field_name} must be a list")
            
    @staticmethod
    def hash_password(password: str) -> str:
        """Temporary hashing method (to be moved to service layer)."""
        if not isinstance(password, str) or not password.strip():
            raise ValueError("password must be a non-empty string")
        return f"hashed_{password}"
