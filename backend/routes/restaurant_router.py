# backend/routes/restaurant_router.py
from fastapi import APIRouter, status, HTTPException, Depends
from typing import List, Dict
from backend.schemas.restaurant_schema import Restaurant, UpdateRestaurantSchema
from backend.services.restaurant_service import RestaurantService
from backend.repositories.restaurant_repository import RestaurantRepository

repo = RestaurantRepository("backend/data/restaurants.json")
service = RestaurantService(repo)

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

# --- Get Methods ---

@router.get("", response_model=List[Dict])
def get_restaurants():
    """
    GET: Retrieve all restaurants via load all from service
    """
    return service.get_all_published()

@router.get("/{restaurant_id}")
def get_restaurant(restaurant_id: str):
    """
    GET: Get a specific restaurant by ID
    """
    result, code = service.get_filtered_view(restaurant_id, "customer")
    if code == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    if code == 403:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Restaurant unavailable")
    return result

# --- Post Methods ---

@router.post("/{restaurant_id}/owner", status_code=status.HTTP_200_OK)
def post_assign_owner(restaurant_id: str, owner_id: str):
    """
    POST: Assign an owner to a restaurant using string IDs
    """
    result, code = service.assign_owner_to_restaurant(restaurant_id, owner_id)
    
    if code == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result["error"])
        
    return result

@router.post("/{restaurant_id}/publish", status_code=status.HTTP_200_OK)
def post_publish_restaurant(restaurant_id: str):
    """
    POST: Publish a restaurant and checks through service
    """
    result, code = service.publish_restaurant(restaurant_id)
    
    if code == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    if code == 400:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get("error"))
        
    return result

# --- Put Methods ---

@router.put("/{restaurant_id}", response_model=Dict)
def put_restaurant(restaurant_id: str, payload: UpdateRestaurantSchema):
    """
    PUT: Update restaurant details using the update schema
    """
    result, code = service.update_restaurant_details(restaurant_id, payload.model_dump(exclude_unset=True))

    if code == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    if code == 400:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get("error"))

    return result
