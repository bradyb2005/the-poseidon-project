from pydantic import BaseModel
from typing import List
from uuid import UUID

class OrderItem(BaseModel):
    menu_item_id: UUID
    quantity: int
    price_at_time: float

class Cart(BaseModel):
    customer_id: str
    items: List[OrderItem] = []