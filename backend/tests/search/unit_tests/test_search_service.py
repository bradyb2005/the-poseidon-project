# backend/tests/search/unit_tests/search_service.py
import pytest
from unittest.mock import MagicMock
from backend.services.search_service import SearchService


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def service(mock_repo):
    return SearchService(mock_repo)

# --- Functional Tests ---


def test_search_applies_cuisine_filter(service, mock_repo):
    # Feat3-FR2:
    # Functional tests applies cuisine filters
    mock_repo.search_restaurants_and_menu_items.return_value = [
        {"name": "Pizza Hut", "cuisine": "Italian"},
        {"name": "Dominoes", "cuisine": "American"}
    ]

    results = service.search("Pizza", cuisine="Italian")

    assert len(results) == 1
    assert results[0]["name"] == "Pizza Hut"


def test_search_applies_rating_filter(service, mock_repo):
    # Feat3-FR2
    # Functional test applies rating filters
    mock_repo.search_restaurants_and_menu_items.return_value = [
        {"name": "Starbucks", "rating": 4.5},
        {"name": "Dunkin", "rating": 3.0}
    ]

    results = service.search("Coffee", min_rating=4.0)

    assert len(results) == 1
    assert results[0]["name"] == "Starbucks"

# --- Edge Case Tests ---


def test_search_returns_empty_for_short_query(service, mock_repo):
    # Feat3-FR2
    # Edge case test: If a search is only one letter and they
    # Try to search, nothing will show up to save resources
    results = service.search("a")

    assert results == []

    mock_repo.search_restaurants_and_menu_items.assert_not_called()


def test_search_handles_missing_rating_key(service, mock_repo):
    # Feat3-FR2
    # Edge case test: If a restaurnat doesn't have a rating,
    # it defaults to 0 so that it does not crash
    mock_repo.search_restaurants_and_menu_items.return_value = [
        {"name": "New Place"}
    ]

    results = service.search("New", min_rating=1.0)

    assert len(results) == 0
