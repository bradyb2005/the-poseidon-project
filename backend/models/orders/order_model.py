# This file defines the Order class, representing an order within our system.

from __future__ import annotations
from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class Order:
    """
    Order Model (based on UML diagram)

    UML Attributes:
      - id: int
      - customer: Customer
      - restaurant: Restaurant
      - items: List[OrderItem]
      - status: OrderStatus
      - order_date: datetime
      - fullfillment_request: List[FullfillmentRequest]
      - total_price: float

    In our code:
     - we will use the same attributes as the UML class diagram, but we will use type hints to indicate the types of the attributes.
     - we will include the same methods as the UML class diagram, but we will implement them with actual code instead of just method signatures.
    """

    id: int
    customer: "Customer" #TODO: update this to match the actual Customer class once defined
    restaurant: "Restaurant" #TODO: update this to match the actual Restaurant class once defined
    items: List["OrderItem"] #TODO: update this to match the actual OrderItem class once defined
    status: "OrderStatus" #TODO: update this to match the actual OrderStatus class once defined
    order_date: datetime
    fullfillment_request: List["FullfillmentRequest"] #TODO: update this to match the actual FullfillmentRequest class once defined
    total_price: float

    def __post_init__(self) -> None:
        """
        This runs right after the dataclass constructor, which means it runs after we create an Order object.
        We use it to validate that the Order object is not invalid.
        """
        if not isinstance(self.id, int) or self.id < 0:
            raise ValueError("id must be a non-negative integer")

        if not isinstance(self.customer, "Customer"):
            raise ValueError("customer must be a Customer object")

        if not isinstance(self.restaurant, "Restaurant"):
            raise ValueError("restaurant must be a Restaurant object")

        if not isinstance(self.items, list) or not all(isinstance(item, "OrderItem") for item in self.items):
            raise ValueError("items must be a list of OrderItem objects")

        if not isinstance(self.status, "OrderStatus"):
            raise ValueError("status must be an OrderStatus object")

        if not isinstance(self.order_date, datetime):
            raise ValueError("order_date must be a datetime object")

        if not isinstance(self.fullfillment_request, list) or not all(isinstance(request, "FullfillmentRequest") for request in self.fullfillment_request):
            raise ValueError("fullfillment_request must be a list of FullfillmentRequest objects")

        if not isinstance(self.total_price, (int, float)) or self.total_price < 0:
            raise ValueError("total_price must be a non-negative number")

    def submit_order(self) -> None:
        self.status = "Submitted" #TODO: update this to match the actual OrderStatus enum once defined

    def cancel_order(self) -> None:
        self.status = "Cancelled" #TODO: update this to match the actual OrderStatus enum once defined
    
    def update_status(self, new_status: "OrderStatus") -> None:
        self.status = new_status