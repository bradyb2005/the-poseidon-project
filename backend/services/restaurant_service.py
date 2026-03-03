from backend.models.user.restaurant_owner_model import RestaurantOwner
from backendd.models.user.admin_model import Admin
from backend.models.user.user_model import User
from backend.repositories.restaurant_repository import RestaurantRepository

class RestaurantService:
    def __init__(self, restaurant_repository):
        self.restaurant_repository = restaurant_repository

    def register_restaurant(self, restaurant_data: dict):
        """
        Feat2-FR1: Storing Information
        Checks if user is an admin or owner
        """
        # Check if user is an admin or owner
        if not (isinstance(User, RestaurantOwner) or isinstance(User, Admin)):
            return {"success": False, "error": "unathouraized"}
        
        if not restaurant_data.get("name") or not restaurant_data.get("address"):
            return {"success": False, "error": "Missing required fields"}
        
        # Save to repository
        new_id = self.restaurant_repository.create_restaurant(restaurant_data)
        return {"success": True, "restaurant_id": new_id}
