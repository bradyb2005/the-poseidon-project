# backend/tests/search/integration_tests/test_search_routes.py
import pytest

# --- GET Search Tests ---

def test_get_search_success(client, mock_search_service):
    """
    Equivalence Partitioning
    Verifies that a valid keyword returns a list of items and 200 OK.
    """
    mock_items = [{"name": "Burger", "restaurant_id": "1", "price": 10.99}]
    mock_search_service.search_by_keyword.return_value = mock_items

    response = client.get("/search?q=burger")

    assert response.status_code == 200
    assert response.json() == mock_items
    mock_search_service.search_by_keyword.assert_called_with("burger")


def test_get_search_empty_query(client, mock_search_service):
    """
    Boundary Value Analysis
    Ensures that calling search without a query parameter returns an empty list.
    """
    response = client.get("/search")

    assert response.status_code == 200
    assert response.json() == []

    mock_search_service.search_by_keyword.assert_not_called()


# --- Homepage & Featured Tests ---

def test_get_homepage_list(client, mock_search_service):
    """
    Functional Test
    Ensures the homepage returns the list of published restaurants (Feat3-FR3).
    """
    mock_restaurants = [{"id": "1", "name": "John's Diner", "is_published": True}]
    mock_search_service.browse_homepage.return_value = mock_restaurants

    response = client.get("/search/homepage")

    assert response.status_code == 200
    assert response.json() == mock_restaurants


def test_get_featured_items(client, mock_search_service):
    """
    Functional Test
    Ensures the featured endpoint returns the expected menu items (Feat3-FR3).
    """
    mock_featured = [{"name": "Special Pizza", "price": 15.00}]
    mock_search_service.get_homepage_featured.return_value = mock_featured

    response = client.get("/search/featured")

    assert response.status_code == 200
    assert len(response.json()) == 1


# --- Detail View Tests ---

def test_get_restaurant_details_success(client, mock_search_service):
    """
    Equivalence Partitioning
    Verifies retrieval of a specific restaurant with its full menu injected.
    """
    mock_details = {
        "id": "1",
        "name": "John's Diner",
        "full_menu_details": [{"name": "Burger", "price": 10.99}]
    }
    mock_search_service.get_restaurant_details.return_value = mock_details

    response = client.get("/search/details/1")

    assert response.status_code == 200
    assert "full_menu_details" in response.json()
    assert response.json()["name"] == "John's Diner"


def test_get_restaurant_details_not_found(client, mock_search_service):
    """
    Exception Handling
    Ensures a 404 is raised if the restaurant is missing or unpublished.
    """

    mock_search_service.get_restaurant_details.return_value = None

    response = client.get("/search/details/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Restaurant not found or is not published"