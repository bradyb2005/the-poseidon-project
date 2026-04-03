# backend/schemas/restaurant_schema.py
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

from backend.schemas.items_schema import MenuItem

class RestaurantBase(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        validate_assignment=True)

    name: Optional[str] = None
    menu: Optional[List[str]] = None
    owner_id: Optional[str] = Field(default=None, alias="_owner_id")
    open_time: Optional[int] = Field(default=None, alias="_open_time")
    close_time: Optional[int] = Field(default=None, alias="_close_time")
    address: Optional[str] = Field(default=None, alias="_address")
    phone: Optional[str] = Field(default=None, alias="_phone")
    latitude: Optional[float] = Field(default=0.0, alias="_latitude")
    longitude: Optional[float] = Field(default=0.0, alias="_longitude")
    is_published: Optional[bool] = Field(default=False, alias="_is_published")

class Restaurant(RestaurantBase):
    # Main Schema for loading JSON files

    id: int 
    name: str 
    menu: List[str]

    def get_id(self) -> int:
        return self.id

class PaginatedRestaurantResponse(BaseModel):
    """
    Specific schema for paginated homepage results of Restaurants
    """
    items: List[Restaurant]
    total_count: int
    page: int
    per_page: int
    has_next: bool
    total_pages: int

class UpdateRestaurantSchema(RestaurantBase):
    # Update schema for partial updates
    pass

class RestaurantDetailResponse(Restaurant):
    """
    Makes full menu item objects instead of just a list of strings.
    """
    full_menu_details: List[MenuItem] = Field(default_factory=list)