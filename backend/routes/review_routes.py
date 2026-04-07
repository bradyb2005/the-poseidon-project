# backend/routes/review_routes.py
from fastapi import APIRouter, Depends, Response
from typing import Any

from backend.schemas.review_schema import ReviewCreate, ReviewUpdate
from backend.services.review_service import ReviewService
from backend.repositories.review_repository import ReviewRepository
from backend.repositories.order_repository import OrderRepository
from backend.repositories.restaurant_repository import RestaurantRepository

router = APIRouter(prefix="/reviews", tags=["Reviews"])

# --- Dependency Injection ---

def get_review_service():
    """Initializes the service with all required repositories."""
    return ReviewService(
        review_repo=ReviewRepository(),
        order_repo=OrderRepository(),
        restaurant_repo=RestaurantRepository()
    )

# --- Endpoints ---

@router.post("/", status_code=201)
def create_review(
    review_in: ReviewCreate, 
    service: ReviewService = Depends(get_review_service)
):
    """Feat9-FR1/2: Submit a rating and review for a completed order."""
    result, status = service.submit_review(review_in)
    
    if status != 201:
        return Response(content=result["error"], status_code=status)
    return result

@router.get("/restaurant/{restaurant_id}")
def get_restaurant_reviews(
    restaurant_id: int, 
    service: ReviewService = Depends(get_review_service)
):
    """Feat9-FR3: View a restaurant's reviews and average rating."""
    result, status = service.get_restaurant_reviews(restaurant_id)
    return result

@router.patch("/{review_id}")
def update_review(
    review_id: str, 
    update_in: ReviewUpdate, 
    service: ReviewService = Depends(get_review_service)
):
    """Feat9-FR4: Edit a review within the 30-minute window."""
    result, status = service.update_review(review_id, update_in)
    
    if status != 200:
        # result will be {"error": "..."} on failure
        return Response(content=result["error"], status_code=status)
    return result

@router.delete("/{review_id}")
def delete_review(
    review_id: str, 
    service: ReviewService = Depends(get_review_service)
):
    """Feat9-FR4: Delete a review at any time."""
    result, status = service.delete_review(review_id)
    
    if status != 200:
        return Response(content=result["error"], status_code=status)
    return result