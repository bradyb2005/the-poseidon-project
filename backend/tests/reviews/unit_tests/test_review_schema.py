# backend/tests/reviews/unit_tests/test_review_schema.py
import pytest
from pydantic import ValidationError
from datetime import datetime
from backend.schemas.review_schema import ReviewCreate, ReviewUpdate, ReviewDisplay

@pytest.fixture
def base_review_data():
    return {
        "order_id": "ORD-123",
        "restaurant_id": 1,
        "customer_id": "USER-456",
        "rating": 5,
        "comment": "Excellent service!"
    }

@pytest.fixture
def full_display_data(base_review_data):
    """
    Mocks data coming from a database for the Display schema
    """
    return {
        **base_review_data,
        "id": "REV-999",
        "created_at": datetime.now()
    }

# --- Initialization & Validation Tests ---

def test_review_create_initialization(base_review_data):
    """
    Equivalence Partitioning
    Ensures mandatory review data is correctly mapped
    """
    review = ReviewCreate(**base_review_data)
    assert review.order_id == "ORD-123"
    assert review.rating == 5
    assert review.comment == "Excellent service!"

def test_review_rating_boundary_low():
    """
    Boundary Value Analysis
    Ensures rating cannot be less than 1
    """
    with pytest.raises(ValidationError) as exc_info:
        ReviewCreate(order_id="A", restaurant_id=1, customer_id="B", rating=0)
    assert "Input should be greater than or equal to 1" in str(exc_info.value)

def test_review_rating_boundary_high():
    """
    Boundary Value Analysis
    Ensures rating cannot be greater than 5
    """
    with pytest.raises(ValidationError) as exc_info:
        ReviewCreate(order_id="A", restaurant_id=1, customer_id="B", rating=6)
    assert "Input should be less than or equal to 5" in str(exc_info.value)

def test_review_missing_mandatory_fields():
    """
    Exception Handling
    Ensures error when order_id or restaurant_id is missing
    """
    with pytest.raises(ValidationError) as exc_info:
        ReviewCreate(rating=5)
    
    assert "order_id" in str(exc_info.value)
    assert "restaurant_id" in str(exc_info.value)

# --- Update Tests ---

def test_review_partial_update():
    """
    Functional Test
    Tests that a user can update just the comment or just the rating
    """
    # Test updating comment
    update_comment = ReviewUpdate(comment="New comment")
    assert update_comment.comment == "New comment"
    assert update_comment.rating is None

    # Test updating rating
    update_rating = ReviewUpdate(rating=2)
    assert update_rating.rating == 2
    assert update_rating.comment is None

def test_review_update_invalid_rating():
    """
    Functional Test
    Ensures updates must follow the 1-5 rating rule
    """
    with pytest.raises(ValidationError):
        ReviewUpdate(rating=10)

# --- Serialization & Display Tests ---

def test_review_display_serialization(full_display_data):
    """
    Serialization
    Ensures the display schema correctly handles ID and timestamp
    """
    display = ReviewDisplay(**full_display_data)
    dump = display.model_dump()

    assert dump["id"] == "REV-999"
    assert isinstance(dump["created_at"], datetime)
    assert dump["rating"] == 5

def test_review_populate_by_alias():
    """
    Functional logic test
    Tests that the schema respects the populate_by_name config
    """

    data = {"order_id": "ORD-1", "restaurant_id": 1, "customer_id": "C-1", "rating": 4}
    review = ReviewCreate(**data)
    assert review.rating == 4