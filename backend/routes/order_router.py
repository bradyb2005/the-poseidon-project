from fastapi import APIRouter, status, Depends
from backend.schemas.order_schema import Order, OrderCreate, OrderUpdate
from backend.services.order_service import OrderService
from backend.repositories.order_repo import OrderRepository
from backend.repositories.user_repository import UserRepository
from backend.repositories.items_repository import ItemRepository
from backend.repositories.restaurant_repository import RestaurantRepository

router = APIRouter(prefix="/orders", tags=["orders"])

def get_order_service():
    return OrderService(
        order_repository=OrderRepository(),
        user_repository=UserRepository(),
        items_repository=ItemRepository(),
        restaurant_repository=RestaurantRepository()
    )

@router.post("", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate,
    service: OrderService = Depends(get_order_service)
):
    return service.create_order(payload)

@router.put("/{order_id}", response_model=Order, status_code=status.HTTP_200_OK)
def update_order(
    order_id: str,
    payload: OrderUpdate,
    service: OrderService = Depends(get_order_service)
):
    return service.update_order(order_id, payload)