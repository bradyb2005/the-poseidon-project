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

    def generate_order_id(self) -> str:
        """Generates 6 random hex chars + 1 random uppercase letter. (to follow ID structure in example data)"""
        unique_hex = uuid.uuid4().hex[:6]
        random_letter = random.choice(string.ascii_uppercase)
        return f"{unique_hex}{random_letter}"

    def create_order(self, payload: OrderCreate) -> Order:
        users = self.user_repository.load_all()
        orders = self.repository.load_all()
        items = self.items_repository.load_all()
        restaurants = self.restaurant_repository.load_all()
        
        # Validate passed info
        try:
            lat = OrderValidate.validate_delivery_latitude(payload.delivery_latitude)
            lon = OrderValidate.validate_delivery_longitude(payload.delivery_longitude)
            pc = OrderValidate.validate_delivery_postal_code(payload.delivery_postal_code)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
            
        # Validate user's cart exists and has items
        user_cart = next((u.get("cart") for u in users if u.get("id") == payload.customer_id), None)
        if user_cart is None:
            raise HTTPException(status_code=404, detail="User or cart not found")
        if not user_cart.get("items"):
            raise HTTPException(status_code=400, detail="Cart is empty")
            
        first_menu_item_id = user_cart.get("items")[0].get("menu_item_id")
        restaurant_id = next((i.get("restaurant_id") for i in items if i.get("item_id") == first_menu_item_id), None)
        restaurant = next((r for r in restaurants if r.get("id") == restaurant_id), None)
        
        if restaurant is None:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        if not restaurant.get("is_published"):
            raise HTTPException(status_code=400, detail="Restaurant is not published")

        # Generate order ID
        id = self.generate_order_id()
        if any(it.get("id") == id for it in orders):  # extremely unlikely, but consistent check
            raise HTTPException(status_code=409, detail="ID collision; retry.")

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
            # TODO: Feat7 - Integrate fee calculators for these:
            "cost_breakdown": 0
        }
        
        if payload.delivery_address:
            new_order_data["delivery_address"] = payload.delivery_address.strip()
        if payload.delivery_instructions:
            new_order_data["delivery_instructions"] = payload.delivery_instructions.strip()

        # Save order to repo
        orders = self.repository.load_all()
        orders.append(new_order_data)
        self.repository.save_all(orders)

        # Clear user's cart
        for user in users:
            if user.get("id") == payload.customer_id:
                user["cart"]["items"] = []
                break
        self.user_repository.save_all(users)
        
        return Order(**new_order_data)

    def update_order(self, order_id: str, payload: OrderUpdate) -> Order:
        orders = self.repository.load_all()
        order_idx = next((i for i, o in enumerate(orders) if o.get("id") == order_id), None)
        
        if order_idx is None:
            raise HTTPException(status_code=404, detail="Order not found")

        current_order = orders[order_idx]

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

        self.repository.save_all(orders)
        return Order(**current_order)