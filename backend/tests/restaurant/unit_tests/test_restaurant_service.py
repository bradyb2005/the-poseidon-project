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
