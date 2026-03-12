# backend/models/restaurant/restaurant_model.py

import uuid
from typing import TYPE_CHECKING, List

# Read by VSCode for type checking but python ignores
if TYPE_CHECKING:
    from backend.models.restaurant.menu_item_model import MenuItem


# Restaurant information initialization
class Restaurant:
    def __init__(
            self,
            name: str,
            open_time: str,
            close_time: str,
            distance_from_user: float,
            menu: List["MenuItem"],
            is_published: bool = False):
        self.id = str(uuid.uuid4())
        self.name = name
        self.open_time: open_time
        self.close_time: close_time
        self.distance_from_user: distance_from_user
        self.menu: menu
        self.is_published: False
    
    # Method to publish the restaurant, making it visible to customers
    def publish(self):
        if not self.menu:
            return False  # Cannot publish empty menu
        self.is_published = True
        return True
    
    def get_view(self, perspective: str):
        # Allows admin to see restaurants from different perspectives
        if perspective == "Customer" and not self.is_published:
            return None  # Unpublished restaurants are hidden from customers
        return self.__dict__