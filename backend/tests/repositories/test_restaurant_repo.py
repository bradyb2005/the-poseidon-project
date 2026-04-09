# backend/tests/repositories/test_restaurant_repo.py
import json
from unittest.mock import MagicMock, mock_open, patch
from backend.repositories.restaurant_repository import RestaurantRepository
from backend.schemas.restaurant_schema import Restaurant

@patch("backend.repositories.restaurant_repository.open", new_callable=mock_open)
@patch("pathlib.Path.exists")
def test_load_valid_data(mock_exists, mock_file):
    """
    Valid Equivalence Partitioning
    Load all of the data
    """
    mock_exists.return_value = True
    fake_data = json.dumps([{
        "id": 1,
        "name": "The Poseidon",
        "menu": ["Burger"],
        "phone": "555-555-5555"}
    ])
    mock_file.return_value.read.return_value = fake_data

    repo = RestaurantRepository()
    results = repo.load_all()
    
    assert len(results) == 1
    assert results[0].name == "The Poseidon"


@patch("pathlib.Path.exists")
def test_load_all_missing_file(mock_exists):
    """
    Invalid Equivalence Partitioning
    Handles loading a file that doesnt exist and pass
    a FileNotFoundError
    """
    mock_exists.return_value = False
    repo = RestaurantRepository()
    results = repo.load_all()
    
    # Should return an empty list instead of crashing
    assert results == []


@patch("backend.repositories.restaurant_repository.json.load")
@patch("pathlib.Path.exists")
def test_load_all_corrupted_data(mock_exists, mock_json_load):
    """
    Fault Injection/ Exception Handling:
    Injects corrupted JSON to trigger a JSONDecodeError
    """
    mock_exists.return_value = True

    mock_json_load.side_effect = json.JSONDecodeError("Invalid JSON", "INVALID_JSON_STREAM", 0)

    repo = RestaurantRepository()
    results = repo.load_all()
    
    # Repo should catch the error and return []
    assert results == []


@patch("backend.repositories.restaurant_repository.open", new_callable=mock_open)
def test_save_all_serialization(mock_file):
    """
    Mocking Functionality
    Verifies that the repository correctly writes data.
    """
    repo = RestaurantRepository()

    test_res = Restaurant(
        id=10,
        name="Grayson's Grill",
        menu=["Burger"],
        address="123 Street",
        phone="555-555-5555"
        )
    
    success = repo.save_all([test_res])
    
    assert success is True
    
    # Check that the file was actually written to
    handle = mock_file()

    written_content = "".join(call.args[0] for call in handle.write.call_args_list)
    assert '"id": 10' in written_content
    assert "Grayson's Grill" in written_content

@patch.object(RestaurantRepository, 'load_all')
def test_find_by_id_success(mock_load_all):
    """
    Positive Functional Test
    Verifies that find_by_id correctly returns the matching restaurant.
    """
    repo = RestaurantRepository()
    
    mock_rest_1 = MagicMock()
    mock_rest_1.id = 1 
    mock_rest_2 = MagicMock()
    mock_rest_2.id = 2

    mock_load_all.return_value = [mock_rest_1, mock_rest_2]

    result = repo.find_by_id("1")

    assert result == mock_rest_1


@patch.object(RestaurantRepository, 'load_all')
def test_find_by_id_not_found(mock_load_all):
    """
    Negative Functional Test
    Verifies that find_by_id returns None when the target ID does not exist.
    """
    repo = RestaurantRepository()
    
    mock_rest = MagicMock()
    mock_rest.id = 1

    mock_load_all.return_value = [mock_rest]

    result = repo.find_by_id("99")

    assert result is None
