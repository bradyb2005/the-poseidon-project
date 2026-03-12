# backend/services/restaurant_service.py
from backend.models.user.restaurant_owner_model import RestaurantOwner
from backend.models.user.admin import Admin
from backend.models.restaurant.restaurant_model import Restaurant


class RestaurantService:
    def __init__(self, restaurant_repository):
        self.restaurant_repository = restaurant_repository

    def register_restaurant(self, user, data: dict):
        """
        Feat2-FR1: Storing Information
        Checks if user is an admin or owner
        """
        user_type = user.__class__.__name__
        # Check if user is an admin or owner
        if user_type not in ["RestaurantOwner", "Admin"]:
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
        
        if not restaurant.address or not restaurant.phone:
            return {"success": False, "error": "address and phone is required"}
        
        if not restaurant.menu:
            return {"success": False, "error": "menu cannot be empty"}
        
        try:
            restaurant.is_published = True
            self.restaurant_repository.update(restaurant)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
