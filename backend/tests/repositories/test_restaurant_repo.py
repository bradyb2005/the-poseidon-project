# backend/tests/restaurant/unit_tests/test_restaurant_repo.py
import pytest
from backend.models.restaurant.restaurant_model import Restaurant
from backend.models.restaurant.menu_item_model import MenuItem
from backend.repositories.restaurant_repository import RestaurantRepository
from backend.models.restaurant.menu_item_model import MenuItem


# --- Fixtures ---


@pytest.fixture
def restaurant_repo():
    mock_db = []
    return RestaurantRepository(mock_db)


@pytest.fixture
def owner():
    class MockOwner:
        id = 1
    return MockOwner()


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
    res_id = restaurant_repo.create_restaurant(sample_restaurant)

    sample_restaurant.address = "456 New Ave"
    sample_restaurant.is_published = True

    success = restaurant_repo.update_restaurant(sample_restaurant)

    assert success is True
    updated_data = restaurant_repo.get_by_id(res_id)
    assert updated_data["address"] == "456 New Ave"
    assert updated_data["is_published"] is True

# --- Ratings and Reviews  ---

def test_update_restaurant_rating_persistence(restaurant_repo, sample_restaurant):
    """
    Feat3-FR3: Ratings update when new reviews are added.
    Functional Test: Verifies that the repo correctly stores
    the recalculated rating.
    """
    res_id = restaurant_repo.create_restaurant(sample_restaurant)
    
    # Simulate a calculation performed in the Service layer
    new_avg = 4.5
    new_total = 10
    
    success = restaurant_repo.update_restaurant_rating(res_id, new_avg, new_total)
    
    assert success is True
    updated_data = restaurant_repo.get_by_id(res_id)
    assert updated_data["average_rating"] == 4.5
    assert updated_data["total_reviews"] == 10


def test_add_review_to_restaurant_persistence(restaurant_repo, sample_restaurant):
    """
    Feat3-FR3: Customer reviews are visible to users.
    Functional Test: Verifies that a review dictionary
    is correctly appended to the restaurant.
    """
    res_id = restaurant_repo.create_restaurant(sample_restaurant)
    review_data = {
        "rating": 5,
        "comment": "Delicious!",
        "customer_name": "Grayson",
        "customer_id": 101
    }
    
    success = restaurant_repo.add_review_to_restaurant(res_id, review_data)
    
    assert success is True
    stored_res = restaurant_repo.get_by_id(res_id)
    assert len(stored_res["reviews"]) == 1
    assert stored_res["reviews"][0]["customer_name"] == "Grayson"
    assert stored_res["reviews"][0]["rating"] == 5

def test_update_rating_nonexistent_restaurant(restaurant_repo):
    """
    Feat3-FR3: Update rating of a nonexistent restuarant.
    Edge Case: Ensure updating a rating for a missing ID fails
    """
    success = restaurant_repo.update_restaurant_rating(999, 5.0, 1)
    assert success is False


def test_add_review_nonexistent_restaurant(restaurant_repo):
    """
    Feat3-FR3: Add review to nonexistent restaurant
    Edge Case: Ensure adding a review to a missing ID fails
    """
    success = restaurant_repo.add_review_to_restaurant(999, {"rating": 5})
    assert success is False

# --- Tagging ---


def test_add_menu_item_with_tags(restaurant_repo, restaurant, sample_item):
    # Test for Feat2-FR2: Tagging Menu items
    # Functional test: Add tags to new menu item
    res_id = restaurant_repo.create_restaurant(restaurant)

    restaurant_repo.add_menu_item(res_id, sample_item)

    stored_res = restaurant_repo.get_by_id(res_id)
    stored_item = stored_res["menu"][0]
    assert "Popular" in stored_item["tags"]

# --- Updating menu ---


def test_update_menu_item(restaurant_repo, restaurant, sample_item):
    # Feat2-FR4: Verifies existing menu item data can be edited
    res_id = restaurant_repo.create_restaurant(restaurant)
    restaurant_repo.add_menu_item(res_id, sample_item)

    stored_res = restaurant_repo.get_by_id(res_id)
    stored_item_id = stored_res["menu"][0]["id"]

    updated_item = MenuItem(
        name="Premium Burger", price=15.0)
    success = restaurant_repo.update_menu_item(
        res_id, stored_item_id, updated_item)

    assert success is True
    final_data = restaurant_repo.get_by_id(res_id)
    assert final_data["menu"][0]["name"] == "Premium Burger"


def test_remove_menu_item(restaurant_repo, restaurant, sample_item):
    # FR4: Verifies an item can be removed from the menu.
    res_id = restaurant_repo.create_restaurant(restaurant)

    # Grab the ID of the first item (the burger)
    stored_res = restaurant_repo.get_by_id(res_id)
    item_id_to_remove = stored_res["menu"][0]["id"]

    success = restaurant_repo.remove_menu_item(
        res_id, item_id_to_remove)

    assert success is True
    updated_res = restaurant_repo.get_by_id(restaurant.id)
    assert len(updated_res["menu"]) == 0


def test_update_menu_item_preserves_extra_fields(
        restaurant_repo, restaurant, sample_item):
    res_id = restaurant_repo.create_restaurant(restaurant)
    restaurant_repo.add_menu_item(res_id, sample_item)

    # Simulate a field we didn't account for in the model
    stored_res = restaurant_repo.get_by_id(res_id)
    stored_res["menu"][0]["calories"] = 500
    item_id = stored_res["menu"][0]["id"]

    updated_item = MenuItem(name="Lean Burger", price=12.0)
    restaurant_repo.update_menu_item(res_id, item_id, updated_item)

    final_data = restaurant_repo.get_by_id(res_id)
    assert final_data["menu"][0]["calories"] == 500
    assert final_data["menu"][0]["name"] == "Lean Burger"

# --- Tagging ---


def test_add_menu_item_with_tags(restaurant_repo, restaurant, sample_item):
    # Test for Feat2-FR2: Tagging Menu items
    # Functional test: Add tags to new menu item
    restaurant_repo.create_restaurant(restaurant)

    restaurant_repo.add_menu_item(restaurant.id, sample_item)

    stored_res = restaurant_repo.get_by_id(restaurant.id)
    stored_item = stored_res["menu"][0]
    assert "Popular" in stored_item["tags"]

# --- Browsing and Search ---


def test_search_by_cuisine(restaurant_repo, owner):
    # Test for Feat3-FR4: Filtering search results
    # Verifies searching by cuisine returns correct results
    res1 = Restaurant(name="Sushi Place", owner=owner)
    res_id = restaurant_repo.create_restaurant(res1)

    restaurant_repo.get_by_id(res1.id)["cuisine"] = "Japanese"

    results = restaurant_repo.search_by_cuisine("Japanese")
    assert len(results) == 1
    assert isinstance(results[0]["id"], int)


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
    result = restaurant_repo.get_by_id(999)
    assert result is None


def update_nonexistent_restaurant(restaurant_repo, sample_restaurant):
    # Verifies we cannot update a nonexistent restaurant
    success = restaurant_repo.update_restaurant(sample_restaurant)
    assert success is False
