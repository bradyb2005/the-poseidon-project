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
        # Check if user is an admin or owner
        if not (isinstance(user, RestaurantOwner) or isinstance(user, Admin)):
            return {"success": False, "error": "unauthorized"}
        
        try:
            new_restaurant = Restaurant(
                name=data.get("name"),
                open_time=data.get("open_time", "09:00"),
                close_time=data.get("close_time", "21:00"),
                distance_from_user=data.get("distance_from_user", 0.0),
                menu=[]

            )
            new_id = self.restaurant_repository.create_restaurant(new_restaurant)
            return {"success": True, "restaurant_id": new_id}
        
        # Handle potential errors
        except Exception as e:
            return {"success": False, "error": str(e)}
