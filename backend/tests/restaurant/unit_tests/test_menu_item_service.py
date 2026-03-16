# backend/tests/restaurant/unit_tests/test_menu_service.py
import pytest
from unittest.mock import MagicMock
# Cannot fix flaking error or will break best practice for code (redundancy)
from backend.services.menu_item_service import MenuService, EntityNotFoundError, PermissionError
from backend.models.restaurant.menu_item_model import MenuItem


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def menu_service(mock_repo):
    return MenuService(repository=mock_repo)

# --- Crud Operations ---


def test_add_menu_item_success(menu_service, mock_repo):
    # Feat2-FR4: Functional Test:
    # tests that adding menu item is successful
    mock_repo.get_by_id.return_value = {
        "id": 123, "owner_id": 1, "menu": []}
    item_data = {"name": "New Burger", "price": 10.99, "tags": ["New"]}

    menu_service.add_menu_item(
        owner_id=1, restaurant_id=123, item_data=item_data)

    args, _ = mock_repo.add_menu_item.call_args
    assert args[0] == 123
    assert args[1].name == "New Burger"


def test_update_availability_success(menu_service, mock_repo):
    # Edge case: Update availabilitiy of a menu item
    mock_repo.get_by_id.return_value = {"id": 10, "owner_id": 1}
    mock_repo.update_menu_item.return_value = True

    result = menu_service.update_item_availability(
        1, 10, 1, False)

    assert result is True
    mock_repo.update_menu_item_availability.assert_called_once_with(
        10, 1, False)


def test_edit_menu_item_success(menu_service, mock_repo):
    # Feat2-FR4: Functional test to ensure you can edit a menu item
    mock_repo.get_by_id.return_value = {"id": "res_123", "owner_id": 1}
    mock_repo.update_menu_item.return_value = True

    updated_data = {"name": "Cheeseburger", "price": 12.99}

    result = menu_service.edit_menu_item(
        1, "res_123", "item_001", updated_data)

    assert result is True
    mock_repo.update_menu_item.assert_called_once()


def test_remove_menu_item_success(menu_service, mock_repo):
    # Feat2-FR4: Functional test to ensure you can remove an item
    mock_repo.get_by_id.return_value = {"id": "res_123", "owner_id": 1}
    mock_repo.remove_menu_item.return_value = True

    result = menu_service.remove_menu_item(1, "res_123", "item_001")

    assert result is True
    mock_repo.remove_menu_item.assert_called_once_with("res_123", "item_001")

# --- Error handling and Permission ---


def test_update_availability_restaurant_not_found(menu_service, mock_repo):
    # Edge case: Test if menu item can be updated if no restaurant is connected
    mock_repo.get_by_id.return_value = None

    with pytest.raises(EntityNotFoundError) as exc:
        menu_service.update_item_availability(1, 99, 1, False)

    assert "Restaurant with ID 99 not found" in str(exc.value)


def test_update_availability_item_not_found(menu_service, mock_repo):
    # Edge case: Test when restaurant exists but item does not
    mock_repo.get_by_id.return_value = {"id": "res_10", "owner_id": 1}
    mock_repo.update_menu_item_availability.return_value = False

    with pytest.raises(EntityNotFoundError) as exc:
        menu_service.update_item_availability(1, "res_10", "555", False)

    assert "Menu Item with ID 555 not found" in str(exc.value)


def test_unauthorized_owner_access(menu_service, mock_repo):
    # Edge case: User 2 tries to modify User 1's restaurant
    mock_repo.get_by_id.return_value = {"id": "res_123", "owner_id": 1}

    with pytest.raises(PermissionError) as exc:
        menu_service.update_item_availability(
            2, "res_123", "item_001", False)
    assert "Access denied" in str(exc.value)
