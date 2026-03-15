# backend/models/restaurant/menu_item_model.py
from dataclasses import dataclass, field
from typing import List


@dataclass
class MenuItem:
    name: str
    price: float
    id: int = 0
    tags: List[str] = field(default_factory=list)
