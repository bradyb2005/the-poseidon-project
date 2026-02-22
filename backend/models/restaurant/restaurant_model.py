# backend/models/restaurant/restaurant_model.py

# Typing used for type hints to avoid circular imports
from typing import TYPE_CHECKING, List

# Read by VSCode for type checking but python ignores
if TYPE_CHECKING:
    from backend.models.user.restaurant_owner_model import RestaurantOwner
    from backend.models.restaurant.menu_item_model import MenuItem

class Restaurant:
    def __init__(self, id: int, name: str, owner: "RestaurantOwner"):
        self.id = id
        self.name = name
        self.owner = owner

        # Operational details
        self.address = None
        self.city = None
        self.postal_code = None
        self.phone = None
        self.cuisine_type = None
        self.open_time = None
        self.close_time = None

        # Status
        self.is_open = False

        # Menu
        self.menu = []
