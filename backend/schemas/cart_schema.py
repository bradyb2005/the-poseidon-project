from decimal import Decimal

from pydantic import BaseModel, Field
from typing import List
from uuid import UUID, uuid4

class OrderItem(BaseModel):
    menu_item_id: UUID = Field(default_factory=uuid4)
    quantity: int
    price_at_time: Decimal

class Cart(BaseModel):
    customer_id: str
    items: List[OrderItem] = []