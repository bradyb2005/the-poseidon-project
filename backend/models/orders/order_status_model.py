# This file defines the OrderStatus class, representing an order status within our system.

from enum import Enum

class OrderStatus(Enum):
    UNPAID = "Unpaid"
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    READY_FOR_PICKUP = "Ready for Pickup"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"