# backend/dependencies.py
from backend.repositories.restaurant_repository import RestaurantRepository
from backend.repositories.items_repository import ItemRepository
from backend.services.restaurant_service import RestaurantService
from backend.services.item_service import MenuService

# Initialize Repositories
restaurant_repo = RestaurantRepository("backend/data/restaurants.json")
item_repo = ItemRepository("backend/data/items.json") 

# Dependency Functions
def get_restaurant_service() -> RestaurantService:
    """Provides a RestaurantService instance to routes."""
    return RestaurantService(restaurant_repo)

def get_menu_service() -> MenuService:
    """Provides a MenuService instance to routes."""
    return MenuService(item_repo)