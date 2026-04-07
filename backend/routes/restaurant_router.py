# backend/routes/restaurant_router.py
from fastapi import APIRouter, status, HTTPException, Depends
from typing import List, Dict
from backend.schemas.restaurant_schema import Restaurant, UpdateRestaurantSchema
from backend.services.restaurant_service import RestaurantService
from backend.repositories.restaurant_repository import RestaurantRepository

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

def get_restaurant_service():
    """
    Override this in tests to provide a mock service
    """
    repo = RestaurantRepository("backend/data/restaurants.json")
    return RestaurantService(repo)

# --- Get Methods ---

@router.get("", response_model=List[Dict])
def get_restaurants(service: RestaurantService = Depends(get_restaurant_service)):
    """
    GET: Retrieve all restaurants via load all from service
    """
    return service.get_all_published()

@router.get("/{restaurant_id}")
def get_restaurant(
    restaurant_id: str,
    service: RestaurantService = Depends(get_restaurant_service)):
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
def post_assign_owner(
    restaurant_id: str,
    owner_id: str,
    service: RestaurantService = Depends(get_restaurant_service)):
    """
    POST: Assign an owner to a restaurant using string IDs
    """
    result, code = service.assign_owner_to_restaurant(restaurant_id, owner_id)
    
    if code == 404:
        raise HTTPException(status_code=404, detail=result.get("error", "Not Found"))
        
    return result

@router.post("/{restaurant_id}/publish", status_code=status.HTTP_200_OK)
def post_publish_restaurant(
    restaurant_id: str,
    service: RestaurantService = Depends(get_restaurant_service)):
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
def put_restaurant(
    restaurant_id: str,
    payload: UpdateRestaurantSchema,
    service: RestaurantService = Depends(get_restaurant_service)):
    """
    PUT: Update restaurant details using the update schema
    """
    result, code = service.update_restaurant_details(restaurant_id, payload.model_dump(exclude_unset=True))

    if code == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    if code == 400:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get("error"))

    return result

@router.get("", response_model=List[Dict])
def get_restaurants(service: RestaurantService = Depends(get_restaurant_service)):
    data = service.get_all_published()
    print(f"DEBUG: Data found: {data}") # Check your terminal output
    return data