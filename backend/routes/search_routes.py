# backend/routes/search_routes.py
from fastapi import APIRouter, status, HTTPException, Query
from typing import List, Dict, Optional
from backend.services.search_service import SearchService
from backend.repositories.restaurant_repository import RestaurantRepository
from backend.repositories.items_repository import ItemRepository 
from backend.schemas.items_schema import PaginatedItemResponse
from backend.schemas.restaurant_schema import PaginatedRestaurantResponse, RestaurantDetailResponse

restaurant_repo = RestaurantRepository("backend/data/restaurants.json")
item_repo = ItemRepository("backend/data/items.json")
service = SearchService(restaurant_repo, item_repo)

router = APIRouter(prefix="/search", tags=["search"])

# --- Get Methods ---

@router.get("", response_model=PaginatedItemResponse)
def get_search(
    q: Optional[str] = Query(None, description="Search keyword for items or tags"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page")
):
    """
    GET: Search for menu items by keyword (name or tags)
    Only returns items from published restaurants
    """
    return service.search_by_keyword(q, page=page, limit=limit)

@router.get("/homepage", response_model=PaginatedRestaurantResponse)
def get_homepage(
    q: Optional[str] = None,
    page: int = 1, 
    limit: int = 20):
    """
    GET: Feat3-FR1 - Browse restaurants for homepage with optional search query
    """
    return service.browse_homepage(page=page, limit=limit)
 
@router.get("/nearby", response_model=List[Dict])
def get_nearby(
    lat: float = Query(..., description="Latitude of the user (-90 to 90)", ge=-90, le=90),
    lon: float = Query(..., description="Longitude of the user (-180 to 180)", ge=-180, le=180)):
    """
    GET: Returns restaurants sorted by distance from the provided lat/lon
    Calculated in Kilometers
    """
    return service.get_nearby_restaurants(lat, lon)

@router.get("/featured", response_model=List[Dict])
def get_featured():
    """
    GET: Feat3-FR3 - Returns a selection of featured menu items
    """
    return service.get_homepage_featured()

@router.get("/details/{restaurant_id}", response_model=RestaurantDetailResponse)
def get_restaurant_details(restaurant_id: int):
    """
    GET: Feat3-FR3 - Fetches a specific restaurant and its full menu
    """
    result = service.get_restaurant_details(restaurant_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Restaurant not found or is not published"
        )
    return result

@router.get("/landing", response_model=Dict)
def get_full_landing_page():
    """
    GET: Homepage landing data - combines featured items and restaurant list
    It returns featured items AND the restaurant list in one go.
    """
    return {
        "featured": service.get_homepage_featured(),
        "restaurants": service.browse_homepage(page=1, limit=10),
        "message": "Welcome to Poseidon"
    }