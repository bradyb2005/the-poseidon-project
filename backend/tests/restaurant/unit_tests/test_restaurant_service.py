# backend/tests/restaurant/unit_tests/test_menu_item_model.py
import pytest
from unittest.mock import MagicMock, ANY
from backend.models.user.customer import Customer
from backend.services.restaurant_service import RestaurantService
from backend.models.user.customer import Customer
from backend.models.user.restaurant_owner_model import RestaurantOwner

@pytest.fixture
def mock_restaurant_repository():
    return MagicMock()

@pytest.fixture
def service(mock_restaurant_repository):
    return RestaurantService(mock_restaurant_repository)

@pytest.fixture
def restaurant_owner():
    return RestaurantOwner(
        id=1, 
        username="John Doe", 
        password_hash="hashed_password", 
        email="fakeemail@mail.ca",
    )
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

@pytest.fixture
def customer():
    return Customer(id=2, username="Newbie", password_hash="hashed_pw", email="customer@mail.com")

# --- FR2: Menu tagging tests ---

# Positive Functional Test
def test_add_tagged_item_success(service, mock_restaurant_repository, restaurant_owner):
    # Verify owner can add item with tags
    restaurant_id = "rest1"

    item_data = {
        "name": "Vegan Burger",
        "price": 9.99,
        "tags": ["Vegan", "Burger"]
    }

    mock_restaurant_repository.add_menu_item.return_value = True
    result = service.add_tagged_item(restaurant_owner, restaurant_id, item_data)

    assert result["success"] == True
    assert "menu_item" in result

    # Verify repository method was called with correct parameters
    mock_restaurant_repository.add_menu_item.assert_called_once_with(restaurant_id, ANY)

    args, _ = mock_restaurant_repository.add_menu_item.call_args
    passed_item = args[1]
    assert passed_item.name == "Vegan Burger"
    assert passed_item.tags == ["Vegan", "Burger"]

def test_add_tagged_item_invalid_tags(service, mock_restaurant_repository, restaurant_owner):
    restaurant_id = 123
    # Sending integers instead of strings
    item_data = {
        "name": "Bad Tags Burger",
        "price": 9.99,
        "tags": [1, 2, 3] 
    }

    result = service.add_tagged_item(restaurant_owner, restaurant_id, item_data)

    assert result["success"] is False
    assert "tags must be a list of strings" in result["error"]
    # Ensure the repo was NEVER called
    mock_restaurant_repository.add_menu_item.assert_not_called()

# --- Creating restaurant tests ---

# --- FR3: Publishing logic ---

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

# --- FR1: Registration and roles

def test_create_restaurant_as_owner(restaurant_service, owner):
    # Positive functionality test: Owner can create a restaurant
    data = {"name": "New Spot", "location": "789 Road"}
    result = restaurant_service.register_restaurant(owner, data)
# Positive functionality test: A restaurant owner should be able to create a restaurant
def test_create_restaurant_as_owner(service, mock_restaurant_repository, restaurant_owner):
    data = {
        "name": "Testaurant", 
        "open_time": "10:00", 
        "close_time": "22:00"
    }

    mock_restaurant_repository.create_restaurant.return_value = "mock_id_123"

    result = service.register_restaurant(restaurant_owner, data)

    assert result["success"] is True
    assert result["restaurant_id"] == "mock_id_123"
    mock_restaurant_repository.create_restaurant.assert_called_once_with(ANY)

    args, _ = mock_restaurant_repository.create_restaurant.call_args
    created_restaurant = args[0]
    assert created_restaurant.name == "Testaurant"

# Edge case: A customer should not be able to create a restaurant
def test_create_restaurant_as_customer(service, customer):
    data = {"name": "Testaurant"}
    
    result = service.register_restaurant(customer, data)
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
    assert result["error"] == "unauthorized"

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
