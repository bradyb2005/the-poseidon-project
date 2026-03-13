# This file defines the OrderItem class, representing an order item within our system.

from dataclasses import dataclass

from backend.models.restaurant.menu_item_model import MenuItem

@dataclass
class OrderItem:

    id: int
    menu_item: MenuItem
    quantity: int
    price_at_time: float

    def __post_init__(self) -> None:
        """
        This runs right after the dataclass constructor, which means it runs after we create an OrderItem object.
        We use it to validate that the OrderItem object is not invalid.
        """
        if not isinstance(self.id, int) or self.id < 0:
            raise ValueError("id must be a non-negative integer")

        if not isinstance(self.menu_item, MenuItem):
            raise ValueError("menu_item must be a MenuItem object")

        if not isinstance(self.quantity, int) or self.quantity <= 0:
            raise ValueError("quantity must be a positive integer")
        
        if not isinstance(self.price_at_time, (int, float)) or self.price_at_time < 0:
            raise ValueError("price_at_time must be a non-negative number")