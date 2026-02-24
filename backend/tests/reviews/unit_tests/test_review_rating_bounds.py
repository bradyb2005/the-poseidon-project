import pytest
from backend.models.review.review_model import Review


def test_rating_lower_bound():
    r = Review(id=1, user_id=1, restaurant_id=1, rating=1)
    assert r.rating == 1


def test_rating_upper_bound():
    r = Review(id=1, user_id=1, restaurant_id=1, rating=5)
    assert r.rating == 5


def test_rating_below_range():
    with pytest.raises(ValueError):
        Review(id=1, user_id=1, restaurant_id=1, rating=0)


def test_rating_above_range():
    with pytest.raises(ValueError):
        Review(id=1, user_id=1, restaurant_id=1, rating=6)