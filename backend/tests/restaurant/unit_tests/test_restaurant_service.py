# backend/tests/restaurant/unit_tests/test_menu_item_model.py
import pytest
from unittest.mock import MagicMock
from backend.services.restaurant_service import RestaurantService
from backend.models.user.restaurant_owner_model import RestaurantOwner

@pytest.fixture
def mock_restaurant_repository():
    return MagicMock()

@pytest.fixture
def service(mock_restaurant_repository):
    return RestaurantService(mock_restaurant_repository)

@pytest.fixture
def restaurant_owner():
    return RestaurantOwner(id=1, username="John Doe", password_hash="hashed_password", email="fakeemail@mail.ca")

# --- FR2: Menu tagging tests ---

# Positive Functional Test
def test_add_tagged_item_success(service, mock_restaurant_repository, restaurant_owner):
    # Verify owner can add item with tags
    restauarant_id = "rest1"
    item_data = {
        "name": "Vegan Burger",
        "price": 9.99,
        "tags": ["Vegan", "Burger"]
    }

    mock_restaurant_repository.add_menu_item.return_value = True
    result = service.add_tagged_item(restaurant_owner, restauarant_id, item_data)

    assert result["success"] == True
    assert "menu_item" in result

    # Verify repository method was called with correct parameters
    mock_restaurant_repository.add_menu_item.assert_called_once()
    args, _ = mock_restaurant_repository.add_menu_item.call_args
    assert args[0] == restauarant_id
    assert args[1].tags == ["Vegan", "Burger"]
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
    user = RestaurantOwner(id=1,name="Grayson",password_hash="hashed_pw")
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
