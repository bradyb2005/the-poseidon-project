# backend/repositories/items_repository.py
import json
from pathlib import Path
from typing import List, Optional
from uuid import UUID, uuid4
from decimal import Decimal
from pydantic import ValidationError
from backend.schemas.items_schema import MenuItem

class ItemRepository:
    def __init__(self, file_path: str = None):
        if file_path:
            self._file_path = Path(file_path)
        else:
            self._file_path = Path(__file__).parent.parent / "data" / "items.json"
        
        if not self._file_path.parent.exists():
            self._file_path.parent.mkdir(parents=True, exist_ok=True)

    def load_all(self) -> List[MenuItem]:
        """
        Reads the JSON file and returns a list of MenuItem objects
        Handles missing fields (price, id) by providing defaults
        """
        if not self._file_path.exists():
            return []
        
        try:
            with open(self._file_path, 'r') as f:
                data = json.load(f)
                
                if not isinstance(data, list):
                    return []
    
                items = []
                for raw_item in data:
                    if "price" not in raw_item:
                        raw_item["price"] = Decimal("0.00")
                    if "id" not in raw_item and "item_id" not in raw_item:
                        raw_item["id"] = str(uuid4())
                        
                    try:
                        items.append(MenuItem(**raw_item))
                    except ValidationError as e:
                        print(f"Skipping invalid item {raw_item.get('item_name')}: {e}")
                
                return items
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_all(self, items: List[MenuItem]) -> bool:
        """
        Serializes the list back to JSON with full schema details.
        """
        try:
            data = [item.model_dump(mode="json", by_alias=True) for item in items]
            with open(self._file_path, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except (IOError, TypeError):
            return False
