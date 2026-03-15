# backend/repositories/restaurant_repository.py
from typing import List, Dict, Optional
from backend.models.restaurant.restaurant_model import Restaurant
from backend.models.restaurant.menu_item_model import MenuItem


class RestaurantRepository:
    def __init__(self, db_connection):
        # Initialize data storage collection
        self.db = db_connection
        self._next_res_id = 1
        self._next_menu_id = 1

    # --- Restaurant Information ---

    def create_restaurant(self, restaurant: Restaurant) -> int:
        """
        Feat2-FR1 (Storing Information)
        Create dictionary to store restaurant info
        """
        # Ensure that the dictionary contains all required fields
        # Run Insert query to data store
        # Return unique restaurant id
        restaurant.id = self._next_res_id
        self._next_res_id += 1

        lat = getattr(restaurant, 'latitude', 0.0)
        lon = getattr(restaurant, 'longitude', 0.0)
        final_published_status = restaurant.is_published if (
            lat != 0.0 and lon != 0.0) else False

        restaurant_data = {
            "id": restaurant.id,
            "name": restaurant.name,
            "owner_id": int(restaurant.owner.id),
            "address": restaurant.address,
            "latitude": getattr(restaurant, 'latitude', 0.0),
            "longitude": getattr(restaurant, 'longitude', 0.0),
            "phone": restaurant.phone,
            "open_time": restaurant.open_time,
            "close_time": restaurant.close_time,
            "is_published": restaurant.is_published,
            "menu": [{
                "id": item.id,
                "name": item.name,
                "price": item.price,
                "tags": item.tags
            } for item in restaurant.menu
            ]if restaurant.menu else []

        }

        self.db.append(restaurant_data)
        return restaurant.id

    def update_restaurant(self, restaurant: Restaurant) -> bool:
        """
        Feat2-FR3 (Correct and accurate information)
        Modify existing restaurant info
        """
        # Find existing restaurant by restaurant_id
        # Update fields and save changes to data store
        res_dict = self.get_by_id(restaurant.id)
        if res_dict:
            lat = getattr(restaurant, 'latitude', 0.0)
            long = getattr(restaurant, 'longitude', 0.0)

            # If coordinates are 0.0, force is_published to False
            # regardless of what the input object says.
            final_published_status = restaurant.is_published
            if lat == 0.0 or long == 0.0:
                final_published_status = False
            # We create a map of only the fields we want to sync
            changes = {
                "name": restaurant.name,
                "address": restaurant.address,
                "latitude": lat,
                "longitude": long,
                "phone": restaurant.phone,
                "open_time": restaurant.open_time,
                "close_time": restaurant.close_time,
                "is_published": final_published_status
            }
            # .update() merges these changes into the existing dict
            # Any key NOT in the 'changes' dict remains exactly as it was.
            res_dict.update(changes)
            return True
        return False

    def add_menu_item(self, restaurant_id: int, menu_item: MenuItem) -> bool:
        """
        Feat2-FR2 (Tagging menu items)
        Feat2-FR4 (Adding and editing menu items)
        Link menu item to specific restaurant with tags
        """
        # Verify restaurant exists
        # Format item
        # Store menu item in data store with reference to restaurant_id
        res_dict = self.get_by_id(restaurant_id)

        if res_dict:
            menu_item.id = self._next_menu_id
            self._next_menu_id += 1

            item_data = {
                "id": menu_item.id,
                "name": menu_item.name,
                "price": menu_item.price,
                "tags": menu_item.tags
            }
            # Ensure menu list exists and append
            if "menu" not in res_dict:
                res_dict["menu"] = []

            res_dict["menu"].append(item_data)
            res_dict.setdefault("menu", []).append(item_data)
            return True
        return False

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

    # --- Adding and editing menu item ---

    def update_menu_item(self, restaurant_id: int,
                         item_id: int, updated_item: MenuItem) -> bool:
        """
        Feat2-FR4: Adding and editing menu items
        Finds specific item in a restaurants menu and updates it
        """
        res = self.get_by_id(restaurant_id)
        if res and "menu" in res:
            for item in res["menu"]:
                if item["id"] == item_id:
                    # Update the stored dictionary with new object data
                    item["name"] = updated_item.name
                    item["price"] = updated_item.price
                    item["tags"] = updated_item.tags
                    return True
        return False

    def remove_menu_item(self, restaurant_id: str, item_id: str) -> bool:
        """
        Feat2-FR4 (Adding and editing menu items)
        Removes an item from the menu list.
        """
        res = self.get_by_id(restaurant_id)
        if res and "menu" in res:
            initial_len = len(res["menu"])
            res["menu"] = [item for item in
                           res["menu"] if item["id"] != item_id]
            return len(res["menu"]) < initial_len
        return False

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

    def filter_results(self, cuisine: Optional[str] = None,
                       min_rating: Optional[float] = None) -> List[Dict]:
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
        return [restaurant for restaurant in self.db
                if restaurant.get('cuisine') == cuisine]

    # --- Admin Support ---

    def get_most_popular_restaurants(self, limit: int = 10) -> List[Dict]:
        """
        Feat10-FR3 (Generate most popular restaurants)
        Retrieve top 10 most popular restaurants based on orders or ratings
        """
        # Query data store for restaurants sorted by popularity metrics
        # Return top N results
        pass
