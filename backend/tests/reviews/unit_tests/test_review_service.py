# backend/tests/reviews/unit_tests/test_review_service.py
import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from backend.services.review_service import ReviewService
from backend.schemas.review_schema import ReviewDisplay, ReviewCreate, ReviewUpdate
from backend.schemas.order_schema import Order, OrderStatus

# --- Submit Review Tests ---

def test_submit_review_success(review_service, mock_review_repo, mock_order_repo):
    """
    Equivalence Partitioning
    Ensures a review can be submitted when the order is completed and no review exists.
    """
    mock_order_repo.load_all.return_value = [
        Order(id="ord-001", status=OrderStatus.COMPLETED, restaurant_id=1, customer_id="cust-10")
    ]
    mock_review_repo.load_all.return_value = []
    
    review_in = ReviewCreate(order_id="ord-001", restaurant_id=1, customer_id="cust-10", rating=5)
    
    result, status = review_service.submit_review(review_in)

    assert status == 201
    assert result.rating == 5
    assert result.order_id == "ord-001"
    mock_review_repo.save_all.assert_called_once()

def test_submit_review_order_not_found(review_service, mock_order_repo):
    """
    Exception Handling
    Ensures submitting a review for a non-existent order returns 404.
    """
    mock_order_repo.load_all.return_value = []
    review_in = ReviewCreate(order_id="fake-id", restaurant_id=1, customer_id="c1", rating=5)

    result, status = review_service.submit_review(review_in) 
    
    assert status == 404

def test_submit_review_order_not_completed(review_service, mock_order_repo):
    """
    Functional Test / Logic
    Ensures reviews are blocked if the order status is not 'completed'.
    """
    mock_order_repo.load_all.return_value = [
        Order(id="ord-001", status=OrderStatus.PENDING, restaurant_id=1, customer_id="c1")
    ]
    review_in = ReviewCreate(order_id="ord-001", restaurant_id=1, customer_id="c1", rating=5)

    result, status = review_service.submit_review(review_in)

    assert status == 400
    assert "Order must be completed" in result["error"]

def test_submit_review_duplicate_check(review_service, mock_review_repo, mock_order_repo, sample_review):
    """
    Equivalence Partitioning
    Ensures only one review per order id is permitted.
    """
    target_order_id = "ord-001"
    sample_review.order_id = target_order_id 

    mock_order_repo.load_all.return_value = [
        Order(id=target_order_id, status=OrderStatus.COMPLETED, restaurant_id=1, customer_id="cust-10")
    ]
    
    mock_review_repo.load_all.return_value = [sample_review]
    
    review_in = ReviewCreate(order_id=target_order_id, restaurant_id=1, customer_id="cust-10", rating=2)

    result, status = review_service.submit_review(review_in)

    assert status == 400
    assert "already exists" in result["error"]

# --- Edit Review Tests ---

def test_update_review_success_within_window(review_service, mock_review_repo, sample_review):
    """
    Functional Test
    Ensures a review can be edited if it is within the 30-minute window.
    """
    sample_review.created_at = datetime.now() - timedelta(minutes=10)
    mock_review_repo.load_all.return_value = [sample_review]
    
    update_in = ReviewUpdate(rating=1)
    result, status = review_service.update_review(sample_review.id, update_in)

    assert status == 200
    assert result.rating == 1
    mock_review_repo.save_all.assert_called_once()

def test_update_review_forbidden_after_window(review_service, mock_review_repo, sample_review):
    """
    Boundary Value Analysis
    Ensures the 30-minute edit limit is strictly enforced.
    """
    sample_review.created_at = datetime.now() - timedelta(minutes=31)
    mock_review_repo.load_all.return_value = [sample_review]
    
    update_in = ReviewUpdate(rating=1)
    result, status = review_service.update_review(sample_review.id, update_in)

    assert status == 403
    assert "30 minutes" in result["error"]

# --- Average Rating Tests ---

def test_get_restaurant_stats_calculation(review_service, mock_review_repo):
    """
    Functional Test
    Ensures the average rating is calculated correctly from the review list.
    """
    rev1 = ReviewDisplay(id="r1", order_id="o1", customer_id="c1", restaurant_id=1, rating=5, created_at=datetime.now())
    rev2 = ReviewDisplay(id="r2", order_id="o2", customer_id="c2", restaurant_id=1, rating=3, created_at=datetime.now())
    
    mock_review_repo.load_all.return_value = [rev1, rev2]

    result, status = review_service.get_restaurant_reviews(1)

    assert status == 200
    assert result["average_rating"] == 4.0
    assert len(result["reviews"]) == 2

def test_get_restaurant_stats_empty(review_service, mock_review_repo):
    """
    Boundary Value Analysis
    Ensures a restaurant with zero reviews returns an average of 0.0.
    """
    mock_review_repo.load_all.return_value = []

    result, status = review_service.get_restaurant_reviews(99)

    assert status == 200
    assert result["average_rating"] == 0.0

# --- Deletion Tests ---

def test_delete_review_success(review_service, mock_review_repo, sample_review):
    """
    Equivalence Partitioning
    Ensures a review can be deleted.
    """
    mock_review_repo.load_all.return_value = [sample_review]
    
    response, status = review_service.delete_review(sample_review.id)

    assert status == 200
    mock_review_repo.save_all.assert_called_once()
    args, _ = mock_review_repo.save_all.call_args
    assert len(args[0]) == 0
