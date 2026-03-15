# backend/models/restaurant/menu_item_model.py
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class MenuItem:
    name:str
    price: float
    tags: List[str] = field(default_factory=list)
    id: Optional[int] = 0
