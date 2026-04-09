import json
from pathlib import Path

class OrderRepository:
    def __init__(self, file_path='backend/data/orders.json'):
        self.file_path = Path(file_path)

    def load_all(self):
        """Reads the JSON file and returns a list of dictionaries."""
        if not self.file_path.exists():
            return []
        
        with open(self.file_path, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

    def save_all(self, orders):
        """Takes a list of order dictionaries and writes them to the JSON file."""
        with open(self.file_path, 'w') as file:
            json.dump(orders, file, indent=4, default=str)

    def find_by_id(self, target_id: str):
        """Fetches all records, but only returns the single matched item."""
        all_records = self.load_all()
        return next((item for item in all_records if item.get("id") == target_id), None)