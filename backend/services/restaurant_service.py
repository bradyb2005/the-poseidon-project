# backend/services/restaurant_service.py
from typing import List, Optional, Tuple, Dict
import math
from backend.schemas.restaurant_schema import Restaurant, RestaurantBase
from pydantic import Field, field_validator, model_validator


class RestaurantService:
    def __init__(self, restaurant_repo):
        self.restaurant_repo = restaurant_repo
    
    def _validate_business_rules(self, data: dict):
        lat = data.get("latitude")
        lon = data.get("longitude")
        open_time = data.get("open_time")
        close_time = data.get("close_time")

        if lat is not None and not (-90 <= lat <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if lon is not None and not (-180 <= lon <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        
        if open_time is not None:
            if not (0 <= open_time <= 2400):
                raise ValueError("Invalid time format (0-2400)")
        
        if open_time is not None and close_time is not None:
            if open_time >= close_time:
                raise ValueError("open_time must be before close_time")
    
    def get_restaurant_by_id(self, restaurant_id: str) -> Tuple[Optional[Restaurant], int]:
        """
        Returns a single restaurant
        Matches 200 OK or 404 Not Found
        """
        restaurants = self.restaurant_repo.load_all()
        target = next((r for r in restaurants if r.id == restaurant_id), None)
        
        if not target:
            return None, 404
        return target, 200
    
    def get_all_published(self) -> List[Dict]:
        """
        Returns a list of all published restaurants and remove sensitive data
        """
        restaurants = self.restaurant_repo.load_all()
        return [
            r.model_dump(by_alias=False, exclude={"owner_id"}) 
            for r in restaurants if r.is_published
        ]

    def assign_owner_to_restaurant(self, restaurant_id: str, owner_id: str) -> Tuple[Dict, int]:
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


    def update_restaurant_details(self, restaurant_id: str, update_data: dict) -> Tuple[Dict, int]:
        """
        Feat2-FR3: Update restaurant info
        """
        restaurants = self.restaurant_repo.load_all()
        target = next((r for r in restaurants if r.get_id() == restaurant_id), None)

        if not target:
            return {"error": "Not Found"}, 404

        try:
            self._validate_business_rules(update_data)
            for key, value in update_data.items():
                if hasattr(target, key):
                    setattr(target, key, value)
        
            self.restaurant_repo.save_all(restaurants)
            return {"message": "Updated successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 400

    def publish_restaurant(self, restaurant_id: str) -> Tuple[Dict, int]:
        """
        Feat2-FR3:
        Ensure valid phone/coords before publishing
        """
        restaurants = self.restaurant_repo.load_all()
        target = next((r for r in restaurants if str(r.id) == str(restaurant_id)), None)

        if not target:
            return {"error": "Not Found"}, 404

        if not target.phone or target.latitude == 0.0 or target.longitude == 0.0:
            return {"error": "Cannot publish: Missing phone or valid coordinates"}, 400

        target.is_published = True
        self.restaurant_repo.save_all(restaurants)
        return {"message": "Restaurant is now published"}, 200

    def get_filtered_view(self, restaurant_id: str, user_role: str) -> Tuple[Optional[Dict], int]:
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
