# backend/tests/repositories/test_items_repo.py
import json
from decimal import Decimal
from uuid import uuid4
from unittest.mock import mock_open, patch
from backend.repositories.items_repository import ItemRepository
from backend.schemas.items_schema import MenuItem

@patch("backend.repositories.items_repository.open", new_callable=mock_open)
@patch("pathlib.Path.exists")
def test_load_valid_data(mock_exists, mock_file):
    """
    Valid Equivalence Partitioning/ Mocking
    Load all of the data and verify hydration of defaults.
    """
    mock_exists.return_value = True
    # Mimicking your raw data format (missing price and id)
    fake_raw_data = json.dumps([
        {
            "item_name": "Beef pie",
            "restaurant_id": 1
        }
    ])

    mock_file.return_value.__enter__.return_value.read.return_value = fake_raw_data

    repo = ItemRepository()
    results = repo.load_all()

    assert len(results) == 1
    assert results[0].name == "Beef pie"
    assert results[0].restaurant_id == 1

    assert isinstance(results[0].price, Decimal)
    assert results[0].price == Decimal("0.00")
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


@patch("backend.repositories.items_repository.json.load")
@patch("pathlib.Path.exists")
def test_load_all_corrupted_data(mock_exists, mock_json_load):
    """
    Fault Injection/ Exception Handling:
    Injects corrupted JSON to trigger a JSONDecodeError.
    """
    mock_exists.return_value = True
    mock_json_load.side_effect = json.JSONDecodeError("Invalid JSON", "INVALID_JSON_STREAM", 0)

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
