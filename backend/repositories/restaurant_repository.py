# backend/repositories/restaurant_repository.py
from typing import List, Dict, Optional
import uuid

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
        restaurant_data['id'] = str(uuid.uuid4())  # Generate unique ID for the restaurant
        self.db.append(restaurant_data)  # Simulate inserting into data store
        return restaurant_data['id']

    def update_restaurant(self, restaurant_id: str, update_data: Dict):
        """
        Feat2-FR3 (Correct and accurate information)
        Modify existing restaurant info
        """
        # Find existing restaurant by restaurant_id
        # Update fields and save changes to data store
        res = self.get_by_id(restaurant_id)
        if res:
            res.update(update_data)  # Update restaurant information
            return True
        return False

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
        for restaurant in self.db:
            if restaurant['id'] == restaurant_id:
                return restaurant
        return None

    # --- Browsing and Search ---

    def get_restaurants_paginated(self, page: int, limit: int):
        """
        Feat3-FR5 (Paginated Results)
        Retrieve subset of restaurants
        """
        # Calculate offset based on page and limit
        # Query data store for restaurants with pagination
        start = (page - 1) * limit
        end = start + limit
        return self.db[start:end]

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

    def get_all_restaurants(self):
        """
        Feat3-FR1 and Feat3-FR5
        Retrieve all restaurants with pagination
        """
        # Query data store for all restaurants with limit and offset
        return self.db

    def search_by_cuisine(self, cuisine: str) -> List[Dict]:
        """
        Feat3-FR4 (Filtering search results)
        Search for restaurants by cuisine type
        """
        # Query data store for restaurants matching the specified cuisine
        return [restaurant for restaurant in self.db if restaurant.get('cuisine') == cuisine]

    # --- Admin Support ---

    def get_most_popular_restaurants(self, limit: int = 10) -> List[Dict]:
        """
        Feat10-FR3 (Generate most popular restaurants)
        Retrieve top 10 most popular restaurants based on orders or ratings
        """
        # Query data store for restaurants sorted by popularity metrics
        # Return top N results
        pass