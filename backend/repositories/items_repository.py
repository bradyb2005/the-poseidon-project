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
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)
                
                if not isinstance(data, list):
                    return []
    
                items = []
                for raw_item in data:
                    if "price" not in raw_item:
                        raw_item["price"] = Decimal("0.01")
                    if "id" not in raw_item:
                        raw_item["id"] = str(uuid4())
                    if "restaurant_id" not in raw_item:
                        raw_item["restaurant_id"] = 0

                    try:
                        items.append(MenuItem(**raw_item))
                    except ValidationError as e:
                        raise ValueError(f"Pydantic Validation Error: {e}")
                
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
        
    def find_by_id(self, target_id: str) -> Optional[MenuItem]:
        """Fetches all records, but only returns the single matched item."""
        all_records = self.load_all()
        return next((
            item for item in all_records 
            if str(getattr(item, "item_id", None)) == str(target_id)
        ), None)
