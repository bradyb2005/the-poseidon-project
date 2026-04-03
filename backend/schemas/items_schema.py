# backend/schemas/items_schema.py
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from decimal import Decimal
from uuid import uuid4, UUID

class MenuItemBase(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        validate_assignment=True
    )

    name: str = Field(..., alias="item_name")
    restaurant_id: int = Field(...)

    item_id: UUID = Field(default_factory=uuid4, alias="id")
    price: Decimal = Field(..., decimal_places=2)
    availability: bool = Field(default=True)
    tags: List[str] = Field(default_factory=list)
    description: Optional[str] = None

class MenuItem(MenuItemBase):
    """
    Have all fields from base
    """
    pass

class CreateMenuItemSchema(MenuItemBase):
    """
    Used when new menu item is added
    """
    pass

class UpdateMenuItemSchema(MenuItemBase):
    model_config = ConfigDict(populate_by_name=True)

    name: Optional[str] = Field(default=None, alias="item_name")
    restaurant_id: Optional[int] = None
    item_id: Optional[UUID] = Field(default=None, alias="id")
    price: Optional[Decimal] = None
    availability: Optional[bool] = None
    tags: Optional[List[str]] = None
    description: Optional[str] = None
