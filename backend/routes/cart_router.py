from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict
from backend.services.cart_service import CartService
from backend.schemas.cart_schema import OrderItemCreate, OrderItemUpdate

router = APIRouter(prefix="/cart", tags=["cart"])


def get_cart_service():
    return CartService()

@router.post("/{customer_id}/items", status_code=status.HTTP_200_OK)
def add_item_to_cart(
    customer_id: str,
    payload: OrderItemCreate,
    service: CartService = Depends(get_cart_service)
):
    result, code = service.add_to_cart(customer_id, payload.menu_item_id, payload.quantity)
    
    if code == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.get("error"))
    if code == 400:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get("error"))
        
    return result

@router.put("/{customer_id}/items/{menu_item_id}", status_code=status.HTTP_200_OK)
def update_cart_item_quantity(
    customer_id: str,
    menu_item_id: str,
    payload: OrderItemUpdate,
    service: CartService = Depends(get_cart_service)
):
    result, code = service.update_quantity(customer_id, menu_item_id, payload.new_quantity)
    
    if code == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.get("error"))
        
    return result

@router.delete("/{customer_id}/items/{menu_item_id}", status_code=status.HTTP_200_OK)
def remove_cart_item(
    customer_id: str,
    menu_item_id: str,
    service: CartService = Depends(get_cart_service)
):
    result, code = service.remove_from_cart(customer_id, menu_item_id)
    
    if code == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.get("error"))
        
    return result

@router.delete("/{customer_id}", status_code=status.HTTP_200_OK)
def clear_customer_cart(
    customer_id: str,
    service: CartService = Depends(get_cart_service)
):
    result, code = service.clear_cart(customer_id)
    
    if code == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.get("error"))
        
    return result