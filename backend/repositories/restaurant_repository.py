# backend/repositories/restaurant_repository.py
import json
import os
from pathlib import Path
from dataclasses import asdict
from typing import List
from backend.models.restaurant.restaurant_model import Restaurant


class RestaurantRepository:
    def __init__(self, file_path: str = None):
        # guide to our path to the data
        if file_path:
            self._file_path = Path(file_path)
        else:
            self._file_path = Path(__file__).parent.parent / "data" / "restaurants.json"

        self._file_path.parent.mkdir(parents=True, exist_ok=True)

    def load_all(self) -> List[Restaurant]:
        """
        Read JSON file and return list of Restaurant objects
        """
        if not self._file_path.exists():
            return []
        
        try:
            with open(self._file_path, 'r') as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.load(f)
                return [Restaurant(**item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_all(self, restaurants: List[Restaurant]) -> bool:
        """
        Writes list of objects back to JSON
        """
        try:
            data = [asdict(res) for res in restaurants]
            with open(self._file_path, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except IOError:
            return False
