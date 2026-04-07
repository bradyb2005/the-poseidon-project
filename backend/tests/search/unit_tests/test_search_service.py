# backend/tests/search/unit_tests/search_service.py
import pytest
from unittest.mock import MagicMock
from backend.services.search_service import SearchService


def test_search_returns_empty_for_short_query(search_service):
    """
    Feat3-FR2
    Boundary value analysis: If a search is only one letter and they
    Try to search, nothing will show up to save resources
    """
    res = search_service.search_by_keyword("")
    assert res["items"] == []
    assert res["total_count"] == 0

def test_search_by_keyword_success(search_service, mock_restaurant_repo, mock_item_repo):
    """
    Functional Logic/ Mocking
    Tests that a valid keyword returns matching items from published restaurants.
    """
    mock_res = MagicMock()
    mock_res.id = 10
    mock_res.is_published = True
    mock_restaurant_repo.load_all.return_value = [mock_res]

    mock_item = MagicMock()
    mock_item.restaurant_id = 10
    mock_item.name = "Beef Pie"
    mock_item.tags = ["savory"]
    mock_item.model_dump.return_value = {"item_name": "Beef Pie", "tags": ["savory"]}
    
    mock_item_repo.load_all.return_value = [mock_item]

    results = search_service.search_by_keyword("beef")

    assert len(results["items"]) == 1
    assert results["items"][0]["item_name"] == "Beef Pie"
    assert results["total_count"] == 1


def test_search_filters_unpublished_restaurants(search_service, mock_restaurant_repo, mock_item_repo):
    """
    Equivalence Partitioning
    Items should NOT appear in search if their restaurant is not published.
    """
    mock_res = MagicMock(id=10, is_published=False)
    mock_restaurant_repo.load_all.return_value = [mock_res]

    mock_item = MagicMock(restaurant_id=10, name="Hidden Pizza", tags=[])
    mock_item_repo.load_all.return_value = [mock_item]

    results = search_service.search_by_keyword("pizza")

    assert len(results["items"]) == 0


def test_search_by_tag_match(search_service, mock_restaurant_repo, mock_item_repo):
    """
    Functional Test
    Tests that searching for a tag (e.g., 'vegan') returns the item.
    """
    mock_res = MagicMock(id=1, is_published=True)
    mock_restaurant_repo.load_all.return_value = [mock_res]

    mock_item = MagicMock()
    mock_item.restaurant_id = 1
    mock_item.name = "Salad"
    mock_item.tags = ["vegan", "healthy"]
    mock_item.model_dump.return_value = {"item_name": "Salad", "tags": ["vegan"]}
    
    mock_item_repo.load_all.return_value = [mock_item]

    results = search_service.search_by_keyword("vegan")

    assert len(results["items"]) == 1
    assert "Salad" in results["items"][0]["item_name"]

# --- Feature 3 - FR 3 ---

def test_get_homepage_featured_limit(search_service, mock_restaurant_repo, mock_item_repo):
    """
    Boundary Value Analysis
    Ensures only the first 5 published items are returned.
    """
    mock_res = MagicMock(id=1, is_published=True)
    mock_restaurant_repo.load_all.return_value = [mock_res]

    items = []
    for i in range(10):
        item = MagicMock(restaurant_id=1)
        item.model_dump.return_value = {"id": i}
        items.append(item)
    
    mock_item_repo.load_all.return_value = items

    featured = search_service.get_homepage_featured()

    assert len(featured["items"]) == 5

def test_browse_homepage_filters_unpublished(search_service, mock_restaurant_repo):
    """
    Equivalence Partitioning
    Homepage list only contains published restaurants.
    """
    mock_res_active = MagicMock(id=1, is_published=True)
    mock_res_hidden = MagicMock(id=2, is_published=False)
    
    mock_res_active.model_dump.return_value = {"id": 1, "name": "Active Diner"}
    mock_restaurant_repo.load_all.return_value = [mock_res_active, mock_res_hidden]

    results = search_service.browse_homepage()

    assert len(results["items"]) == 1
    assert results["items"][0]["name"] == "Active Diner"


def test_get_restaurant_details_success(search_service, mock_restaurant_repo, mock_item_repo):
    """
    Mocking/ Functional Test
    Fetches a restaurant and successfully injects its menu items
    """

    mock_res = MagicMock(id=101, is_published=True)
    mock_res.model_dump.return_value = {"id": 101, "name": "Test Cafe"}
    mock_restaurant_repo.load_all.return_value = [mock_res]

    mock_item = MagicMock(restaurant_id=101)
    mock_item.model_dump.return_value = {"item_name": "Coffee"}
    mock_item_repo.load_all.return_value = [mock_item]

    result = search_service.get_restaurant_details(101)

    assert result is not None
    assert result["name"] == "Test Cafe"
    assert len(result["full_menu_details"]) == 1
    assert result["full_menu_details"][0]["item_name"] == "Coffee"


def test_get_restaurant_details_not_found_or_hidden(search_service, mock_restaurant_repo):
    """
    Exception Handling/ Fault injection
    Returns None for non-existent or unpublished IDs.
    """
    mock_res = MagicMock(id=50, is_published=False)
    mock_restaurant_repo.load_all.return_value = [mock_res]

    assert search_service.get_restaurant_details(50) is None

    assert search_service.get_restaurant_details(999) is None

# ---Pagination tests ---

def test_search_pagination_limit_per_page(search_service, mock_restaurant_repo, mock_item_repo):
    """
    Boundary Value Analysis
    Verify that a maximum of 20 results are returned per page
    """
    mock_res = MagicMock(id=1, is_published=True)
    mock_restaurant_repo.load_all.return_value = [mock_res]

    items = []
    for i in range(25):
        item = MagicMock()
        item.restaurant_id = 1
        item.name = "Pizza"
        item.tags = []
        item.model_dump.return_value = {"id": i, "name": "Pizza", "tags": []}
        items.append(item)
    
    mock_item_repo.load_all.return_value = items

    results = search_service.search_by_keyword("pizza", page=1, limit=20)

    assert len(results["items"]) == 20
    assert results["total_count"] == 25


def test_pagination_navigator_metadata(search_service, mock_restaurant_repo):
    """
    Functional Test
    Ensures 'total_pages' is calculated correctly for the page navigator
    """

    restaurants = [MagicMock(id=i, is_published=True) for i in range(45)]
    for r in restaurants: r.model_dump.return_value = {"id": r.id}
    mock_restaurant_repo.load_all.return_value = restaurants

    results = search_service.browse_homepage(page=1, limit=20)

    assert results["total_pages"] == 3
    assert results["total_count"] == 45
    assert results["has_next"] is True
# --- Location-Based Search Tests ---

def test_get_nearby_restaurants_sorting(search_service, mock_restaurant_repo):
    """
    Functional Test
    Ensures restaurants are sorted by distance (closest first)
    """
    mock_res_a = MagicMock(id=1, latitude=0.1, longitude=0.1, is_published=True)
    mock_res_b = MagicMock(id=2, latitude=1.0, longitude=1.0, is_published=True)
    
    mock_res_a.model_dump.return_value = {"id": 1, "name": "Close Place"}
    mock_res_b.model_dump.return_value = {"id": 2, "name": "Far Place"}
    
    # wrong order to ensure sorting is tested
    mock_restaurant_repo.load_all.return_value = [mock_res_b, mock_res_a]

    results = search_service.get_nearby_restaurants(user_lat=0.0, user_lon=0.0)

    assert len(results["items"]) == 2
    assert results["items"][0]["name"] == "Close Place"
    assert results["items"][0]["distance_km"] < results["items"][1]["distance_km"]


def test_get_nearby_restaurants_filters_unpublished(search_service, mock_restaurant_repo):
    """
    Equivalence Partitioning
    Unpublished restaurants should not appear in nearby results.
    """
    mock_res_pub = MagicMock(id=1, latitude=0.1, longitude=0.1, is_published=True)
    mock_res_hid = MagicMock(id=2, latitude=0.1, longitude=0.1, is_published=False)
    
    mock_res_pub.model_dump.return_value = {"id": 1}
    mock_restaurant_repo.load_all.return_value = [mock_res_pub, mock_res_hid]

    results = search_service.get_nearby_restaurants(user_lat=0.0, user_lon=0.0)

    assert len(results["items"]) == 1
    assert results["items"][0]["id"] == 1


def test_get_nearby_restaurants_limit(search_service, mock_restaurant_repo):
    """
    Boundary Value Analysis
    Ensures the 'limit' parameter restricts the number of results.
    """
    restaurants = []
    for i in range(10):
        res = MagicMock(id=i, latitude=0.1, longitude=0.1, is_published=True)
        res.model_dump.return_value = {"id": i}
        restaurants.append(res)
        
    mock_restaurant_repo.load_all.return_value = restaurants

    results = search_service.get_nearby_restaurants(user_lat=0.0, user_lon=0.0, limit=3)

    assert len(results["items"]) == 3
