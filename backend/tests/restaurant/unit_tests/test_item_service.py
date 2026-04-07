# backend/tests/restaurant/unit_tests/test_item_service.py
from decimal import Decimal

import pytest
from unittest.mock import MagicMock
from pydantic import ValidationError
from backend.services.item_service import MenuService
from backend.schemas.items_schema import CreateMenuItemSchema

@pytest.fixture
def menu_service(mock_item_repo):
    return MenuService(mock_item_repo)

# --- Ownership ---

def test_verify_ownership_not_found(menu_service, mock_item_repo):
    """
    Exception handling
    Ensure 404 is returned if the restaurant ID does not exist in the repo
    """
    mock_item_repo.get_by_id.return_value = None
    
    response, status = menu_service.add_menu_item("1", "999", {})
    
    assert status == 404
    assert response["error"] == "Restaurant not found"

def test_verify_ownership_unauthorized(menu_service, mock_item_repo, restaurant):
    """
    Exception handling
    Ensure 403 is returned if the owner_id doesn't match the restaurant owner
    """
    mock_item_repo.get_by_id.return_value = restaurant
    
    response, status = menu_service.remove_menu_item("99", str(restaurant.id), "item_uuid")
    
    assert status == 403
    assert "You do not own this restaurant" in response["error"]

# --- Add Menu Item ---

def test_add_menu_item_success(menu_service, mock_item_repo, restaurant, raw_menu_item_data):
    """
    Functional test
    Ensure a valid item can be added when ownership is verified
    """
    mock_item_repo.get_by_id.return_value = restaurant
    mock_item_repo.add_menu_item.return_value = True

    response, status = menu_service.add_menu_item(
        restaurant.owner_id, 
        str(restaurant.id), 
        raw_menu_item_data
    )
    
    assert status == 201
    assert response["message"] == "Item added successfully"

    args, _ = mock_item_repo.add_menu_item.call_args
    assert isinstance(args[1], CreateMenuItemSchema)
    assert args[1].name == raw_menu_item_data["item_name"]

def test_validate_data_efficiency_decimal_reuse(menu_service):
    """
    Efficiency Test:
    Ensures the service converts the price to Decimal and puts it back in the dict
    """
    item_data = {"price": "19.99"}
    menu_service._validate_menu_item_data(item_data)
    
    assert isinstance(item_data["price"], Decimal)
    assert item_data["price"] == Decimal("19.99")

def test_add_menu_item_invalid_price(menu_service, mock_item_repo, restaurant, raw_menu_item_data):
    """
    Equivalence Partitioning / Fault injection
    Ensure negative prices trigger a 400 error
    """
    mock_item_repo.get_by_id.return_value = restaurant
    raw_menu_item_data["price"] = -10.00
    
    response, status = menu_service.add_menu_item(
        restaurant.owner_id, 
        str(restaurant.id), 
        raw_menu_item_data
    )
    
    assert status == 400
    assert "Price cannot be negative" in response["error"]

# --- Edit Menu Item ---

def test_edit_menu_item_success(menu_service, mock_item_repo, restaurant):
    """
    Functional test
    Ensure existing item can be updated
    """
    mock_item_repo.get_by_id.return_value = restaurant
    mock_item_repo.update_menu_item.return_value = True
    
    update_data = {"item_name": "Updated Pie", "price": 15.00}
    response, status = menu_service.edit_menu_item(
        restaurant.owner_id, 
        str(restaurant.id), 
        "some-uuid", 
        update_data
    )
    
    assert status == 200
    assert "updated successfully" in response["message"]

# --- Availability Toggle ---

def test_update_item_availability_not_found(menu_service, mock_item_repo, restaurant):
    """
    Equivalence Partitioning
    Test behavior when the item_id doesn't exist in the specific restaurant
    """
    mock_item_repo.get_by_id.return_value = restaurant
    mock_item_repo.update_menu_item_availability.return_value = False
    
    response, status = menu_service.update_item_availability(
        restaurant.owner_id, 
        str(restaurant.id), 
        "missing-item-id", 
        False
    )
    
    assert status == 404
    assert "not found" in response["error"]

def test_update_item_availability_success(menu_service, mock_item_repo, restaurant):
    """
    Equivalence Partitioning
    Ensure the toggle correctly returns the new status when the item exists
    """
    mock_item_repo.get_by_id.return_value = restaurant
    mock_item_repo.update_menu_item_availability.return_value = True

    response, status = menu_service.update_item_availability(
        restaurant.owner_id, str(restaurant.id), "item-123", False
    )
    
    assert status == 200
    assert response["status"] is False
    mock_item_repo.update_menu_item_availability.assert_called_with(str(restaurant.id), "item-123", False)

# --- Remove Menu Item ---

def test_remove_menu_item_success(menu_service, mock_item_repo, restaurant):
    """
    Functional test
    Ensure item removal calls the repository correctly
    """
    mock_item_repo.get_by_id.return_value = restaurant
    mock_item_repo.remove_menu_item.return_value = True
    
    item_id = "item-to-delete-uuid"
    response, status = menu_service.remove_menu_item(
        restaurant.owner_id, 
        str(restaurant.id), 
        item_id
    )
    
    assert status == 200
    assert "removed successfully" in response["message"]
    mock_item_repo.remove_menu_item.assert_called_once_with(str(restaurant.id), item_id)

# --- Validation & Boundary Tests ---

def test_add_menu_item_negative_price(menu_service, mock_item_repo, restaurant, raw_menu_item_data):
    """
    Boundary Value Analysis
    Tests that negative values returns 400
    """
    mock_item_repo.get_by_id.return_value = restaurant
    raw_menu_item_data["price"] = -0.01
    
    response, status = menu_service.add_menu_item(
        restaurant.owner_id, str(restaurant.id), raw_menu_item_data
    )

    assert status == 400
    assert "Price cannot be negative" in response["error"]

def test_add_menu_item_empty_name(menu_service, mock_item_repo, restaurant, raw_menu_item_data):
    """
    Fault Injection
    Tests that names cannot be empty strings or whitespace
    """
    mock_item_repo.get_by_id.return_value = restaurant
    raw_menu_item_data["item_name"] = "   "
    
    response, status = menu_service.add_menu_item(
        restaurant.owner_id, str(restaurant.id), raw_menu_item_data
    )

    assert status == 400
    assert "Name cannot be empty" in response["error"]

def test_add_menu_item_name_non_string_rejects(menu_service, mock_item_repo, restaurant, raw_menu_item_data):
    """
    Fault Injection
    Tests that a non-string name is rejected
    """
    mock_item_repo.get_by_id.return_value = restaurant
    raw_menu_item_data["item_name"] = 12345
    
    response, status = menu_service.add_menu_item(
        restaurant.owner_id, str(restaurant.id), raw_menu_item_data
    )

    assert status == 400
    assert "must be a string" in response["error"].lower()

def test_add_menu_item_invalid_uuid_format(menu_service, mock_item_repo, restaurant, raw_menu_item_data):
    """
    Validation test
    catches bad UUIDS and returns 400
    """
    mock_item_repo.get_by_id.return_value = restaurant
    raw_menu_item_data["id"] = "not-a-valid-uuid"
    
    response, status = menu_service.add_menu_item(
        restaurant.owner_id, str(restaurant.id), raw_menu_item_data
    )

    assert status == 400
    assert "valid UUID" in response["error"]

def test_add_menu_item_tags_standardization(menu_service, mock_item_repo, restaurant, raw_menu_item_data):
    """
    Functional logic
    Ensures tags are all lowercase, stripped, no duplicates before being saved
    """
    mock_item_repo.get_by_id.return_value = restaurant
    raw_menu_item_data["tags"] = [" Pizza ", "pizza", "  HOT  "]
    
    menu_service.add_menu_item(
        restaurant.owner_id, str(restaurant.id), raw_menu_item_data
    )

    args, _ = mock_item_repo.add_menu_item.call_args
    passed_schema = args[1]
    
    assert passed_schema.tags == ["pizza", "hot"]
    assert len(passed_schema.tags) == 2