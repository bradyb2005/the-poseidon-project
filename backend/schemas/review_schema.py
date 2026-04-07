# backend/schemas/review_schema.py
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        validate_assignment=True
    )

    rating: int = Field(..., ge=1, le=5, description="Rating must be between 1 and 5")
    comment: Optional[str] = Field(default=None, max_length=1000)

class ReviewCreate(ReviewBase):
    order_id: str
    restaurant_id: int
    customer_id: str

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None

class ReviewDisplay(ReviewBase):
    id: str
    order_id: str
    customer_id: str
    restaurant_id: int
    created_at: datetime