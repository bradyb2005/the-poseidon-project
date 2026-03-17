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

<<<<<<< HEAD:backend/tests/restaurant/unit_tests/test_restaurant_repo.py
def test_create_restaurant_with_missing_coordinates(
        restaurant_repo, owner):
    """
    Feat3-FR1: Ensures that if the restaurant object
    lacks lat/long attributes,
    the repo defaults them to 0.0 instead of crashing.
    """
    minimal_res = Restaurant(name="Minimal", owner=owner)
    # Manually remove attributes if they exist to simulate an old
    # model version
    if hasattr(minimal_res, 'latitude'):
        del minimal_res.latitude
    if hasattr(minimal_res, 'longitude'):
        del minimal_res.longitude

    res_id = restaurant_repo.create_restaurant(minimal_res)
    stored_data = restaurant_repo.get_by_id(res_id)

    assert stored_data["latitude"] == 0.0
    assert stored_data["longitude"] == 0.0

# --- Coordinates ---


def test_repository_safety_net_forces_false_publication(
        restaurant_repo, sample_restaurant):
    """
    Safety Net: Verifies that update_restaurant overrides is_published to False
    if latitude or longitude are 0.0.
    """
    # 1. Create the restaurant in the repo first
    res_id = restaurant_repo.create_restaurant(sample_restaurant)

    # 2. Set coordinates to 0.0 and attempt to publish
    sample_restaurant.latitude = 0.0
    sample_restaurant.longitude = 0.0
    sample_restaurant.is_published = True

    # 3. Call the update method
    restaurant_repo.update_restaurant(sample_restaurant)

    # 4. Assert that the safety net caught it
    updated_data = restaurant_repo.get_by_id(res_id)
    assert updated_data["is_published"] is False
    assert updated_data["latitude"] == 0.0

=======
>>>>>>> abc67dd9fd17c71b01ce00104e19d68b1e308e7b:backend/tests/repositories/test_restaurant_repo.py
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
    # (e.g., from a future DB migration)
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

# --- Tagging ---


def test_add_menu_item_with_tags(restaurant_repo, restaurant, sample_item):
    # Test for Feat2-FR2: Tagging Menu items
    # Functional test: Add tags to new menu item
    restaurant_repo.create_restaurant(restaurant)

    restaurant_repo.add_menu_item(restaurant.id, sample_item)

    stored_res = restaurant_repo.get_by_id(restaurant.id)
    stored_item = stored_res["menu"][0]
    assert "Popular" in stored_item["tags"]

# --- Updating menu ---


def test_update_menu_item(restaurant_repo, restaurant, sample_item):
    # Feat2-FR4: Verifies existing menu item data can be edited
    restaurant_repo.create_restaurant(restaurant)

    stored_res = restaurant_repo.get_by_id(restaurant.id)
    stored_item_id = stored_res["menu"][0]["id"]  # The burger from conftest

    updated_item = MenuItem(
        name="Premium Burger", price=15.0, id=stored_item_id)
    success = restaurant_repo.update_menu_item(
        restaurant.id, stored_item_id, updated_item)

    assert success is True
    final_data = restaurant_repo.get_by_id(restaurant.id)
    assert final_data["menu"][0]["name"] == "Premium Burger"


def test_remove_menu_item(restaurant_repo, restaurant, sample_item):
    # FR4: Verifies an item can be removed from the menu.
    restaurant_repo.create_restaurant(restaurant)

    # Grab the ID of the first item (the burger)
    stored_res = restaurant_repo.get_by_id(restaurant.id)
    item_id_to_remove = stored_res["menu"][0]["id"]

    success = restaurant_repo.remove_menu_item(
        restaurant.id, item_id_to_remove)

    assert success is True
    updated_res = restaurant_repo.get_by_id(restaurant.id)
    assert len(updated_res["menu"]) == 0

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
