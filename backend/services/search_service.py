# backend/services/search_service.py
from typing import List, Dict, Optional
import math


class SearchService:
    def __init__(self, restaurant_repo, item_repo):
        """
        Connects to the repository
        """
        self.restaurant_repo = restaurant_repo
        self.item_repo = item_repo
    
    def _calculate_distance(self, user_lat: float, user_lon: float, res_lat: float, res_lon: float) -> float:
        """
        Haversine formula to calculate distance in kilometers
        """
        R = 6371.0
        
        dis_lat = math.radians(res_lat - user_lat)
        dis_lon = math.radians(res_lon - user_lon)
        
        a = (math.sin(dis_lat / 2)**2 + 
             math.cos(math.radians(user_lat)) * math.cos(math.radians(res_lat)) * math.sin(dis_lon / 2)**2)
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def get_nearby_restaurants(self, user_lat: float, user_lon: float, limit: int = 10) -> List[Dict]:
        """
        Feat3-FR1: Shows restaurants sorted by proximity to the user's location
        """
        all_res = self.restaurant_repo.load_all()
        published = [r for r in all_res if r.is_published]

        results = []
        for res in published:
            dist = self._calculate_distance(user_lat, user_lon, res.latitude, res.longitude)
            
            data = res.model_dump(by_alias=True)
            data["distance_km"] = round(dist, 2)
            results.append(data)


        results.sort(key=lambda x: x["distance_km"])
        return results[:limit]

    def search_by_keyword(self, keyword: str) -> List[Dict]:
        """
        Feat3-FR2: Searching
        Combines keyword matching with specific attribute filters.
        """
        if not keyword or len(keyword.strip()) < 2:
            return []

        search_term = keyword.lower().strip()

        published_restaurant_ids = {
            str(r.id) for r in self.restaurant_repo.load_all() 
            if r.is_published
        }

        all_items = self.item_repo.load_all()

        results = []
        for item in all_items:
            if str(item.restaurant_id) not in published_restaurant_ids:
                continue

            name_match = search_term in item.name.lower()
            tag_match = any(search_term in tag.lower() for tag in item.tags)

            if name_match or tag_match:
                results.append(item.model_dump())

        return results

    def get_homepage_featured(self) -> List[Dict]:
        """
        Feat3-FR3
        Returns a random or 'featured' selection of published items
        """
        published_ids = {str(r.id) for r in self.restaurant_repo.load_all() if r.is_published}
        all_items = self.item_repo.load_all()
        
        return [
            item.model_dump() for item in all_items 
            if str(item.restaurant_id) in published_ids
        ][:5]

    def browse_homepage(self) -> List[Dict]:
        """
        Feat3-FR3: Returns all published restaurants for the homepage list.
        """
        all_res = self.restaurant_repo.load_all()
        
        return [
            res.model_dump(by_alias=True) 
            for res in all_res 
            if res.is_published
        ]

    def get_restaurant_details(self, restaurant_id: int) -> Optional[Dict]:
        """
        Feat3-FR3: Fetches a specific restaurant and injects its full menu.
        """
        all_restaurants = self.restaurant_repo.load_all()
        restaurant = next((r for r in all_restaurants if r.id == restaurant_id), None)

        if not restaurant or not restaurant.is_published:
            return None

        all_items = self.item_repo.load_all()
        menu_details = [
            item.model_dump(by_alias=True) 
            for item in all_items 
            if item.restaurant_id == restaurant_id
        ]

        data = restaurant.model_dump(by_alias=True)
        data["full_menu_details"] = menu_details
        
        return data