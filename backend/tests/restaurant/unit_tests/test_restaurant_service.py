# backend/tests/restaurant/unit_tests/test_menu_item_model.py
import pytest
from unittest.mock import MagicMock
from backend.services.restaurant_service import RestaurantService
from backend.schemas.restaurant_schema import Restaurant


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

# --- Assign owner to restaurant ---

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
