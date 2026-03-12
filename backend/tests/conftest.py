# backend/tests/conftest.py
import pytest
from unittest.mock import MagicMock
from backend.models.user.restaurant_owner_model import RestaurantOwner
from backend.models.restaurant.restaurant_model import Restaurant
from backend.models.restaurant.menu_item_model import MenuItem

@pytest.fixture
def owner():
    """
    Return real RestaurantOwner
    """
    return RestaurantOwner(
        id=1,
        username="John_Doe",
        email="john_doe@gmail.com",
        password_hash="SecurePass123"
    )

@pytest.fixture
def mock_owner():
    """
    Return mock for tests where owner login is not important
    """
    mock = MagicMock(spec=RestaurantOwner)
    mock.id = 99
    mock.username = "MockUser"
    return mock

@pytest.fixture
def sample_item():
    """
    return valid menu item for FR3
    """
    return MenuItem(name="Burger", price=9.99)

@pytest.fixture
def restaurant(owner, sample_item):
    """
    Return default instance linked to owner
    """
    return Restaurant(
        name="John's Diner",
        owner=owner,
        menu=[sample_item]
    )
