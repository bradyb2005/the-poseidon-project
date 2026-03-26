import sys
from pathlib import Path
from decimal import Decimal
from uuid import uuid4
from unittest.mock import MagicMock

import pytest

from backend.models.user.user_schema import User
from backend.models.restaurant.menu_item_model import MenuItem
from backend.schemas.items_schema import MenuItem as MenuItemSchema
from backend.schemas.restaurant_schema import Restaurant as RestaurantSchema


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
def sample_item():
    """Return a valid menu item."""
    return MenuItem(
        id=101,
        name="Burger",
        price=9.99,
        tags=["Popular"],
    )

@pytest.fixture
def raw_menu_item_data():
    return {
        "item_name": "Beef Pie",
        "restaurant_id": 10,
        "price": "12.50",
        "id": str(uuid4())
    }

@pytest.fixture
def restaurant(owner, sample_item):
    """Return a default restaurant linked to an owner."""
    return Restaurant(
        id=1,
        name="John's Diner",
        owner=owner,
        menu=[sample_item],
    )

