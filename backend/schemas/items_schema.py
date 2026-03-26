# backend/schemas/items_schema.py
from pydantic import BaseModel, ConfigDict, Field, field_validator
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

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: Optional[str]):
        if v is not None and not v.strip():
            raise ValueError("Name cannot be empty or whitespace")
        return v

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v: float):
        if v < 0:
            raise ValueError("Price cannot be negative")
        return v

    @field_validator("tags")
    @classmethod
    def validate_tags_content(cls, v: List[str]):
        if not all(isinstance(t, str) for t in v):
            raise TypeError("All tags must be strings")
        return v
    
    @field_validator("item_id", mode="before")
    @classmethod
    def validate_uuid(cls, v):
        if isinstance(v, UUID):
            return v
        try:
            return UUID(v)
        except (ValueError, AttributeError):
            raise ValueError("item_id must be a valid UUID string")
        
    @field_validator("tags")
    @classmethod
    def validate_and_clean_tags(cls, v: List[str]):
        """
        Standardizes tags: lowercase, no whitespace, no duplicates
        """
        if not all(isinstance(t, str) for t in v):
            raise TypeError("All tags must be strings")

        cleaned = [t.strip().lower() for t in v if t.strip()]

        return list(dict.fromkeys(cleaned))


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
