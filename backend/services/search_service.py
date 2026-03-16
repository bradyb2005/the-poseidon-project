# backend/services/search_service.py
from typing import List, Dict, Optional
from backend.repositories.restaurant_repository import RestaurantRepository


class SearchService:
    def __init__(self, restaurant_repo: RestaurantRepository):
        """
        Connects to the repository
        """
        self.repo = restaurant_repo

    def search(self, query: str, cuisine: Optional[str] = None,
               min_rating: Optional[float] = None) -> List[Dict]:
        """
        Feat3-FR2: Searching
        Combines keyword matching with specific attribute filters.
        """
        if not query or len(query.strip()) < 2:
            # Return an empty list or raise a custom exception
            # if the query is too short
            return []

        # Gets restaurants matching the name or menu items
        results = self.repo.search_restaurants_and_menu_items(query)

        # Apply filters
        if cuisine:
            results = [r for r in results if
                       r.get("cuisine", "").lower() == cuisine.lower()]

        if min_rating is not None:
            results = [r for r in results if r.get("rating", 0) >= min_rating]

        # Sort results
        return results
