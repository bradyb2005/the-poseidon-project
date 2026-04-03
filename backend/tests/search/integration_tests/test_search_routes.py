# backend/tests/search/integration_tests/test_search_routes.py
import pytest

# --- GET Search Tests ---

def test_get_search_success(client, mock_search_service, raw_menu_item_data):
    """
    Equivalence Partitioning
    Verifies that a valid keyword returns a list of items and 200 OK.
    """
    mock_search_service.search_by_keyword.return_value = {
        "items": [raw_menu_item_data],
        "total_count": 1,
        "page": 1,
        "per_page": 20,
        "has_next": False,
        "total_pages": 1
    }

    response = client.get("/search?q=pie")
    assert response.status_code == 200

    data = response.json()
    assert data["total_count"] == 1
    assert data["items"][0]["item_name"] == "Beef Pie"


def test_get_search_empty_query(client, mock_search_service):
    """
    Boundary Value Analysis
    Ensures that calling search without a query parameter returns an empty list.
    """
    mock_search_service.search_by_keyword.return_value = {
        "items": [],
        "total_count": 0,
        "page": 1,
        "per_page": 20,
        "has_next": False,
        "total_pages": 1
    }
    response = client.get("/search?q=unknown_item")

    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total_count"] == 0

    mock_search_service.search_by_keyword.assert_called_once()


# --- Homepage & Featured Tests ---

def test_get_homepage_list(client, mock_search_service, restaurant):
    """
    Functional Test
    Ensures the homepage returns the list of published restaurants (Feat3-FR3).
    """
    restaurant_dict = restaurant.model_dump(by_alias=True)
    
    mock_search_service.browse_homepage.return_value = {
        "items": [restaurant_dict],
        "total_count": 1,
        "page": 1,
        "per_page": 20,
        "has_next": False,
        "total_pages": 1
    }

    response = client.get("/search/homepage")

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["items"][0]["name"] == "John's Diner"


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

def test_get_restaurant_details_success(client, mock_search_service, restaurant, raw_menu_item_data):
    """
    Equivalence Partitioning
    Verifies retrieval of a specific restaurant with its full menu injected.
    """
    detail_data = restaurant.model_dump(by_alias=True)
    detail_data["full_menu_details"] = [raw_menu_item_data]

    mock_search_service.get_restaurant_details.return_value = detail_data

    response = client.get(f"/search/details/{restaurant.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John's Diner"
    assert "full_menu_details" in data
    assert data["full_menu_details"][0]["item_name"] == "Beef Pie"


def test_get_restaurant_details_not_found(client, mock_search_service):
    """
    Exception Handling
    Ensures a 404 is raised if the restaurant is missing or unpublished.
    """

    mock_search_service.get_restaurant_details.return_value = None

    response = client.get("/search/details/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Restaurant not found or is not published"