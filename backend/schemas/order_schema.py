from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum
from backend.schemas.cart_schema import OrderItem
from backend.schemas.payment_schema import CostBreakdown

class OrderStatus(str, Enum):
    UNPAID = "unpaid"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    READY_FOR_PICKUP = "ready_for_pickup"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Order(BaseModel):
    id: str
    customer_id: str
    restaurant_id: int
    items: List[OrderItem]
    status: OrderStatus
    order_date: datetime
    cost_breakdown: CostBreakdown
    delivery_address: Optional[str] = None
    delivery_latitude: float
    delivery_longitude: float
    delivery_postal_code: str
    delivery_instructions: Optional[str] = None
    # ADDED IN EXTRA FEATURE: Loyalty Program
    loyalty_points_earned: int = 0

class OrderCreate(BaseModel):
    customer_id: str
    restaurant_id: int
    delivery_address: Optional[str] = None
    delivery_latitude: float
    delivery_longitude: float
    delivery_postal_code: str
    delivery_instructions: Optional[str] = None

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    delivery_address: Optional[str] = None
    delivery_latitude: Optional[float] = None
    delivery_longitude: Optional[float] = None
    delivery_postal_code: Optional[str] = None
    delivery_instructions: Optional[str] = None