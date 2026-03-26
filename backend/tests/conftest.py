import sys
import pytest
from pathlib import Path
from decimal import Decimal
from uuid import uuid4
from unittest.mock import MagicMock
from backend.models.user.user_schema import User
from backend.schemas.items_schema import MenuItem
from backend.schemas.restaurant_schema import Restaurant


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


@pytest.fixture
def owner():
    """Return a user representing a restaurant owner."""
    return User(
        id="1",
        username="John_Doe",
        email="john_doe@gmail.com",
        password_hash="SecurePass123",
        owned_restaurants_id=["1"],
    )


@pytest.fixture
def mock_owner():
    """Return a mock user for owner-related tests."""
    mock = MagicMock(spec=User)
    mock.id = "99"
    mock.username = "MockUser"
    mock.owned_restaurants_id = ["1"]
    return mock

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
def raw_menu_item_data():
    return {
        "item_name": "Beef Pie",
        "restaurant_id": 10,
        "price": "12.50",
        "id": str(uuid4())
    }

@pytest.fixture
def sample_menu_item(raw_menu_item_data):
    return MenuItem(**raw_menu_item_data)

