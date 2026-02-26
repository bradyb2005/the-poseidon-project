from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class CartItem:
    """A single line item in a cart."""
    menu_item_id: int
    quantity: int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.menu_item_id, int) or self.menu_item_id < 0:
            raise ValueError("menu_item_id must be a non-negative integer")
        if not isinstance(self.quantity, int) or self.quantity <= 0:
            raise ValueError("quantity must be a positive integer")

    def to_dict(self) -> Dict:
        return {"menu_item_id": self.menu_item_id, "quantity": self.quantity}

    @staticmethod
    def from_dict(data: Dict) -> "CartItem":
        return CartItem(
            menu_item_id=int(data["menu_item_id"]),
            quantity=int(data["quantity"]),
        )


@dataclass
class Cart:
    """
    Cart model:
    - One cart per user (typical)
    - Tracks restaurant_id optionally (helps enforce single-restaurant cart later)
    - Stores items as CartItem list
    """
    id: int
    user_id: int
    restaurant_id: Optional[int] = None
    items: List[CartItem] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.id, int) or self.id < 0:
            raise ValueError("id must be a non-negative integer")
        if not isinstance(self.user_id, int) or self.user_id < 0:
            raise ValueError("user_id must be a non-negative integer")
        if self.restaurant_id is not None and (not isinstance(self.restaurant_id, int) or self.restaurant_id < 0):
            raise ValueError("restaurant_id must be a non-negative integer or None")

    # -------------------------
    # Cart operations
    # -------------------------
    def add_item(self, menu_item_id: int, quantity: int = 1) -> None:
        if not isinstance(menu_item_id, int) or menu_item_id < 0:
            raise ValueError("menu_item_id must be a non-negative integer")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("quantity must be a positive integer")

        for it in self.items:
            if it.menu_item_id == menu_item_id:
                it.quantity += quantity
                return

        self.items.append(CartItem(menu_item_id=menu_item_id, quantity=quantity))

    def remove_item(self, menu_item_id: int) -> None:
        self.items = [it for it in self.items if it.menu_item_id != menu_item_id]

    def update_quantity(self, menu_item_id: int, quantity: int) -> None:
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("quantity must be a positive integer")

        for it in self.items:
            if it.menu_item_id == menu_item_id:
                it.quantity = quantity
                return

        raise ValueError("item not found in cart")

    def clear(self) -> None:
        self.items.clear()
        self.restaurant_id = None

    # -------------------------
    # Serialization
    # -------------------------
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "restaurant_id": self.restaurant_id,
            "items": [it.to_dict() for it in self.items],
        }

    @staticmethod
    def from_dict(data: Dict) -> "Cart":
        return Cart(
            id=int(data["id"]),
            user_id=int(data["user_id"]),
            restaurant_id=(int(data["restaurant_id"]) if data.get("restaurant_id") is not None else None),
            items=[CartItem.from_dict(x) for x in data.get("items", [])],
        )