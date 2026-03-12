# This file defines the Cart class, which represents a shopping cart for a customer. 

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.user.customer_model import Customer
    from backend.models.cart.cart_item_model import CartItem

class Cart:
    def __init__(self, id: int, customer: 'Customer'):
        self.id = id
        self.customer = customer
        self.items: List['CartItem'] = []

    def add_item(self, item: 'CartItem') -> None:
        """Adds an item to the cart. If it already exists, increases the quantity."""
        for existing_item in self.items:
            if existing_item.menu_item.id == item.menu_item.id:
                existing_item.quantity += item.quantity
                return
        self.items.append(item)

    def remove_item(self, item: 'CartItem') -> None:
        """Removes a specific item completely from the cart."""
        if item in self.items:
            self.items.remove(item)

    def update_quantity(self, item: 'CartItem', quantity: int) -> None:
        """Updates the quantity of a specific item. Removes it if quantity drops to 0."""
        if quantity <= 0:
            self.remove_item(item)
            return
            
        for existing_item in self.items:
            if existing_item.menu_item.id == item.menu_item.id:
                existing_item.quantity = quantity
                break

    def clear(self) -> None:
        """Empties the cart entirely."""
        self.items.clear()