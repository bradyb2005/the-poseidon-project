from fastapi import APIRouter, status, HTTPException, Depends, Header
from typing import List
from backend.schemas.items_schema import MenuItem, CreateMenuItemSchema, UpdateMenuItemSchema
from backend.services.item_service import MenuService
from backend.dependencies import get_menu_service

router = APIRouter(prefix="/restaurants/{restaurant_id}/items", tags=["items"])

@router.post("", status_code=status.HTTP_201_CREATED)
def add_item(
    restaurant_id: str,
    item_data: dict,
    owner_id: str = Header(...),
    service: MenuService = Depends(get_menu_service)
):
    result, code = service.add_menu_item(owner_id, restaurant_id, item_data)
    if code != 201:
        raise HTTPException(status_code=code, detail=result.get("error"))
    return result

@router.put("/{item_id}")
def update_item(
    restaurant_id: str,
    item_id: str,
    payload: UpdateMenuItemSchema,
    owner_id: str = Header(...),
    service: MenuService = Depends(get_menu_service)
):
    result, code = service.edit_menu_item(
        owner_id, 
        restaurant_id, 
        item_id, 
        payload.model_dump(exclude_unset=True)
    )
    if code != 200:
        raise HTTPException(status_code=code, detail=result.get("error"))
    return result

@router.delete("/{item_id}")
def delete_item(
    restaurant_id: str,
    item_id: str,
    owner_id: str = Header(...),
    service: MenuService = Depends(get_menu_service)
):
    result, code = service.remove_menu_item(owner_id, restaurant_id, item_id)
    if code != 200:
        raise HTTPException(status_code=code, detail=result.get("error"))
    return result