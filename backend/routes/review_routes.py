# backend/routes/review_routes.py
from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Any

from starlette import status

from starlette import status

from backend.schemas.review_schema import ReviewCreate, ReviewUpdate
from backend.services.review_service import ReviewService
from backend.repositories.review_repository import ReviewRepository
from backend.repositories.order_repository import OrderRepository
from backend.repositories.restaurant_repository import RestaurantRepository

router = APIRouter(prefix="/reviews", tags=["Reviews"])

# --- Dependency ---

def get_review_service():
    """
    Helper function to create a ReviewService instance with its required repositories.
    """
    return ReviewService(
        review_repo=ReviewRepository(),
        order_repo=OrderRepository(),
        restaurant_repo=RestaurantRepository()
    )

# --- Endpoints ---

@router.post("", status_code=status.HTTP_201_CREATED)
def create_review(
    review_data: ReviewCreate,
    service: ReviewService = Depends(get_review_service)
):
    """
    POST: Feat9-FR1/2
    Submit a rating and review for a completed order."""
    result, code = service.submit_review(review_data)
    if code != 201:
        raise HTTPException(status_code=code, detail=result.get("error"))
    return result

@router.get("/restaurant/{restaurant_id}")
def get_restaurant_reviews(
    restaurant_id: int,
    service: ReviewService = Depends(get_review_service)
):
    """
    GET: Feat9-FR3
    View a restaurant's reviews and average rating
    """
    result, code = service.get_restaurant_reviews(restaurant_id)
    if code != 200:
        raise HTTPException(status_code=code, detail=result.get("error"))
    return result

@router.put("/{review_id}")
def update_review(
    review_id: str,
    payload: ReviewUpdate,
    service: ReviewService = Depends(get_review_service)
):
    """
    PUT: Feat9-FR4
    Edit a review (30-minute window enforced in service)."""
    result, code = service.update_review(review_id, payload)
    if code != 200:
        raise HTTPException(status_code=code, detail=result.get("error"))
    return result

@router.delete("/{review_id}")
def delete_review(
    review_id: str,
    service: ReviewService = Depends(get_review_service)
):
    """
    DELETE: Feat9-FR4: Delete a review at any time
    """
    result, code = service.delete_review(review_id)
    if code != 200:
        raise HTTPException(status_code=code, detail=result.get("error"))
    return result