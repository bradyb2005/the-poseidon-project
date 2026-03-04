from backend.models.restaurant.menu_item_model import MenuItem
from backend.models.user.restaurant_owner_model import RestaurantOwner
from backend.models.user.admin import Admin

class RestaurantService:
    def __init__(self, restaurant_repository):
        self.restaurant_repository = restaurant_repository
    
    def add_tagged_item(self, user, restaurant_id: int, item_data: dict):
        """
        Feat2-FR2: Tagging and Menu Management
        """

        # Ensure only owners and admins can modify menus
        if not (isinstance(user, RestaurantOwner) or isinstance(user, Admin)):
            return {"success": False, "error": "unauthorized"}
        
        # Get tags
        name = item_data.get("name")
        price = item_data.get("price")
        tags = item_data.get("tags", [])

        if not name or price is None:
            return {"success": False, "error": "name and price are required"}
        
        # Create menu item and add to restaurant
        menu_item = MenuItem(
            id=item_data.get("id", 0),  # ID will be set by the repository
            name=name,
            price=float(price),
            tags=tags
        )
        # Link menu item to restaurant
        success = self.restaurant_repository.add_menu_item(restaurant_id, menu_item)

        if success:
            return {"success": True, "menu_item": menu_item.id}
        return {"success": False, "error": "Restaurant not found"}
    
    def update_item_availability(self, user, restaurant_id: int, menu_id: int, status: bool):
        """
        Feat2-FR2: Tagging and Menu Management
        Toggle if the item is available or not
        """

        # Ensure only owners and admins can modify menus
        if not isinstance(user, RestaurantOwner) or isinstance(user, Admin):
            return {"success": False, "error": "unauthorized"}
        
        success = self.restaurant_repository.update_menu_item_availability(restaurant_id, menu_id, status)
        return {"success": success}
