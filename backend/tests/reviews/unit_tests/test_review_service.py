from backend.models.review.review_model import Review


def test_update_comment():
    r = Review(id=1, user_id=1, restaurant_id=1, rating=4)
    r.update_comment("Updated comment")

    assert r.comment == "Updated comment"


def test_update_rating_valid():
    r = Review(id=1, user_id=1, restaurant_id=1, rating=3)
    r.update_rating(5)

    assert r.rating == 5