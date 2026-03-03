import pytest

from backend.services.restaurant_service import RestaurantService
from backend.models.user.restaurant_owner_model import RestaurantOwner
from backend.models.user.customer import Customer
from backend.models.user.admin import Admin

class MockRepo:
    def create_restaurant(self, restaurant_data):
        return "mock_id_123"

@pytest.fixture
def restaurant_service():
    return RestaurantService(MockRepo())

# Positive functionality test: A restaurant owner should be able to create a restaurant
def test_create_restaurant_as_owner(restaurant_service):
    user = RestaurantOwner(id=1,username="Grayson",password_hash="hashed_pw")
    data = {"name": "Testaurant", "location": "123 Test St"}

    result = restaurant_service.register_restaurant(user, data)

    assert result["success"] == True
    assert result["restaurant_id"] == "mock_id_123"

# Edge case: A customer should not be able to create a restaurant
def test_create_restaurant_as_customer(restaurant_service):
    user = Customer(id=2,username="Newbie",password_hash="hashed_pw")
    data = {"name": "Testaurant", "location": "123 Test St"}
    
    result = restaurant_service.register_restaurant(user, data)

    assert result["success"] == False
    assert "unauthorized" in result["error"]