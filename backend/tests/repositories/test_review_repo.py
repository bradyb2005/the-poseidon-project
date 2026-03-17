import pytest
from backend.models.review.review_model import Review
from backend.repositories.review_repository import ReviewRepository


@pytest.fixture
def review_repo():
    return ReviewRepository([])


def test_add_and_get_reviews(review_repo):
    """
    Feat3-FR3:
    Functional test: Ensure you can add a review and
    it will be saved
    """
    rev = Review(rating=5, restaurant_id=1, customer_id=101, 
                 customer_name="Grayson", comment="Great!")

    review_id = review_repo.add_review(rev)

    # Verify it was saved
    results = review_repo.get_reviews_by_restaurant(1)
    assert len(results) == 1
    assert results[0]["id"] == review_id
    assert results[0]["customer_name"] == "Grayson"


def test_get_reviews_filters_by_restaurant(review_repo):
    """
    Feat3-FR3:
    Functional test: Tests filtering by reviews
    """
    review_repo.add_review(Review(5, 1, 101, "User1", "Nice"))
    review_repo.add_review(Review(1, 2, 102, "User2", "Bad"))

    # Should only get 1 review for restaurant ID 1
    results = review_repo.get_reviews_by_restaurant(1)
    assert len(results) == 1
    assert results[0]["restaurant_id"] == 1


def test_get_reviews_for_restaurant_with_no_data(review_repo):
    """
    Feat3-FR3:
    Edge Case: Ensure that if a restaurant has no reviews, the repo 
    returns an empty list
    """
    results = review_repo.get_reviews_by_restaurant(999) # Non-existent ID
    assert isinstance(results, list)
    assert len(results) == 0


def test_get_reviews_multiple_entries_integrity(review_repo):
    """
    Feat3-FR3:
    Edge Case: Verify that the repo retrieves ALL reviews for a restaurant,
    not just the most recent one
    """
    restaurant_id = 1
    for i in range(5):
        rev = Review(rating=5, restaurant_id=restaurant_id, customer_id=i, 
                     customer_name=f"User{i}", comment="Great")
        review_repo.add_review(rev)

    results = review_repo.get_reviews_by_restaurant(restaurant_id)
    assert len(results) == 5


def test_reviews_do_not_leak_between_restaurants(review_repo):
    """
    Feat3-FR3:
    Edge Case: Ensure the filter strictly separates
    reviews by restaurant_id.
    """
    review_repo.add_review(Review(5, 1, 101, "A", "Good"))
    review_repo.add_review(Review(1, 2, 102, "B", "Bad"))

    res1_reviews = review_repo.get_reviews_by_restaurant(1)
    ratings = [r["rating"] for r in res1_reviews]

    assert 1 not in ratings
    assert len(res1_reviews) == 1
