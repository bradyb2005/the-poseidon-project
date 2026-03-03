# backend/repositories/restaurant_repository.py
from typing import List, Dict, Optional

class RestaurantRepository:
    def __init__(self, db_connection):
        # Initialize data storage collection
        self.db = db_connection
    
    # --- Restaurant Information ---

    def create_restaurant(self, restaurant_data: Dict) -> str:
        """
        Feat2-FR1 (Storing Information)
        Create dictionary to store restaurant info
        """
        # Ensure that the dictionary contains all required fields
        # Run Insert query to data store
        # Return unique restaurant id
        pass

    def update_restaurant(self, restaurant_id: str, update_data: Dict) -> bool:
        """
        Feat2-FR3 (Correct and accurate information)
        Modify existing restaurant info
        """
        # Find existing restaurant by restaurant_id
        # Update fields and save changes to data store
        pass

    def add_menu_item(self, restaurant_id: str, menu_item_data: Dict):
        """
        Feat2-FR2 (Tagging menu items)
        Feat2-FR4 (Adding and editing menu items)
        Link menu item to specific restaurant with tags
        """
        # Verify restaurant exists
        # Format item
        # Store menu item in data store with reference to restaurant_id
        pass

    def get_by_id(self, restaurant_id: str) -> Optional[Dict]:
        """
        Feat3-FR3 and Feat2-FR3
        Retrieve restaurant details by id
        """
        # Query data store for restaurant with given id
        # Return restaurant details if found, else return None
        pass

    # --- Browsing and Search ---

    def get_all_paginated(self, page: int, limit: int) -> List[Dict]:
        """
        Feat3-FR1 (Display closest restaurants in home page)
        Feat3-FR5 (Paginated Results)
        Retrieve subset of restaurants
        """
        # Calculate offset based on page and limit
        # Query data store for restaurants with pagination
        pass

    def search_restaurants_and_menu_items(self, query: str) -> List[Dict]:
        """
        Feat3-FR2 (Searching for restaurants/items)
        Search for restaurants and menu items matching query
        """
        # Remove special characters from query
        # Perform keyword search in restaurant names and menu item names
        # Return list of matching restaurants and menu items
        pass

    def filter_results(self, cuisine: Optional[str] = None, min_rating: Optional[float] = None) -> List[Dict]:
        """
        Feat3-FR4 (Filtering results)
        Filter search results based on criteria
        """
        # Build query based on provided filters
        # Query data store for matching restaurants
        # If cuisine is provided, filter by cuisine type
        # If min_rating is provided, filter by average rating
        pass

    def get_all_restaurants(self, limit: int = 100, offset: int = 0) -> list:
        """
        Feat3-FR1 and Feat3-FR5
        Retrieve all restaurants with pagination
        """
        # Query data store for all restaurants with limit and offset
        pass

    # --- Admin Support ---

    def get_most_popular_restaurants(self, limit: int = 10) -> List[Dict]:
        """
        Feat10-FR3 (Generate most popular restaurants)
        Retrieve top 10 most popular restaurants based on orders or ratings
        """
        # Query data store for restaurants sorted by popularity metrics
        # Return top N results
        pass