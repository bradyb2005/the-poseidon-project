# backend/tests/restaurant/unit_tests/test_restaurant_service.py
import pytest
from backend.services.restaurant_service import RestaurantService
from backend.models.user.customer import Customer
from backend.models.user.restaurant_owner_model import RestaurantOwner
from backend.models.restaurant.restaurant_model import Restaurant

class MockRepo:
    def __init__(self):
        self.restaurants = {}
    
    def create_restaurant(self, restaurant_data):
        return "mock_id_123"
    
    def get_by_id(self, restaurant_id):
        return self.restaurants.get(restaurant_id)
    
    def update(self, restaurant):
        self.restaurants[restaurant.id] = restaurant
        return True
    
    def get_all_restaurants(self):
        # Expects a list of dictionaries
        return [res.to_dict() if hasattr(res, 'to_dict'
                                         ) else res for res in self.restaurants.values()]

@pytest.fixture
def restaurant_service():
    return RestaurantService(MockRepo())

# --- F2FR3: Publishing logic ---

def test_publish_restaurant_success(restaurant_service, restaurant):
    # Positive Functional test: Publish when all required fields are filled
    # Complete partial conftest
    restaurant.address = "123 Test Ave"
    restaurant.phone = "555-555-5555"
    restaurant.open_time = 900
    restaurant.close_time = 2200
    restaurant.menu = ["Mock item"]

    restaurant_service.restaurant_repository.restaurants[restaurant.id] = restaurant

    result = restaurant_service.publish_restaurant(restaurant.id)

    assert result["success"] is True
    assert restaurant.is_published is True

def test_publish_restaurant_fails_missing_info(restaurant_service, restaurant):
    # Edge test: Throw error if incomplete
    restaurant_service.restaurant_repository.restaurants[restaurant.id] = restaurant
    result = restaurant_service.publish_restaurant(restaurant.id)

    assert result["success"] is False
    assert "is required" in result["error"]
    assert restaurant.is_published is False

def test_admin_customer_perspective(restaurant_service, restaurant):
    # Positive Functional Test: Tests that different perspectives can be used
    # Customer perspective should not see unpublished restaurant
    restaurant.address = "123 Test Ave"
    restaurant.phone = "555-555-5555"
    restaurant.open_time = 900
    restaurant.close_time = 2200
    restaurant_service.restaurant_repository.restaurants[restaurant.id] = restaurant

    # Ensure customer cant see restaurant before it is published
    assert restaurant.get_view("Customer") is None

    # Publish
    restaurant_service.publish_restaurant(restaurant.id)

    # Check to see if customer can view it
    view = restaurant.get_view("Customer")
    assert view is not None
    assert view["name"] == "John's Diner"

# --- F2FR1: Registration and roles---

def test_create_restaurant_as_owner(restaurant_service, owner):
    # Positive functionality test: Owner can create a restaurant
    data = {"name": "New Spot", "location": "789 Road"}
    result = restaurant_service.register_restaurant(owner, data)

    assert result["success"] is True
    assert result["restaurant_id"] == "mock_id_123"

def test_create_restaurant_as_customer(restaurant_service):
    # Edge case: A customer should not be able to create a restaurant
    customer = Customer(
        id=2,
        username="Newbie",
        email="newbie@example.com",
        password_hash="hashed_pw"
    )
    data = {"name": "Fake place", "location": "None"}

    result = restaurant_service.register_restaurant(customer, data)

    assert result["success"] == False
    assert "unauthorized" in result["error"]

def test_service_publish_flow_success(restaurant_service, restaurant):
    # Positive Functional Test: Tests that user can store before publishing
    restaurant.address = "123 Test Ave"
    restaurant.phone = "555-555-5555"
    restaurant.open_time = 900
    restaurant.close_time = 2200
    restaurant_service.restaurant_repository.restaurants[restaurant.id] = restaurant

    result = restaurant_service.publish_restaurant(restaurant.id)

    assert result["success"] is True
    assert restaurant.is_published is True

def test_publish_fails_without_menu(restaurant_service, restaurant):
    # Negative Edge Case: Cannot publish without menu
    restaurant.address = "123 Test Ave"
    restaurant.phone = "555-555-5555"
    # Clear menu
    restaurant.menu = []
    restaurant_service.restaurant_repository.restaurants[restaurant.id] = restaurant

    result = restaurant_service.publish_restaurant(restaurant.id)

    assert result["success"] is False
    assert "menu cannot be empty" in result["error"]

# --- F3FR1 Nearby search logic ---

def test_get_nearby_restaurants_filtering_and_sorting(restaurant_service):
    """
    Feat3-FR1:
    Functional test: Test that restaurants are filtered
    by radius and sorted by distance
    """
    customer = Customer(id=1, username="c", email="c@test.com", password_hash="h", 
                        latitude=0.0, longitude=0.0)

    # Setup Mock Data
    # Restaurant A: Very close
    res_a = {"id": 1, "name": "Close Cafe", "latitude": 0.01, "longitude": 0.01, "is_published": True}
    # Restaurant B: Within radius but further
    res_b = {"id": 2, "name": "Far Food", "latitude": 0.1, "longitude": 0.1, "is_published": True}
    # Restaurant C: Outside 20km radius
    res_c = {"id": 3, "name": "Out of Bounds", "latitude": 1.0, "longitude": 1.0, "is_published": True}

    restaurant_service.restaurant_repository.restaurants = {1: res_a, 2: res_b, 3: res_c}

    # Execution (Radius 20km)
    results = restaurant_service.get_nearby_restaurants(customer, radius_km=20.0)

    assert len(results) == 2  # Only A and B
    assert results[0]["name"] == "Close Cafe"  # Sorting check (closest first)
    assert results[1]["name"] == "Far Food"
    assert "distance_from_user" in results[0]

def test_get_nearby_restaurants_ignores_unpublished(restaurant_service):
    """
    Feat3-FR1:
    Negative functional test: Test that even if a
    restaurant is close, it's hidden if not published
    """
    customer = Customer(id=1, username="c", email="c@test.com", password_hash="h", 
                        latitude=0.0, longitude=0.0)

    # Close but unpublished
    res_hidden = {"id": 1, "name": "Ghost Kitchen", "latitude": 0.001, "longitude": 0.001, "is_published": False}

    restaurant_service.restaurant_repository.restaurants = {1: res_hidden}

    results = restaurant_service.get_nearby_restaurants(customer, radius_km=10.0)

    assert len(results) == 0

def test_calculate_haversine_accuracy(restaurant_service):
    """
    Feat3-FR1:
    Positive Functional: Test the math helper directly with known distances.
    Distance between Kelowna and Vancouver is ~270km
    """
    dist = restaurant_service.calculate_haversine(49.88, -119.49, 49.28, -123.12)
    assert 265 <= dist <= 275  # Allow small margin for earth curvature models

def test_get_nearby_restaurants_at_zero_coordinates(restaurant_service):
    """
    Feat3-FR1:
    Edge Case: Customer and Restaurant are both at (0,0)
    """
    customer = Customer(id=1, username="c", email="c@test.com", password_hash="h", 
                        latitude=0.0, longitude=0.0)

    res = {"id": 1, "name": "Equator Eats", "latitude": 0.0, "longitude": 0.0, "is_published": True}
    restaurant_service.restaurant_repository.restaurants = {1: res}

    results = restaurant_service.get_nearby_restaurants(customer, radius_km=10.0)

    assert len(results) == 1
    assert results[0]["distance_from_user"] == 0.0

def test_get_nearby_restaurants_extreme_radius(restaurant_service):
    """
    Feat3-FR1:
    Edge Case: Huge radius should include all published restaurants
    """
    customer = Customer(id=1, username="c", email="c@test.com", password_hash="h", 
                        latitude=0.0, longitude=0.0)

    # One in London, one in Tokyo
    res1 = {"id": 1, "name": "London Pub", "latitude": 51.5, "longitude": -0.1, "is_published": True}
    res2 = {"id": 2, "name": "Tokyo Sushi", "latitude": 35.6, "longitude": 139.6, "is_published": True}

    restaurant_service.restaurant_repository.restaurants = {1: res1, 2: res2}

    # Radius of 20,000km
    results = restaurant_service.get_nearby_restaurants(customer, radius_km=20000.0)

    assert len(results) == 2

def test_get_nearby_restaurants_zero_radius(restaurant_service):
    """
    Feat3-FR1:
    Edge Case: Radius of 0.0 should only return
    exact matches
    """
    customer = Customer(id=1, username="c", email="c@test.com", password_hash="h", 
                        latitude=10.0, longitude=10.0)

    res_exact = {"id": 1, "name": "Same Spot", "latitude": 10.0, "longitude": 10.0, "is_published": True}
    res_near = {"id": 2, "name": "Near Spot", "latitude": 10.0001, "longitude": 10.0001, "is_published": True}

    restaurant_service.restaurant_repository.restaurants = {1: res_exact, 2: res_near}

    results = restaurant_service.get_nearby_restaurants(customer, radius_km=0.0)

    assert len(results) == 1
    assert results[0]["id"] == 1
