# backend/tests/restaurant/unit_tests/test_restaurant_model.py
import pytest
from backend.models.restaurant.restaurant_model import Restaurant
from unittest.mock import MagicMock


@pytest.fixture
def mock_owner():
    return MagicMock()


@pytest.fixture
def restaurant(mock_owner):
    return Restaurant(
        id=1,
        name="Testaurant",
        owner=mock_owner
    )


''' Create restaurant initialization'''


# Positive Functional Test: The restaurant model initializes correctly with attributes
def test_restaurant_initialization(restaurant, mock_owner):
    assert restaurant.id == 1
    assert restaurant.name == "Testaurant"
    assert restaurant.owner == mock_owner
    assert restaurant.open_time == ""
    assert restaurant.close_time == ""
    assert not restaurant.is_open
    assert restaurant.menu == []
    assert restaurant.reviews == []


"""Average rating"""


# Edge Case: Test rating calculation with no reviews
def test_get_average_rating_no_reviews(restaurant):
    assert restaurant.get_average_rating() == 0.0  # Empty


# Positive Functional Test: Rating calculation with multiple reviews
def test_get_average_rating_multiple_reviews(restaurant):
    restaurant.reviews = [
        MagicMock(rating=4.0),
        MagicMock(rating=5.0),
        MagicMock(rating=3.0)
    ]
    assert restaurant.get_average_rating() == 4.0


# Edge Case: Test rating round down
def test_get_average_rating_round_down(restaurant):
    restaurant.reviews = [
        MagicMock(rating=4.0),
        MagicMock(rating=4.0),
        MagicMock(rating=5.0)
    ]
    assert restaurant.get_average_rating() == 4.3


# Edge Case: Test rating round up
def test_get_average_rating_round_up(restaurant):
    restaurant.reviews = [
        MagicMock(rating=4.0),
        MagicMock(rating=5.0),
        MagicMock(rating=5.0)
    ]

    assert restaurant.get_average_rating() == 4.7


'''Update attributes'''


# Functional Test: Update hours and address
def test_update_attributes(restaurant):
    restaurant.open_time = "09:00"
    restaurant.close_time = "21:00"
    restaurant.address = "123 Test St"

    assert restaurant.open_time == "09:00"
    assert restaurant.address == "123 Test St"


# Negative Test: Test hours with empty strings and not None
def test_hours_empty_strings(restaurant):
    # Helps if we need to get length of hours and prevent NoneType errors
    assert isinstance(restaurant.open_time, str)
    assert restaurant.open_time == ""
