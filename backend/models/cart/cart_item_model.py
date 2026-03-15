# This method defines the CartItem class, representing an item in the shopping cart within our system.

from dataclasses import dataclass

from backend.models.restaurant.menu_item_model import MenuItem

@dataclass
class CartItem:

    id: int
    menu_item: MenuItem
    quantity: int

    def __post_init__(self) -> None:
        """
        This runs right after the dataclass constructor, which means it runs after we create a CartItem object.
        We use it to validate that the CartItem object is not invalid.
        """
        if not isinstance(self.id, int) or self.id < 0:
            raise ValueError("id must be a non-negative integer")

        if not isinstance(self.menu_item, MenuItem):
            raise ValueError("menu_item must be a MenuItem object")

        if not isinstance(self.quantity, int) or self.quantity <= 0:
            raise ValueError("quantity must be a positive integer")

