# backend/tests/reviews/unit_tests/test_review_model.py
import pytest
from backend.models.review.review_model import Review


def test_review_initialization_success():
    """
    Feat3-FR3:
    Positive Functional Test: Ensure a valid review object is created.
    """
    review = Review(
        rating=5,
        restaurant_id=1,
        customer_id=123,
        customer_name="Grayson",
        comment="The burger was fantastic!"
    )
    assert review.rating == 5
    assert review.customer_name == "Grayson"
    assert review.restaurant_id == 1
    assert review.customer_id == 123
    assert review.id is None


def test_review_mandatory_fields_error():
    """
    Feat3-FR3:
    Edge Case: Ensure Python raises TypeError when
    mandatory fields are missing.
    """
    with pytest.raises(TypeError):
        # Missing customer_id and customer_name
        Review(rating=5, restaurant_id=1, comment="Should fail")


def test_review_with_empty_comment():
    """
    Feat3-FR3
    Edge Case: Verify the system handles an empty comment string
    Rating should still be visible
    """
    review = Review(
        rating=4,
        restaurant_id=1,
        customer_id=456,
        customer_name="Silent Eater",
        comment=""
    )
    assert review.comment == ""
    assert review.rating == 4


def test_review_type_integrity():
    """
    Feat3-FR3
    Functional Test: Ensure ID fields are stored as integers.
    """
    review = Review(
        rating=3,
        restaurant_id=10,
        customer_id=20,
        customer_name="Test User",
        comment="Good"
    )
    assert isinstance(review.restaurant_id, int)
    assert isinstance(review.customer_id, int)


def test_review_to_dict_for_view():
    """
    Feat3-FR3:
    Functional Test: Customer reviews are visible to users.
    """
    review = Review(
        rating=5,
        restaurant_id=1,
        customer_id=99,
        customer_name="Alice",
        comment="Perfect!"
    )
    review_data = vars(review)

    expected_keys = {"rating", "restaurant_id",
                     "customer_id", "customer_name", "comment", "id"}
    assert expected_keys.issubset(review_data.keys())
    assert review_data["customer_name"] == "Alice"
