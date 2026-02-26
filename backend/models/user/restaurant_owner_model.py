# Restaurant owner model class

from backend.models.restaurant.restaurant_model import Restaurant
from backend.models.user.user_model import User
import backend.models.restaurant.menu_item_model



class RestaurantOwner(User):

    def __init__(self, id: int, username: str, email: str, password_hash: str):
        super().__init__(id, username, email, password_hash)

    # Allows the restaurant owner to create a restaurant
    def create_restaurant(self, name, **kwargs):
        if not name or name.strip() == "":
            raise ValueError("Restaurant name cannot be empty")
        return Restaurant(name=name, owner = self, **kwargs)

    def update_info(self, restaurant, **kwargs):
        for key, value in kwargs.items():
            if hasattr(restaurant, key):
                setattr(restaurant, key, value)

    # adds a menu item to the restaurant's menu
    def add_menu_item(self, restaurant, item):
        restaurant.menu.append(item)

    # removes a menu item from the restaurant's menu
    def remove_menu_item(self, restaurant, item):
        restaurant.menu = [i for i in restaurant.menu if i.id != item.id]

    # updates a menu item in the restaurant's menu
    def update_menu_item(self, item, **kwargs):
        # Updates menu item, only updates if value is not None
        # also checks if price is negative
        if 'price' in kwargs:
            if kwargs['price'] < 0:
                raise ValueError("Price cannot be negative")
            item.price = kwargs['price']

        if 'available' in kwargs:
            item.availability = kwargs['available']
        
        for key, value in kwargs.items():
            if key not in ['price', 'available'] and hasattr(item, key):
                setattr(item, key, value)

    # Sets the availability of a menu item
    def set_item_availability(self, item, status):
        item.availability = status

    # Sets the restaurant's open and close times
    def set_open_closed(self, restaurant,status):
        if not isinstance(status, bool):
            raise ValueError ("Status must be a boolean")
        restaurant.is_open = status
