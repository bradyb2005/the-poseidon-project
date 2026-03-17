# backend/models/restaurant/menu_item_model.py
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class MenuItem:
    name:str
    price: float
    id: Optional[int] = None
    availability: bool = True
    tags: List[str] = field(default_factory=list)
    description: Optional[str] = None

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")

        if not self.name or not self.name.strip():
            raise ValueError("Name cannot be empty or whitespace")

        if not isinstance(self.tags, list) or not all(isinstance(
                t, str) for t in self.tags):
            raise TypeError("Tags must be a list of strings")
