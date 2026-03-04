# backend/models/restaurant/menu_item_model.py
import uuid
from dataclasses import dataclass, field

@dataclass
class MenuItem:
    name: str
    price: float
    availability: bool = True
    tags: list = field(default_factory=list)
    id: int = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = None
    category: str = None

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        
        if not self.name:
            raise ValueError("Name cannot be empty")
        
        self.price = float(self.price)
        self.availability = bool(self.availability)
