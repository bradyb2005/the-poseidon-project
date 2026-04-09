import uuid
import random
import string
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException

from backend.schemas.order_schema import Order, OrderCreate, OrderUpdate, OrderStatus
from backend.schemas.cart_schema import OrderItem
from backend.repositories.order_repo import OrderRepository
from backend.repositories.user_repository import UserRepository
from backend.repositories.items_repository import ItemRepository
from backend.repositories.restaurant_repository import RestaurantRepository
from backend.services.payment_service import PaymentService
from backend.schemas.payment_schema import CostBreakdown
from backend.services.loyalty_service import LoyaltyService
from backend.schemas.loyalty_schema import LoyaltyTier, LoyaltyConfig


class OrderValidate:
    @staticmethod
    def validate_delivery_postal_code(value: str) -> str:
        import re
        if value is None: return None
        regex_pattern = r"^[A-Z][0-9][A-Z]\s?[0-9][A-Z][0-9]$"
        formatted_value = value.strip().upper()
        if not re.match(regex_pattern, formatted_value):
            raise ValueError(f"'{value}' is not a valid Canadian postal code (e.g., V1V 1V1)")
        return formatted_value

    @staticmethod
    def validate_delivery_latitude(value: float) -> float:
        if value is not None and not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return value

    @staticmethod
    def validate_delivery_longitude(value: float) -> float:
        if value is not None and not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return value

class OrderService:
    def __init__(self, order_repository: OrderRepository,
                 user_repository: UserRepository,
                 items_repository: ItemRepository,
                 restaurant_repository: RestaurantRepository):
        self.repository = order_repository
        self.user_repository = user_repository
        self.items_repository = items_repository
        self.restaurant_repository = restaurant_repository
        self.loyalty_service = LoyaltyService()


    def generate_order_id(self) -> str:
        """Generates 6 random hex chars + 1 random uppercase letter. (to follow ID structure in example data)"""
        unique_hex = uuid.uuid4().hex[:6]
        random_letter = random.choice(string.ascii_uppercase)
        return f"{unique_hex}{random_letter}"

    

    def create_order(self, payload: OrderCreate) -> Order:
        payment_service = PaymentService()
        
        # Validate passed info
        try:
            lat = OrderValidate.validate_delivery_latitude(payload.delivery_latitude)
            lon = OrderValidate.validate_delivery_longitude(payload.delivery_longitude)
            pc = OrderValidate.validate_delivery_postal_code(payload.delivery_postal_code)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
            
        # Validate user's cart exists and has items
        user = self.user_repository.find_by_id(payload.customer_id)
        user_cart = user.get("cart") if user else None

        if user_cart is None:
            raise HTTPException(status_code=404, detail="User or cart not found")
        if not user_cart.get("items"):
            raise HTTPException(status_code=400, detail="Cart is empty")
            
        first_menu_item_id = user_cart.get("items")[0].get("menu_item_id")
        item = self.items_repository.find_by_id(first_menu_item_id)
        restaurant_id = item.restaurant_id if item else None

        restaurant = self.restaurant_repository.find_by_id(str(restaurant_id)) if restaurant_id else None
        
        if restaurant is None:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        if not restaurant.get("is_published"):
            raise HTTPException(status_code=400, detail="Restaurant is not published")

        # Generate order ID
        id = self.generate_order_id()
        if self.repository.find_by_id(id) is not None:
            raise HTTPException(status_code=409, detail="ID collision; retry.")
        
        subtotal = payment_service.calculate_subtotal(user_cart)
        fees = payment_service.calculate_fees_and_taxes(subtotal)
        total = payment_service.calculate_total(subtotal)

        # Create cost breakdown object

        cost_breakdown = CostBreakdown(
            subtotal=subtotal,
            delivery_fee=fees["delivery_fee"],
            service_fee=fees["service_fee"],
            tax=fees["tax"],
            total=total.total
        )
        # Apply the tier benefits (Discounts/Fee Waivers)
        user_tier = user.get("loyalty_tier", "Bronze")
        cost_breakdown_dict = cost_breakdown.model_dump(by_alias=True)
        points_earned = self.loyalty_service.calculate_earned_points(cost_breakdown_dict["_subtotal"])

        new_order_data = {
            "id": id,
            "customer_id": payload.customer_id.strip(),
            "restaurant_id": restaurant_id,
            "items": user_cart.get("items"),
            "status": OrderStatus.UNPAID,
            "order_date": datetime.now().isoformat(),
            "delivery_latitude": lat,
            "delivery_longitude": lon,
            "delivery_postal_code": pc,
            "cost_breakdown": cost_breakdown.model_dump(by_alias=True),
            "loyalty_points_earned": points_earned
        }
        
        if payload.delivery_address:
            new_order_data["delivery_address"] = payload.delivery_address.strip()
        if payload.delivery_instructions:
            new_order_data["delivery_instructions"] = payload.delivery_instructions.strip()

        # Save order to repo
        orders = self.repository.load_all()
        orders.append(new_order_data)
        self.repository.save_all(orders)

        # Clear user's cart and save order to user's order history
        users = self.user_repository.load_all()
        for user in users:
            if user.get("id") == payload.customer_id:
                user["cart"]["items"] = []
                user["orders"].append(id)
                break
        self.user_repository.save_all(users)
        
        return Order(**new_order_data)

    def update_order(self, order_id: str, payload: OrderUpdate) -> Order:
        current_order = self.repository.find_by_id(order_id)
        
        if current_order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        
        current_status = current_order.get("status")
        if current_status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
            raise HTTPException(status_code=400, detail="Cannot update a completed or cancelled order")

        try:
            if payload.status: current_order["status"] = payload.status
            if payload.delivery_latitude:
                current_order["delivery_latitude"] = OrderValidate.validate_delivery_latitude(payload.delivery_latitude)
            if payload.delivery_longitude:
                current_order["delivery_longitude"] = OrderValidate.validate_delivery_longitude(payload.delivery_longitude)
            if payload.delivery_postal_code:
                current_order["delivery_postal_code"] = OrderValidate.validate_delivery_postal_code(payload.delivery_postal_code)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        if payload.status == OrderStatus.COMPLETED:
            customer_id = current_order.get("customer_id")
            users = self.user_repository.load_all()
            
            for u in users:
                if u.get("id") == customer_id:
                    order_subtotal = current_order.get("cost_breakdown", {}).get("_subtotal", 0.0)
                    earned_points = self.loyalty_service.calculate_earned_points(order_subtotal)
                    
                    new_total_points = u.get("loyalty_points", 0) + earned_points
                    u["loyalty_points"] = new_total_points
                    
                    u["loyalty_tier"] = self.loyalty_service.evaluate_tier(new_total_points)
                    break
            
            self.user_repository.save_all(users)

        orders = self.repository.load_all()
        for i, o in enumerate(orders):
            if o.get("id") == order_id:
                orders[i] = current_order
                break

        self.repository.save_all(orders)
        return Order(**current_order)
    
def get_order_by_id(self, order_id: str) -> Order:
    """Uses the repository's find_by_id to fetch a single order."""
    order_data = self.repository.find_by_id(order_id)
    if not order_data:
        raise HTTPException(status_code=404, detail="Order not found")
    return Order(**order_data)

def get_orders_by_customer(self, customer_id: str) -> list[Order]:
    """Fetches the user's order history and retrieves each order by ID."""
    user = self.user_repository.find_by_id(customer_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    order_ids = user.get("orders", [])
    
    # Use find_by_id for each ID in the user's list
    orders = []
    for o_id in order_ids:
        o_data = self.repository.find_by_id(o_id)
        if o_data:
            orders.append(Order(**o_data))
    
    return orders