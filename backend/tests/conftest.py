# backend/tests/conftest.py
import pytest
import sys
from pathlib import Path
from decimal import Decimal
from uuid import uuid4
from unittest.mock import MagicMock
from backend.schemas.restaurant_schema import Restaurant
from backend.schemas.items_schema import MenuItem as MenuItemSchema



# add project root to import path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

@pytest.fixture
def client():
    from backend.main import app
    from fastapi.testclient import TestClient
    return TestClient(app)

@pytest.fixture
def mock_restaurant_service(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("backend.routes.restaurant_router.service", mock)
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

@pytest.fixture
def mock_search_service(monkeypatch):
    mock = MagicMock()
    # This will be used when we create the search_router
    monkeypatch.setattr("backend.routes.search_router.service", mock)
    return mock


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
    return MenuItemSchema(**raw_menu_item_data)

