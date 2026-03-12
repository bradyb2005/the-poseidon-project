# backend/models/restaurant/menu_item_model.py
from dataclasses import dataclass, field
from typing import List
import uuid

@dataclass
class MenuItem:
    name:str
    price: float
    tags: List[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
