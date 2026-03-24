# backend/tests/conftest.py
import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock
from backend.schemas.restaurant_schema import Restaurant
from backend.models.user.restaurant_owner_model import RestaurantOwner
from backend.models.restaurant.menu_item_model import MenuItem


# add project root to import path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

@pytest.fixture
def restaurant():
        return Restaurant(
            id=1,
            name="John's Diner",
            menu=["Burger", "Fries"],
            owner_id="1",
            open_time=900,
            close_time=2200,
            phone="555-555-5555",
            address="123 Main St",
            latitude=34.34,
            longitude=-118.34,
            is_published=False,
    )

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    from backend.services.restaurant_service import RestaurantService
    return RestaurantService(mock_repo)

# old fixtures

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
def sample_item():
    """
    return valid menu item for FR3
    """
    return MenuItem(
        id=101,
        name="Burger",
        price=9.99,
        tags=["Popular"])



