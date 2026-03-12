# backend/tests/restaurant/unit_tests/test_menu_service.py
import pytest
from unittest.mock import MagicMock
from backend.services.menu_item_service import MenuService, EntityNotFoundError


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def menu_service(mock_repo):
    return MenuService(repository=mock_repo)


def test_update_availability_success(menu_service, mock_repo):
    mock_restaurant = MagicMock(id=10)
    mock_item = MagicMock(id=1, restaurant_id=10, availability=True)

    mock_repo.get_restaurant_by_id.return_value = mock_restaurant
    mock_repo.get_menu_item_by_id.return_value = mock_item

    result = menu_service.update_item_availability(10, 1, False)

    assert result.availability is False
    mock_repo.save.assert_called_once_with(mock_item)

# --- Error handling ---


def test_update_availability_restaurant_not_found(menu_service, mock_repo):
    # Edge case: Test if menu item can be updated if no restaurant is connected
    mock_repo.get_restaurant_by_id.return_value = None

    with pytest.raises(EntityNotFoundError) as exc:
        menu_service.update_item_availability(99, 1, False)

    assert "Restaurant with ID 99 not found" in str(exc.value)


def test_update_availability_item_not_found(menu_service, mock_repo):
    # Edge case: Test when restaurant exists but item does not
    mock_repo.get_restaurant_by_id.return_value = MagicMock(id=10)
    mock_repo.get_menu_item_by_id.return_value = None

    with pytest.raises(EntityNotFoundError) as exc:
        menu_service.update_item_availability(10, 555, False)

    assert "Menu Item with ID 555 not found" in str(exc.value)


def test_update_availability_wrong_restaurant(menu_service, mock_repo):
    # Edge case: Item belongs but is in a different restaurant
    mock_repo.get_restaurant_by_id.return_value = MagicMock(id=10)
    mock_item = MagicMock(id=1, restaurant_id=20)
    mock_repo.get_menu_item_by_id.return_value = mock_item

    with pytest.raises(EntityNotFoundError) as exc:
        menu_service.update_item_availability(10, 1, False)

    assert "does not belong to Restaurant 10" in str(exc.value)
