# backend/tests/restaurant/unit_tests/test_menu_item_model.py
import pytest
from unittest.mock import MagicMock
from backend.models.user.customer import Customer
from backend.services.restaurant_service import RestaurantService
from backend.models.restaurant.restaurant_model import Restaurant
from backend.models.user.restaurant_owner_model import RestaurantOwner

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return RestaurantService(mock_repo)

@pytest.fixture
def customer():
    return Customer(
        id=2, 
        username="Newbie",
        password_hash="hashed_pw",
        email="customer@mail.com",
        latitude=0.0,
        longitude=0.0
    )

# ---  Registration and roles---

def test_create_restaurant_as_owner(service, owner, mock_repo):
    # Positive functionality test: Owner can create a restaurant
    data = {"name": "New Spot", "location": "789 Road"}
    mock_repo.save.return_value = 123
    result = service.register_restaurant(owner, data)

    assert result["success"] is True
    assert result["restaurant_id"] == 123
    assert mock_repo.save.called

def test_create_restaurant_as_customer(service, customer):
    # Edge case: A customer should not be able to create a restaurant
    data = {"name": "Fake place", "location": "None"}

    result = service.register_restaurant(customer, data)

    assert result["success"] == False
    assert "unauthorized" in result["error"]

# --- Publishing logic ---


def test_publish_restaurant_success(service, mock_repo, restaurant):
    # Positive Functional test: Publish when all required fields are filled
    # Complete partial conftest
    restaurant.id = 1
    restaurant.address = "123 Test Ave"
    restaurant.phone = "555-555-5555"
    restaurant.open_time = 900
    restaurant.close_time = 2200

    mock_repo.get_by_id.return_value = restaurant

    result = service.publish_restaurant(restaurant.id)

    assert result["success"] is True
    assert restaurant.is_published is True

def test_publish_restaurant_fails_missing_info(service, mock_repo, restaurant):
    # Edge test: Throw error if incomplete since our comftest doesn't have address/phone/time...
    restaurant.id = 1
    mock_repo.get_by_id.return_value = restaurant
    result = service.publish_restaurant(restaurant.id)

    assert result["success"] is False
    assert "is required" in result["error"]
    assert restaurant.is_published is False


def test_publish_fails_without_menu(service, mock_repo, restaurant):
    # Negative Edge Case: Cannot publish without menu
    restaurant.id = 1
    restaurant.address = "123 Test Ave"
    restaurant.phone = "555-555-5555"
    restaurant.open_time = 900
    restaurant.close_time = 2200
    # Clear menu
    restaurant.menu = []
    mock_repo.get_by_id.return_value = restaurant

    result = service.publish_restaurant(restaurant.id)

    assert result["success"] is False
    assert "menu cannot be empty" in result["error"]

# --- Feature 2 test ---

def test_admin_customer_perspective(service, mock_repo, restaurant):
    # Positive Functional Test: Tests that different perspectives can be used
    # Customer perspective should not see unpublished restaurant
    restaurant.address = "123 Test Ave"
    restaurant.phone = "555-555-5555"
    restaurant.open_time = 900
    restaurant.close_time = 2200
    restaurant.menu = ["Item"]

    mock_repo.get_by_id.return_value = restaurant

    # Ensure customer cant see restaurant before it is published
    assert restaurant.get_view("Customer") is None

    # Publish
    service.publish_restaurant(restaurant.id)

    # Check to see if customer can view it
    view = restaurant.get_view("Customer")
    assert view is not None
    assert view["name"] == "John's Diner"


# --- Nearby search ---

def test_get_nearby_restaurants_filtering_and_sorting(service, mock_repo, customer):
    """
    Feat3-FR1:
    Functional test: Test that restaurants are filtered
    by radius and sorted by distance
    """
    # Setup Mock Data
    mock_data = [
        {"id": 1, "name": "Close Cafe", "latitude": 0.01, "longitude": 0.01, "is_published": True},
        {"id": 2, "name": "Far Food", "latitude": 0.1, "longitude": 0.1, "is_published": True},
        {"id": 3, "name": "Out of Bounds", "latitude": 1.0, "longitude": 1.0, "is_published": True}
    ]
    mock_repo.get_all_restaurants.return_value = mock_data

    # Execution (Radius 20km)
    results = service.get_nearby_restaurants(customer, radius_km=20.0)

    assert len(results) == 2
    assert results[0]["name"] == "Close Cafe"


def test_get_nearby_restaurants_ignores_unpublished(service, mock_repo, customer):
    """
    Feat3-FR1:
    Negative functional test: Test that even if a
    restaurant is close, it's hidden if not published
    """

    # Close but unpublished
    mock_data = [{"id": 1, "name": "Ghost Kitchen", "latitude": 0.001, "longitude": 0.001, "is_published": False}]
    mock_repo.get_all_restaurants.return_value = mock_data

    results = service.get_nearby_restaurants(customer, radius_km=10.0)
    assert len(results) == 0


def test_get_nearby_restaurants_at_zero_coordinates(service, mock_repo, customer):
    """
    Feat3-FR1:
    Edge Case: Customer and Restaurant are both at (0,0)
    """
    mock_data = [{"id": 1, "name": "Equator Eats", "latitude": 0.0, "longitude": 0.0, "is_published": True}]
    mock_repo.get_all_restaurants.return_value = mock_data

    results = service.get_nearby_restaurants(customer, radius_km=10.0)
    assert len(results) == 1
    assert results[0]["distance_from_user"] == 0.0

def test_get_nearby_restaurants_extreme_radius(service, mock_repo, customer):
    """
    Feat3-FR1:
    Edge Case: Huge radius should include all published restaurants
    """
    mock_data = [
        {"id": 1, "name": "London Pub", "latitude": 51.5, "longitude": -0.1, "is_published": True},
        {"id": 2, "name": "Tokyo Sushi", "latitude": 35.6, "longitude": 139.6, "is_published": True}
    ]
    mock_repo.get_all_restaurants.return_value = mock_data

    # Radius of 20,000km
    results = service.get_nearby_restaurants(customer, radius_km=20000.0)
    assert len(results) == 2

def test_get_nearby_restaurants_zero_radius(service, mock_repo):
    """
    Feat3-FR1:
    Edge Case: Radius of 0.0 should only return
    exact matches
    """
    local_customer = Customer(id=5, username="u", email="e@mail.com", password_hash="p", latitude=10.0, longitude=10.0)
    mock_data = [
        {"id": 1, "name": "Exact", "latitude": 10.0, "longitude": 10.0, "is_published": True},
        {"id": 2, "name": "Near", "latitude": 10.0001, "longitude": 10.0001, "is_published": True}
    ]
    mock_repo.get_all_restaurants.return_value = mock_data
    
    results = service.get_nearby_restaurants(local_customer, radius_km=0.0)
    assert len(results) == 1


def test_calculate_haversine_accuracy(service):
    """
    Feat3-FR1:
    Positive Functional: Test the math helper directly with known distances.
    Distance between Kelowna and Vancouver is ~270km
    """
    dist = service.calculate_haversine(49.88, -119.49, 49.28, -123.12)
    assert 265 <= dist <= 275  # Allow small margin for earth curvature models
