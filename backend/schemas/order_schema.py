# backend/schemas/order_schema.py
from pydantic import BaseModel, ConfigDict
from enum import Enum

# This is a dummy file to allow for review service to be tested

class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Order(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    status: OrderStatus
    restaurant_id: int
    customer_id: str