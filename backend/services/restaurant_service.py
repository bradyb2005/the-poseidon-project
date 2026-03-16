# backend/services/restaurant_service.py
from backend.models.restaurant.menu_item_model import MenuItem
from backend.models.user.restaurant_owner_model import RestaurantOwner
from backend.models.user.admin import Admin
from backend.models.restaurant.restaurant_model import Restaurant


class RestaurantService:
    def __init__(self, restaurant_repository):
        self.restaurant_repository = restaurant_repository

    def _is_authorized(self, user):
        """Helper to standardize auth checks across the service"""
        return isinstance(user, (RestaurantOwner, Admin))

    def add_tagged_item(self, user, restaurant_id: int, item_data: dict):
        """
        Feat2-FR2: Tagging and Menu Management
        """

        # Ensure only owners and admins can modify menus
        if not self._is_authorized(user):
            return {"success": False, "error": "unauthorized"}
        
        # Get tags
        name = item_data.get("name")
        price = item_data.get("price")
        raw_tags = item_data.get("tags", [])
        # Validate to ensure  tags is a list and all elements are strings
        
        if not isinstance(raw_tags, list) or not all (isinstance(t, str) for t in raw_tags):
            return {"success": False, "error": "tags must be a list of strings"}
        
        if not name or price is None:
            return {"success": False, "error": "name and price are required"}
        
        # Create menu item and add to restaurant
        try:
            menu_item = MenuItem(
            id=item_data.get("id", 0),
            name=name,
            price=float(price),
            tags=raw_tags)
            # Link menu item to restaurant
            success = self.restaurant_repository.add_menu_item(restaurant_id, menu_item)

            if success:
                return {"success": True, "menu_item": menu_item.id}
            return {"success": False, "error": "Restaurant not found"}
    
        except (ValueError, TypeError):
            return {"success": False, "error": "invalid price format"}
    
    def update_item_availability(self, user, restaurant_id: int, menu_id: int, status: bool):
        """
        Feat2-FR2: Tagging and Menu Management
        Toggle if the item is available or not
        """

        if not self._is_authorized(user):
            return {"success": False, "error": "unauthorized"}

        success = self.restaurant_repository.update_menu_item_availability(restaurant_id, menu_id, status)
        return {"success": success}

    def register_restaurant(self, user, data: dict):
        """
        Feat2-FR1: Storing Information
        Checks if user is an admin or owner
        """
        if not self._is_authorized(user):
            return {"success": False, "error": "unauthorized"}
        
        try:
            new_restaurant = Restaurant(
                name=data.get("name"),
                owner=user,
                open_time=data.get("open_time", 900),
                close_time=data.get("close_time", 2100),
                menu=[]
            )
            new_id = self.restaurant_repository.create_restaurant(new_restaurant)
            return {"success": True, "restaurant_id": new_id}
        
        # Handle potential errors
        except Exception as e:
            return {"success": False, "error": str(e)}
        
    def publish_restaurant(self, restaurant_id):
        """
        Feat2-FR3: Correct and accurate information
        """
        restaurant = self.restaurant_repository.get_by_id(restaurant_id)

        if not restaurant:
            return {"success": False, "error": "Restaurant not found"}
        
        if not getattr(restaurant, 'address', None) or not getattr(restaurant, 'phone', None):
            return {"success": False, "error": "address and phone is required"}
        
        if not restaurant.menu:
            return {"success": False, "error": "menu cannot be empty"}
        
        try:
            restaurant.is_published = True
            self.restaurant_repository.update(restaurant)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
