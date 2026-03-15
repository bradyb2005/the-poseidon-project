import pytest
from backend.models.review.review_model import Review


def test_create_review():
    r = Review(id=1, user_id=2, restaurant_id=3, rating=5, comment="Great")

    assert r.rating == 5
    assert r.comment == "Great"


def test_invalid_rating():
    with pytest.raises(ValueError):
        Review(id=1, user_id=1, restaurant_id=1, rating=10)


def test_update_rating():
    r = Review(id=1, user_id=2, restaurant_id=3, rating=4)
    r.update_rating(2)
    assert r.rating == 2


def test_to_dict():
    r = Review(id=1, user_id=2, restaurant_id=3, rating=5, comment="Nice")
    d = r.to_dict()

    assert d["rating"] == 5
    assert d["comment"] == "Nice"