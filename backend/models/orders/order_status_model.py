# This file defines the OrderStatus class, representing an order status within our system.

from enum import Enum

class OrderStatus(Enum):
    PROCESSING = "Processing"
    IN_PROGRESS = "In Progress"
    COMPLETE = "Complete"