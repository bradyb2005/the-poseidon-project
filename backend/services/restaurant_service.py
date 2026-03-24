# backend/services/restaurant_service.py
from typing import List, Optional, Tuple, Dict
import math
from backend.schemas.restaurant_schema import Restaurant


class RestaurantService:
    def __init__(self, restaurant_repo):
        self.restaurant_repo = restaurant_repo
    
    def get_restaurant_by_id(self, restaurant_id: int) -> Tuple[Optional[Restaurant], int]:
        """
        Returns a single restaurant
        Matches 200 OK or 404 Not Found
        """
        restaurants = self.restaurant_repo.load_all()
        target = next((r for r in restaurants if r.id == restaurant_id), None)
        
        if not target:
            return None, 404
        return target, 200

    def assign_owner_to_restaurant(self, restaurant_id: int, owner_id: int) -> Tuple[Dict, int]:
        """
        Assigns user as owner to pre-existing restaurant
        """
        restaurants = self.restaurant_repo.load_all()
        target = next((r for r in restaurants if r.get_id() == restaurant_id), None)

        if not target:
            return {"error": "Restaurant not found"}, 404

        try:
            target.owner_id = str(owner_id)
            self.restaurant_repo.save_all(restaurants)
            return {"message": "Owner assigned", "restaurant_id": restaurant_id}, 200
        except ValueError as e:
            return {"error": str(e)}, 400


    def update_restaurant_details(self, restaurant_id: int, update_data: dict) -> Tuple[Dict, int]:
        """
        Feat2-FR3: Update restaurant info
        """
        restaurants = self.restaurant_repo.load_all()
        target = next((r for r in restaurants if r.get_id() == restaurant_id), None)

        if not target:
            return {"error": "Not Found"}, 404

        try:
            for key, value in update_data.items():
                if hasattr(target, key):
                    setattr(target, key, value)
        
            self.restaurant_repo.save_all(restaurants)
            return {"message": "Updated successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 400

    def publish_restaurant(self, restaurant_id: int) -> Tuple[Dict, int]:
        """
        Feat2-FR3:
        Ensure valid phone/coords before publishing
        """
        restaurants = self.restaurant_repo.load_all()
        target = next((r for r in restaurants if r.id == restaurant_id), None)

        if not target:
            return {"error": "Not Found"}, 404

        if not target.phone or target.latitude == 0.0 or target.longitude == 0.0:
            return {"error": "Cannot publish: Missing phone or valid coordinates"}, 400

        target.is_published = True
        self.restaurant_repo.save_all(restaurants)
        return {"message": "Restaurant is now published"}, 200

    def get_filtered_view(self, restaurant_id: int, user_role: str) -> Tuple[Optional[Dict], int]:
        """
        Feat2-FR4
        Throws a forbidden error if customer tries to view an unpublished restaurant
        """
        restaurants = self.restaurant_repo.load_all()
        target = next((r for r in restaurants if r.id == restaurant_id), None)

        if not target:
            return None, 404

        data = target.model_dump(by_alias=False)

        if user_role == "customer":
            if not target.is_published:
                return {"error": "Restaurant unavailable"}, 403
            # Strip sensitive data
            data.pop("owner_id", None)
            # data.pop("internal_revenue", None) # Example
            
        return data, 200
