# backend/tests/restaurant/integration_tests/test_item_router.py
import pytest
from backend.main import app
from backend.dependencies import get_menu_service

@pytest.fixture
def mock_menu_service(client):
    """
    Injects the mock MenuService into the FastAPI dependency system.
    """
    from unittest.mock import MagicMock
    mock = MagicMock()

    app.dependency_overrides[get_menu_service] = lambda: mock
    
    yield mock

    app.dependency_overrides = {}

# --- POST Tests (Add Item) ---

def test_add_menu_item_success(client, mock_menu_service, restaurant, raw_menu_item_data):
    """
    Equivalence Partitioning
    Verifies that a valid menu item can be added to a restaurant.
    """
    mock_response = {"message": "Item added successfully", "item_id": "uuid-123"}
    mock_menu_service.add_menu_item.return_value = (mock_response, 201)


    response = client.post(
        f"/restaurants/{restaurant.id}/items",
        json=raw_menu_item_data,
        headers={"owner-id": str(restaurant.owner_id)}
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Item added successfully"
    assert "item_id" in response.json()


def test_add_menu_item_unauthorized(client, mock_menu_service, restaurant, raw_menu_item_data):
    """
    Exception Handling
    Ensures a 403 is returned if the user does not own the restaurant.
    """
    mock_error = {"error": "You do not own this restaurant"}
    mock_menu_service.add_menu_item.return_value = (mock_error, 403)

    response = client.post(
        f"/restaurants/{restaurant.id}/items",
        json=raw_menu_item_data,
        headers={"owner-id": "wrong-owner-id"}
    )

    assert response.status_code == 403
    assert "do not own" in response.json()["detail"]

# --- PUT Tests ---

def test_edit_menu_item_success(client, mock_menu_service, restaurant):
    """
    Equivalence Partitioning
    Verifies that an existing menu item can be updated.
    """
    mock_response = {"message": "Item updated successfully"}
    mock_menu_service.edit_menu_item.return_value = (mock_response, 200)

    update_payload = {"item_name": "Updated Burger", "price": 12.99}
    item_id = "some-uuid"

    response = client.put(
        f"/restaurants/{restaurant.id}/items/{item_id}",
        json=update_payload,
        headers={"owner-id": str(restaurant.owner_id)}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Item updated successfully"

# --- DELETE Tests ---

def test_delete_menu_item_success(client, mock_menu_service, restaurant):
    """
    Equivalence Partitioning
    Verifies that a menu item can be removed.
    """
    mock_response = {"message": "Item removed successfully"}
    mock_menu_service.remove_menu_item.return_value = (mock_response, 200)

    item_id = "delete-me-uuid"

    response = client.delete(
        f"/restaurants/{restaurant.id}/items/{item_id}",
        headers={"owner-id": str(restaurant.owner_id)}
    )

    assert response.status_code == 200
    assert "removed" in response.json()["message"]

def test_delete_menu_item_not_found(client, mock_menu_service, restaurant):
    """
    Exception Handling
    Ensures 404 is returned if the item doesn't exist.
    """
    mock_error = {"error": "Item not found"}
    mock_menu_service.remove_menu_item.return_value = (mock_error, 404)

    response = client.delete(
        f"/restaurants/{restaurant.id}/items/fake-id",
        headers={"owner-id": str(restaurant.owner_id)}
    )

    assert response.status_code == 404
    assert "Item not found" in response.json()["detail"]