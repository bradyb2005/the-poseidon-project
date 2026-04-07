import sys
from backend.schemas.review_schema import ReviewDisplay
import pytest
from pathlib import Path
from decimal import Decimal
from uuid import uuid4
from datetime import datetime
from backend.main import app
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from backend.models.user.user_schema import User
from backend.schemas.restaurant_schema import Restaurant
from backend.schemas.items_schema import MenuItem as MenuItemSchema
from backend.services.search_service import SearchService

# Root path setup
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

# --- Repo mocks ---

@pytest.fixture
def mock_restaurant_repo():
    return MagicMock()

@pytest.fixture
def mock_item_repo():
    return MagicMock()

@pytest.fixture
def mock_review_repo():
    return MagicMock()

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def mock_order_repo():
    return MagicMock()

# --- Service fixtures ---

@pytest.fixture
def service(mock_repo):
    from backend.services.restaurant_service import RestaurantService
    return RestaurantService(mock_repo)

@pytest.fixture
def restaurant_service(mock_restaurant_repo):
    from backend.services.restaurant_service import RestaurantService
    return RestaurantService(mock_restaurant_repo)

# For unit tests
@pytest.fixture
def search_service(mock_restaurant_repo, mock_item_repo):
    return SearchService(
        restaurant_repo = mock_restaurant_repo,
        item_repo = mock_item_repo)

# For integration tests
@pytest.fixture
def mock_search_service(monkeypatch):
    mock = MagicMock()
    import backend.routes.search_routes as search_module
    monkeypatch.setattr(search_module, "service", mock)
    return mock

@pytest.fixture
def review_service(mock_review_repo, mock_order_repo, mock_restaurant_repo):
    from backend.services.review_service import ReviewService
    return ReviewService(
        review_repo=mock_review_repo, 
        order_repo=mock_order_repo, 
        restaurant_repo=mock_restaurant_repo
    )

# --- Monkeypatch fixtures ---

"""
This fixture will be used for routers

@pytest.fixture
def mock_review_service_logic(monkeypatch):
    """"""Monkeypatches the review service in the router for integration tests.""""""
    mock = MagicMock()
    # Replace 'backend.routes.review_routes' with your actual router path
    import backend.routes.review_routes as review_module 
    monkeypatch.setattr(review_module, "service", mock)
    return mock
"""


# --- Data fixtures ---

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
            is_published=False
    )

@pytest.fixture
def sample_review():
    """Provides a valid ReviewDisplay object."""
    return ReviewDisplay(
        id=str(uuid4()),
        order_id="ord-123",
        customer_id="user-456",
        restaurant_id=1,
        rating=5,
        comment="Delicious!",
        created_at=datetime.now()
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
def sample_menu_item(raw_menu_item_data):
    return MenuItemSchema(**raw_menu_item_data)
