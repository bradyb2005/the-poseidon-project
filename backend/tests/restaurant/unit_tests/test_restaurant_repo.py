# backend/tests/restaurant/unit_tests/test_restaurant_repo.py
import pytest
from backend.models.restaurant.restaurant_model import Restaurant
from backend.repositories.restaurant_repository import RestaurantRepository

# --- Fixtures ---


@pytest.fixture
def restaurant_repo():
    mock_db = []
    return RestaurantRepository(mock_db)


@pytest.fixture
def sample_restaurant(owner):
    return Restaurant(
        name="Testaurant",
        owner=owner,
        address="123 Test st",
        phone="555-555-5555",
        open_time=900,
        close_time=2200
    )

# --- Restaurant Information ---


def test_create_restaurant(restaurant_repo, sample_restaurant):
    # Test for Feat2-FR1: Storing information
    # Verifies data passed to repo is saved

    result = restaurant_repo.create_restaurant(sample_restaurant)
    assert result == sample_restaurant.id
    assert len(restaurant_repo.get_all_restaurants()) == 1


def test_update_restaurant(restaurant_repo, sample_restaurant):
    # Test for Feat2-FR3: Correct and accurate information
    # Verifies updates to restaurant data are saved
    restaurant_repo.create_restaurant(sample_restaurant)

    sample_restaurant.address = "456 New Ave"
    sample_restaurant.is_published = True

    success = restaurant_repo.update_restaurant(sample_restaurant)

    assert success is True
    updated_data = restaurant_repo.get_by_id(sample_restaurant.id)
    assert updated_data["address"] == "456 New Ave"

# --- Browsing and Search ---


def test_search_by_cuisine(restaurant_repo, owner):
    # Test for Feat3-FR4: Filtering search results
    # Verifies searching by cuisine returns correct results
    res1 = Restaurant(name="Sushi Place", owner=owner)
    restaurant_repo.create_restaurant(res1)

    restaurant_repo.get_by_id(res1.id)["cuisine"] = "Japanese"

    results = restaurant_repo.search_by_cuisine("Japanese")
    assert len(results) == 1
    assert results[0]["name"] == "Sushi Place"


"""
May use this in Feat3, commented out to avoid errors
def test_pagination(restaurant_repo):
    # Test for Feat3-FR5: Paginated results
    # Verifies pagination returns correct number of results
    for i in range(10):
        restaurant_repo.create_restaurant({"name": f"Restaurant {i}",
        "cuisine": "Test"})

    page1 = restaurant_repo.get_restaurants_paginated(page=1, limit=5)
    page2 = restaurant_repo.get_restaurants_paginated(page=2, limit=5)

    assert len(page1) == 5
    assert len(page2) == 5

"""

# Edge case: Get non-existent restaurant


def test_get_nonexistent_restaurant(restaurant_repo):
    # Verifies getting a non-existent restaurant returns None
    result = restaurant_repo.get_by_id("999")
    assert result is None


def update_nonexistent_restaurant(restaurant_repo, sample_restaurant):
    # Verifies we cannot update a nonexistent restaurant
    success = restaurant_repo.update_restaurant(sample_restaurant)
    assert success is False
