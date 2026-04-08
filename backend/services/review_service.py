# backend/services/review_service.py
from datetime import datetime, timedelta
from uuid import uuid4
from typing import List, Optional, Tuple, Dict, Any
from fastapi import HTTPException
from datetime import datetime, timedelta

from backend.schemas.review_schema import ReviewCreate, ReviewUpdate, ReviewDisplay
from backend.repositories.review_repository import ReviewRepository
from backend.repositories.restaurant_repository import RestaurantRepository
from backend.repositories.order_repository import OrderRepository

class ReviewService:
    def __init__(
        self, 
        review_repo: ReviewRepository, 
        order_repo: OrderRepository,
        restaurant_repo: RestaurantRepository
    ):
        self.review_repo = review_repo
        self.order_repo = order_repo
        self.restaurant_repo = restaurant_repo

    def submit_review(self, review_in: ReviewCreate) -> Tuple[Any, int]:
        """
        Feat9-FR1/2: The system shall allow a Customer to submit a rating and written review 
        after an order is marked as delivered
        """
        reviews = self.review_repo.load_all()
        orders = self.order_repo.load_all()

        order = next((o for o in orders if o.id == review_in.order_id), None)
        
        if not order:
            return {"error": "Order not found"}, 404

        # Order must be completed/delivered to review
        if order.status != "completed":
            return {"error": "Order must be completed/delivered to review"}, 400
    
        # One review per order
        if any(r.order_id == review_in.order_id for r in reviews):
            return {"error": "A review already exists for this order"}, 400
    
        new_review = ReviewDisplay(
            id=str(uuid4()),
            order_id=review_in.order_id,
            customer_id=review_in.customer_id,
            restaurant_id=review_in.restaurant_id,
            rating=review_in.rating,
            comment=getattr(review_in, 'comment', ""),
            created_at=datetime.now()
        )

        reviews.append(new_review)
        self.review_repo.save_all(reviews)
        return new_review, 201

    def update_review(self, review_id: str, update_in: ReviewUpdate) -> Tuple[Any, int]:
        """
        Feat9-FR4: The system shall allow a Customer to edit their review within 30 minutes
        """
        reviews = self.review_repo.load_all()
        review_idx = next((i for i, r in enumerate(reviews) if r.id == review_id), None)

        if review_idx is None:
            return {"error": "Review not found"}, 404

        target_review = reviews[review_idx]

        # 30-minute window
        if datetime.now() > target_review.created_at + timedelta(minutes=30):
            return {"error": "Review can only be edited within 30 minutes"}, 403
        if update_in.rating is not None:
            target_review.rating = update_in.rating


        comment_val = getattr(update_in, 'comment', None)
        if comment_val is not None:
            target_review.comment = comment_val

        reviews[review_idx] = target_review
        self.review_repo.save_all(reviews)
        return target_review, 200

    def delete_review(self, review_id: str) -> Tuple[Any, int]:
        """
        Feat9-FR4: Customers can delete reviews at any time
        """
        reviews = self.review_repo.load_all()
        filtered_reviews = [r for r in reviews if r.id != review_id]

        if len(filtered_reviews) == len(reviews):
            return {"error": "Review not found"}, 404

        self.review_repo.save_all(filtered_reviews)
        return {"message": "Review deleted"}, 200

    def get_restaurant_reviews(self, restaurant_id: int) -> Tuple[Dict[str, Any], int]:
        """
        Feat9-FR3: Display a restaurant’s average rating and reviews
        """
        all_reviews = self.review_repo.load_all()
        restaurant_reviews = [r for r in all_reviews if r.restaurant_id == restaurant_id]

        if not restaurant_reviews:
            return {"average_rating": 0.0, "reviews": []}, 200

        avg = sum(r.rating for r in restaurant_reviews) / len(restaurant_reviews)
        
        return {
            "average_rating": round(avg, 1),
            "reviews": restaurant_reviews
        }, 200
