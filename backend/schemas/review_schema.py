# backend/schemas/review_schema.py
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

# This is a dummy file to allow for review service to be tested

class ReviewBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    rating: int = Field(..., ge=1, le=5)

class ReviewCreate(ReviewBase):
    order_id: str
    restaurant_id: int
    customer_id: str
    comment: str = ""

class ReviewUpdate(BaseModel):
    rating: int

class ReviewDisplay(ReviewBase):
    id: str
    order_id: str
    customer_id: str
    restaurant_id: int
    created_at: datetime