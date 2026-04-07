# backend/tests/restaurant/unit_tests/test_restaurant_service.py
import pytest
from unittest.mock import MagicMock
from backend.services.restaurant_service import RestaurantService
from backend.schemas.restaurant_schema import Restaurant

@pytest.fixture
def base_json_data():
    """Provides the minimum required data for a restaurant."""
    return {
        "id": 1,
        "name": "Restaurant 1",
        "menu": ["Beef Pie", "Burger"]
    }

# --- Get restaurant tests ---

def test_get_restaurant_by_id_success(service, mock_repo, restaurant):
    """
    Equivalience partitioning
    Test getting a restaurant with a valid id
    """
    mock_repo.load_all.return_value = [restaurant]

    result, status = service.get_restaurant_by_id(restaurant.id)

    assert status == 200
    assert result.id == restaurant.id
    assert result.name == "John's Diner"

def test_get_restaurant_by_id_not_found(service, mock_repo):
    """
    Equivalience partitioning
    Test getting a restaurant without a valid id
    """
    mock_repo.load_all.return_value = []

    result, status = service.get_restaurant_by_id(999)

    assert status == 404
    assert result is None

def test_get_all_published_success(service, mock_repo):
    """
    Equivalence Partitioning/ Mocking
    Ensures only published restaurants with nonsensitive data is returned
    """
    res_published = Restaurant(
        id=1, 
        name="Published Diner",
        menu=["Burgers"],
        is_published=True, 
        owner_id="owner_1"
    )
    res_draft = Restaurant(
        id=2, 
        name="Draft Cafe",
        menu=["Tea"], 
        is_published=False, 
        owner_id="owner_2"
    )
    
    mock_repo.load_all.return_value = [res_published, res_draft]

    results = service.get_all_published()

    assert len(results) == 1
    assert results[0]["name"] == "Published Diner"

    assert "owner_id" not in results[0]
    assert "name" in results[0]


def test_get_all_published_empty(service, mock_repo):
    """
    Boundary Value Analysis
    Ensures that if no restaurants are published, an empty list is returned
    """
    res_draft = Restaurant(
        id=1,
        name="Testaurant",
        menu=["Burger"],
        owner_id="owner_3",
        is_published=False)
    mock_repo.load_all.return_value = [res_draft]

    results = service.get_all_published()

    assert isinstance(results, list)
    assert len(results) == 0


# --- Assign owner to restaurant ---

def test_assign_owner_success(service, mock_repo, restaurant):
    """
    Equivalence Partitioning
    Ensures a owner can be assigned to a restaurant
    """

    mock_repo.load_all.return_value = [restaurant]
    new_owner_id = 505

    response, status = service.assign_owner_to_restaurant(restaurant.id, new_owner_id)

    assert status == 200
    assert response["message"] == "Owner assigned"
    assert response["restaurant_id"] == restaurant.id

    mock_repo.save_all.assert_called_once()

    assert restaurant.owner_id == str(new_owner_id)


def test_assign_owner_not_found(service, mock_repo):
    """
    Exception handling
    Ensure the proper error returns when we try to assign a restaurant
    to a nonexistent owner
    """
    mock_repo.load_all.return_value = []
    
    response, status = service.assign_owner_to_restaurant(1, 101)
    
    assert status == 404
    assert response["error"] == "Restaurant not found"

def test_assign_owner_value_error_handling(service, mock_repo, restaurant):
    """
    Fault injection
    Ensure the proper error is thrown during owner assignment
    """
    rest_id = restaurant.id
    mock_repo.load_all.return_value = [restaurant]

    mock_repo.save_all.side_effect = ValueError("Database constraint violated")
    response, status = service.assign_owner_to_restaurant(rest_id, 101)

    assert status == 400
    assert "Database constraint violated" in response["error"]

# --- Publishing ---

def test_publish_restaurant_success(service, mock_repo, restaurant):
    """
    Functional test
    Ensure a restaurant can be published 
    """
    restaurant.phone = "250-555-0123"
    restaurant.latitude = 49.88
    restaurant.longitude = -119.49
    restaurant.is_published = False
    
    mock_repo.load_all.return_value = [restaurant]

    response, status = service.publish_restaurant(restaurant.id)

    assert status == 200
    assert "is now published" in response["message"]

    assert restaurant.is_published is True

    mock_repo.save_all.assert_called_once()

def test_publish_restaurant_missing_data(service, mock_repo, restaurant):
    """
    Equivalence Partitioning
    Testing the minimum requirements (phone/coords)
    for the 'Published' state.
    """
    restaurant.phone = ""
    mock_repo.load_all.return_value = [restaurant]

    response, status = service.publish_restaurant(restaurant.id)

    assert status == 400
    assert "Missing phone" in response["error"]

# --- View filtering ---

def test_get_filtered_view_forbidden_for_customer(service, mock_repo, restaurant):
    """
    Exception Handling
    Ensure a customer cannot access a restaurant that isnt published
    """
    restaurant.is_published = False
    mock_repo.load_all.return_value = [restaurant]

    response, status = service.get_filtered_view(restaurant.id, "customer")

    assert status == 403
    assert response["error"] == "Restaurant unavailable"

def test_get_filtered_view_strips_sensitive_data(service, mock_repo, restaurant):
    """
    Equivalence Partitioning
    Ensures that the customer only sees public information
    Should not see owner id
    """
    restaurant.is_published = True
    restaurant.owner_id = "secret_123"
    mock_repo.load_all.return_value = [restaurant]

    response, status = service.get_filtered_view(restaurant.id, "customer")

    assert status == 200
    assert "owner_id" not in response
    assert response["id"] == restaurant.id


# --- Handling Boundaries ---

def test_restaurant_latitude_limits(service, mock_repo, restaurant):
    """
    Test Boundary Value
    Tests the edges of the latitude
    """
    mock_repo.load_all.return_value = [restaurant]

    for invalid_lat in [90.1, -90.1]:
        update_data = {"latitude": invalid_lat}
        response, status = service.update_restaurant_details(restaurant.id, update_data)
        
        assert status == 400
        assert "Latitude must be between -90 and 90" in response["error"]
    

def test_restaurant_longitude_limits(service, mock_repo, restaurant):
    """
    Test Boundary Value
    Tests the edges of the longitude
    """
    mock_repo.load_all.return_value = [restaurant]

    for invalid_lon in [180.1, -180.1]:
        update_data = {"longitude": invalid_lon}
        response, status = service.update_restaurant_details(restaurant.id, update_data)
        
        assert status == 400
        assert "Longitude must be between -180 and 180" in response["error"]

def test_restaurant_time_limits(service, mock_repo, restaurant):
    """
    Test Boundary Value
    Test edges of the 2400 clock
    """
    mock_repo.load_all.return_value = [restaurant]
    update_data = {"open_time": 2500}
    
    response, status = service.update_restaurant_details(restaurant.id, update_data)
    
    assert status == 400
    assert "Invalid time format" in response["error"]

def test_update_restaurant_invalid_time_order(service, mock_repo, restaurant):
    """
    Logic/Boundary Test
    Ensures that open_time cannot be after close_time.
    """
    mock_repo.load_all.return_value = [restaurant]

    invalid_times = {
        "open_time": 1800,
        "close_time": 900
    }
    
    response, status = service.update_restaurant_details(restaurant.id, invalid_times)
    
    assert status == 400
    assert "open_time must be before close_time" in response["error"]


# --- Model Validators ---

def test_restaurant_edge_case_equal_times(service, mock_repo, restaurant):
    """
    Edge Case
    Tests open and close times cannot equal one another
    """
    mock_repo.load_all.return_value = [restaurant]
    update_data = {"open_time": 1200, "close_time": 1200}
    
    response, status = service.update_restaurant_details(restaurant.id, update_data)
    
    assert status == 400
    assert "open_time must be before close_time" in response["error"]
