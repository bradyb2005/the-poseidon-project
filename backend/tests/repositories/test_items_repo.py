# backend/tests/repositories/test_items_repo.py
import json
from decimal import Decimal
from uuid import uuid4
from unittest.mock import MagicMock, mock_open, patch
from backend.repositories.items_repository import ItemRepository
from backend.schemas.items_schema import MenuItem


@patch("backend.repositories.items_repository.json.loads")
@patch("pathlib.Path.exists")
def test_load_valid_data(mock_exists, mock_json_loads):
    """
    Valid Equivalence Partitioning/ Mocking
    Load all of the data and verify hydration of defaults.
    """
    mock_exists.return_value = True
    # Mimicking your raw data format (missing price and id)
    mock_json_loads.return_value = ([
        {
            "item_name": "Beef pie",
            "restaurant_id": 1
        }
    ])

    with patch("backend.repositories.items_repository.open", mock_open(read_data="valid_json")):
        repo = ItemRepository()
        results = repo.load_all()

    assert len(results) == 1
    assert results[0].name == "Beef pie"
    assert results[0].restaurant_id == 1
    assert results[0].price == Decimal("0.01")
    assert results[0].item_id is not None


@patch("pathlib.Path.exists")
def test_load_all_missing_file(mock_exists):
    """
    Invalid Equivalence Partitioning
    Handles loading a file that doesn't exist.
    """
    mock_exists.return_value = False
    repo = ItemRepository()
    results = repo.load_all()

    # Should return an empty list instead of crashing
    assert results == []

@patch("pathlib.Path.exists")
@patch("backend.repositories.items_repository.json.loads")
def test_load_all_corrupted_data(mock_json_loads, mock_exists):
    """
    Fault Injection/ Exception Handling:
    Injects corrupted JSON to trigger a JSONDecodeError.
    """
    mock_exists.return_value = True
    mock_json_loads.side_effect = json.JSONDecodeError("Invalid JSON", "...", 0)

    with patch("backend.repositories.items_repository.open", mock_open(read_data="corrupted")):
        repo = ItemRepository()
        results = repo.load_all()

    # Repo should catch the error and return []
    assert results == []


@patch("backend.repositories.items_repository.open", new_callable=mock_open)
def test_save_all_serialization(mock_file):
    """
    Mocking Functionality
    Verifies that the repository correctly writes data using aliases
    """
    repo = ItemRepository()
    item_uuid = uuid4()

    test_item = MenuItem(
        item_name="Briyani rice",
        restaurant_id=1,
        id=item_uuid,
        price=Decimal("15.50"),
        tags=["spicy", "rice"]
    )

    success = repo.save_all([test_item])

    assert success is True

    handle = mock_file()
    written_content = "".join(call.args[0] for call in handle.write.call_args_list)

    assert '"item_name": "Briyani rice"' in written_content
    assert f'"id": "{str(item_uuid)}"' in written_content
    assert '"price": "15.50"' in written_content

@patch.object(ItemRepository, 'load_all')
def test_find_by_id_success(mock_load_all):
    """
    Positive Functional Test
    Verifies that find_by_id correctly returns the matching item.
    """
    repo = ItemRepository()
    
    mock_item_1 = MagicMock()
    mock_item_1.item_id = "target-item"
    
    mock_item_2 = MagicMock()
    mock_item_2.item_id = "other-item"

    mock_load_all.return_value = [mock_item_1, mock_item_2]

    result = repo.find_by_id("target-item")

    assert result == mock_item_1


@patch.object(ItemRepository, 'load_all')
def test_find_by_id_not_found(mock_load_all):
    """
    Negative Functional Test
    Verifies that find_by_id returns None when the target ID does not exist.
    """
    repo = ItemRepository()
    
    mock_item = MagicMock()
    mock_item.item_id = "target-item"

    mock_load_all.return_value = [mock_item]

    result = repo.find_by_id("non-existent-item")

    assert result is None
