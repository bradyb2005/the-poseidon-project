import pytest

from restaurant.services.restaurant_service import RestaurantService
from backend.models.user.restaurant_owner_model import RestaurantOwner
from backend.models.user.customer_model import Customer
from backend.models.user.admin_model import Admin

class MockRepo:
    def create_restaurant(self, restaurant_data):
        return "mock_id_123"

@pytest.fixture
def restaurant_service():
    return RestaurantService(MockRepo())

# Positive functionality test: A restaurant owner should be able to create a restaurant
def test_create_restaurant_as_owner(restaurant_service):
    user = RestaurantOwner(name="Grayson")
    data = {"name": "Testaurant", "location": "123 Test St"}

    result = restaurant_service.register_restaurant(user, data)

    assert result["success"] == True
    assert result["restaurant_id"] == "mock_id_123"

# Edge case: A customer should not be able to create a restaurant
def test_create_restaurant_as_customer(restaurant_service):
    user = Customer(name="Newbie")
    data = {"name": "Testaurant", "location": "123 Test St"}
    
    result = restaurant_service.create_restaurant(user, data)

    assert result["success"] == False
    assert "unauthorized" in result["error"]