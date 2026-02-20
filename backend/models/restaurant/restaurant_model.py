# backend/models/restaurant/restaurant_model.py

from backend.models.user.restaurant_owner_model import RestaurantOwner

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