# backend/schemas/restaurant_schema.py
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing import List, Optional

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

    @field_validator("open_time", "close_time")
    @classmethod
    def validate_times(cls, v: Optional[int]):
        if v is not None and not (0 <= v <= 2400):
            raise ValueError("Invalid time format (0-2400)")
        return v

    @field_validator("latitude", "longitude")
    @classmethod
    def validate_coords(cls, v: float, info):
        if info.field_name == "latitude" and not (-90 <= v <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if info.field_name == "longitude" and not (-180 <= v <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return v
    
    @model_validator(mode="after")
    def validate_business_hours(self) -> "RestaurantBase":
        if self.open_time is not None and self.close_time is not None:
            if self.open_time >= self.close_time:
                raise ValueError("open_time must be before close_time")
        return self


class Restaurant(RestaurantBase):
    # Main Schema for loading JSON files

    id: int 
    name: str 
    menu: List[str]


class UpdateRestaurantSchema(RestaurantBase):
    # Update schema for partial updates
    pass