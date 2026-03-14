# backend/models/restaurant/menu_item_model.py
from dataclasses import dataclass, field

@dataclass
class MenuItem:
    name: str
    price: float
    id: int = 0
