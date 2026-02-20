# Restaurant owner model class

from backend.models.user.user_model import User
from backend.models.restaurant.restaurant_model import Restaurant
from backend.models.menu_item.menu_item_model import MenuItem

class RestaurantOwner (User):
    #Inherit info from user

    # Allows the restaurant owner to create a restaurant 
    def create_restaurant(self, name: str) -> "Restaurant":
        return Restaurant(id=0, name=name, owner=self)

    def update_info(
            self,
            restaurant: "Restaurant",
            address: str = None,
            city: str = None,
            postal_code: str = None,
            phone: str = None,
            cuisine_type: str = None,
            open_time: str = None,
            close_time: str = None
    ):
        #Sets info for restaurant, only updates if value is not None
        if address is not None:
            restaurant.address = address
        if city is not None:
            restaurant.city = city
        if postal_code is not None:
            restaurant.postal_code = postal_code
        if phone is not None:
            restaurant.phone = phone
        if cuisine_type is not None:
            restaurant.cuisine_type = cuisine_type
        if open_time is not None:
            restaurant.open_time = open_time
        if close_time is not None:
            restaurant.close_time = close_time
    
    # adds a menu item to the restaurant's menu
    def add_menu_item(self, restaurant: "Restaurant", item: "MenuItem"):
        restaurant.menu.append(item)
    # removes a menu item from the restaurant's menu
    def remove_menu_item(self, restaurant: "Restaurant", item: "MenuItem"):
        restaurant.menu = [i for i in restaurant.menu if i.id != item.id]
    # updates a menu item in the restaurant's menu
    def update_menu_item(
            self,
            item: "MenuItem",
            name: str = None,
            description: str = None,
            price: float = None,
            category: str = None,
            available: bool = None
    ):
        # Updates menu item, only updates if value is not None, also checks if price is negative
        if name is not None:
            item.name = name
        if description is not None:
            item.description = description
        if price is not None:
            if price < 0:
                raise ValueError("Price cannot be negative")
            item.price = price
        if category is not None:
            item.category = category
        if available is not None:
            item.availability = available
        
    # Sets the availability of a menu item
    def set_item_availability(self, item: "MenuItem", status: bool ):
        item.availability = status

    
    