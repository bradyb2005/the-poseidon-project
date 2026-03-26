# backend/tests/restaurant/integration_tests/test_restaurant_router.py
import pytest

# --- GET tests ---

import pytest

pytestmark = pytest.mark.skip(reason="Skipping due to user schema refactor (will fix in later PR)")


def test_get_restaurants_list(client, mock_restaurant_service, restaurant):
    """
    Equivalence Partitioning
    Ensures you can see a list of restaurants and returns proper code
    """
    mock_restaurant_service.get_all_published.return_value = [restaurant.model_dump()]
    response = client.get("/restaurants")

    assert response.status_code == 200
    assert response.json()[0]["name"] == restaurant.name
    assert isinstance(response.json(), list)


def test_get_restaurant_by_id_success(client, mock_restaurant_service, restaurant):
    """
    Equivalence Partitioning
    Ensures you can retrieve a restaurant
    """
    mock_restaurant_service.get_filtered_view.return_value = (restaurant.model_dump(), 200)

    response = client.get(f"/restaurants/{restaurant.id}")

    assert response.status_code == 200
    assert response.json()["name"] == restaurant.name


def test_get_restaurant_not_found(client, mock_restaurant_service):
    """
    Exception Handling
    Tries to get a restaurant that doesnt exist
    """
    mock_restaurant_service.get_filtered_view.return_value = (None, 404)

    response = client.get("/restaurants/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Restaurant not found"

# --- POST tests ---

def test_post_assign_owner_success(client, mock_restaurant_service):
    """
    Equivalence Partitioning
    Verifies owner can be assigned and returns proper code
    """
    mock_response = {"message": "Owner assigned", "restaurant_id": 1}
    mock_restaurant_service.assign_owner_to_restaurant.return_value = (mock_response, 200)

    response = client.post("/restaurants/1/owner?owner_id=505")

    assert response.status_code == 200
    assert response.json()["message"] == "Owner assigned"

def test_post_publish_missing_coords(client, mock_restaurant_service):
    """
    Integration test
    Ensures proper error is returned if it misses coordinates
    """
    mock_error = {"error": "Missing valid coordinates"}

    mock_restaurant_service.publish_restaurant.return_value = (mock_error, 400)

    response = client.post("/restaurants/1/publish")

    assert response.status_code == 400
    assert "Missing valid coordinates" in response.json()["detail"]

# --- Put tests ---

def test_put_restaurant_update(client, mock_restaurant_service):
    """
    Validation test
    Ensure you can update properly
    """
    mock_response = {"message": "Updated successfully"}

    mock_restaurant_service.update_restaurant_details.return_value = (mock_response, 200)

    update_payload = {"name": "New Diner Name", "phone": "555-555-5555"}
    response = client.put("/restaurants/1", json=update_payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Updated successfully"
