# backend/routes/search_routes.py
from fastapi import APIRouter, status, HTTPException
from typing import List, Dict, Optional
from backend.services.search_service import SearchService
from backend.repositories.restaurant_repository import RestaurantRepository
from backend.repositories.items_repository import ItemRepository 


restaurant_repo = RestaurantRepository("backend/data/restaurants.json")
item_repo = ItemRepository("backend/data/items.json")
service = SearchService(restaurant_repo, item_repo)

router = APIRouter(prefix="/search", tags=["search"])

# --- Get Methods ---

@router.get("", response_model=List[Dict])
def get_search(q: Optional[str] = None):
    """
    GET: Search for menu items by keyword (name or tags)
    Only returns items from published restaurants
    """
    if not q or not q.strip():
        return []
    return service.search_by_keyword(q)

@router.get("/homepage", response_model=List[Dict])
def get_homepage():
    """
    GET: Feat3-FR3 - Returns all published restaurants for the homepage list
    """
    return service.browse_homepage()

@router.get("/featured", response_model=List[Dict])
def get_featured():
    """
    GET: Feat3-FR3 - Returns a selection of featured menu items
    """
    return service.get_homepage_featured()

@router.get("/details/{restaurant_id}", response_model=Dict)
def get_restaurant_details(restaurant_id: str):
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