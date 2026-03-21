# backend/repositories/restaurant_repository.py
import json
import os
from typing import List, Dict
from backend.models.restaurant.restaurant_model import Restaurant


class RestaurantRepository:
    def __init__(self, storage_service=None):
        # guide to our path to the data
        self._storage = storage_service or open
        self._file_path = os.path.join("backend", "data", "items.json")
        
        # Only create directories if we're using the real file system
        if self._storage == open:
            os.makedirs(os.path.dirname(self._file_path), exist_ok=True)

    def load_all(self) -> List[Restaurant]:
        """
        Read JSON file and return list of Restaurant objects
        """
        if self._storage == open and not os.path.exists(self._file_path):
            return[]
        
        try:
            with self._storage(self._file_path, 'r') as f:
                data = json.load(f)
                return [Restaurant.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError, FileNotFoundError):
            return []

    def save_all(self, restaurants: List[Restaurant]) -> bool:
        """
        Writes list of objects back to JSON
        """
        try:
            data = [res.to_dict() for res in restaurants]
            with self._storage(self._file_path, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception:
            return False
