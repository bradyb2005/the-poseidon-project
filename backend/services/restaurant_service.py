# backend/services/restaurant_service.py
import math
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

    def get_nearby_restaurants(self, customer, radius_km=10.0):
        """
        Feat3-FR1: Restaurants near me
        Retrieves all published restaurants within a specific radius of the customer.
        """
        all_restaurants = self.restaurant_repository.get_all_restaurants()
        nearby = []

        for res_data in all_restaurants:
            # Rule: Only show published restaurants to customers
            if not res_data.get("is_published"):
                continue

            # Calculate distance using the Haversine helper
            dist = self.calculate_haversine(
                customer.latitude, customer.longitude,
                res_data.get("latitude", 0.0), res_data.get("longitude", 0.0)
            )

            if dist <= radius_km:
                # Add distance to the data so the frontend can display "1.2 km away"
                res_data["distance_from_user"] = round(dist, 1)
                nearby.append(res_data)

        # 3. Sort by distance (closest first)
        return sorted(nearby, key=lambda x: x["distance_from_user"])

    @staticmethod
    def calculate_haversine(lat1, lon1, lat2, lon2):
        """
        Feat3-FR1:
        Calculates the great-circle distance between two points on the Earth.
        Returns distance in Kilometers.
        """
        # Earth radius in kilometers
        R = 6371.0

        # Convert degrees to radians
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        # Haversine formula
        a = math.sin(dphi / 2)**2 + \
            math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
