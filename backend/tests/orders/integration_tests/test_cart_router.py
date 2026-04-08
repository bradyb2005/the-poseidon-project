# backend/tests/orders/integration_tests/test_cart_router.py
import pytest
from backend.main import app
from backend.routes.cart_router import get_cart_service

@pytest.fixture
def mock_cart_service(client):
    """
    Injects the mock service into the FastAPI dependency system
    """
    from unittest.mock import MagicMock
    mock = MagicMock()
    
    app.dependency_overrides[get_cart_service] = lambda: mock
    
    yield mock

    app.dependency_overrides = {}

# --- POST tests ---

def test_post_add_item_to_cart_success(client, mock_cart_service, valid_uuids):
    """
    Equivalence Partitioning
    Ensures you can add an item to the cart
    """
    mock_response = {"message": "Item added"}
    mock_cart_service.add_to_cart.return_value = (mock_response, 200)
    
    payload = {"menu_item_id": valid_uuids["item_1"], "quantity": 2}
    response = client.post("/cart/user_1/items", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Item added"


def test_post_add_item_to_cart_not_found(client, mock_cart_service, valid_uuids):
    """
    Exception Handling
    Tries to add an item that doesn't exist
    """
    mock_error = {"error": "Menu item not found"}
    mock_cart_service.add_to_cart.return_value = (mock_error, 404)

    payload = {"menu_item_id": valid_uuids["item_1"], "quantity": 1}
    response = client.post("/cart/user_1/items", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Menu item not found"

# --- PUT tests ---

def test_put_update_cart_item_quantity(client, mock_cart_service, valid_uuids):
    """
    Equivalence Partitioning
    Ensures you can update the quantity of a cart item
    """
    mock_response = {"message": "Updated"}
    mock_cart_service.update_quantity.return_value = (mock_response, 200)

    payload = {"new_quantity": 5}
    response = client.put(f"/cart/user_1/items/{valid_uuids['item_1']}", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Updated"

# --- DELETE tests ---

def test_delete_remove_cart_item(client, mock_cart_service, valid_uuids):
    """
    Equivalence Partitioning
    Ensures you can remove an item from the cart
    """
    mock_response = {"message": "Removed"}
    mock_cart_service.remove_from_cart.return_value = (mock_response, 200)

    response = client.delete(f"/cart/user_1/items/{valid_uuids['item_1']}")

    assert response.status_code == 200
    assert response.json()["message"] == "Removed"


def test_delete_clear_customer_cart(client, mock_cart_service):
    """
    Equivalence Partitioning
    Ensures you can clear the entire cart
    """
    mock_response = {"message": "Cleared"}
    mock_cart_service.clear_cart.return_value = (mock_response, 200)

    response = client.delete("/cart/user_1")

    assert response.status_code == 200
    assert response.json()["message"] == "Cleared"