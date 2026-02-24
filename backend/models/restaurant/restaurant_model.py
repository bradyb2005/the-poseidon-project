# backend/models/restaurant/restaurant_model.py

import uuid

# Typing used for type hints to avoid circular imports
from typing import TYPE_CHECKING, List

# Read by VSCode for type checking but python ignores
if TYPE_CHECKING:
    from backend.models.user.restaurant_owner_model import RestaurantOwner
    from backend.models.restaurant.menu_item_model import MenuItem

class Restaurant:
    def __init__(self, name: str, owner: "RestaurantOwner", **kwargs):
        self.id = str(uuid.uuid4())
        self.name = name
        self.owner = owner

        # Operational details
        self.address = kwargs.get('address')
        self.phone = kwargs.get('phone')
        self.open_time = kwargs.get('open_time')
        self.close_time = kwargs.get('close_time')

        # Set all other kwargs as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

        # Status
        self.is_open = False

        # Menu
        self.menu = []
