# backend/repositories/order_repository.py
import json
import os
from typing import List
from backend.schemas.order_schema import Order

# Dummy file for review servace to be tested.

class OrderRepository:
    def __init__(self, file_path='backend/data/orders.json'):
        self.file_path = file_path

    def load_all(self) -> List[Order]:
        """Reads the JSON file and returns a list of Order objects."""
        if not os.path.exists(self.file_path):
            return []
        
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                # Map dictionaries to Pydantic Order objects
                return [Order(**item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_all(self, orders: List[Order]):
        """Writes list of Order objects back to JSON."""
        # Use mode='json' to handle datetimes and Enums automatically
        data = [order.model_dump(mode='json') for order in orders]
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)