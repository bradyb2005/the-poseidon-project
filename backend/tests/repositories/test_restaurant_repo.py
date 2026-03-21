# backend/tests/restaurant/unit_tests/test_restaurant_repo.py
import json
from unittest.mock import mock_open, patch
from backend.repositories.restaurant_repository import RestaurantRepository
from backend.models.restaurant.restaurant_model import Restaurant

@patch("backend.repositories.restaurant_repository.open", new_callable=mock_open)
@patch("pathlib.Path.exists")
def test_load_valid_data(mock_exists, mock_file):
    """
    Equivalence Partitioning: Valid input class
    Load all of the data
    """
    mock_exists.return_value = True
    fake_data = json.dumps([
        {"id": 1, "name": "The Poseidon", "address": "123 Street", "phone": "555-555-5555"}
    ])
    mock_file.return_value.read.return_value = fake_data

    repo = RestaurantRepository()
    results = repo.load_all()
    
    assert len(results) == 1
    assert results[0].id == 1
    assert results[0].name == "The Poseidon"


@patch("pathlib.Path.exists")
def test_load_all_missing_file(mock_exists):
    """
    Equivalence Partitioning (Missing Input Class)
    Handles loading a file that doesnt exist and pass
    a FileNotFoundError
    """
    mock_exists.return_value = False
    repo = RestaurantRepository()
    results = repo.load_all()
    
    # Should return an empty list instead of crashing
    assert results == []


@patch("backend.repositories.restaurant_repository.open", new_callable=mock_open, read_data="INVALID_JSON_STREAM")
@patch("pathlib.Path.exists")
def test_load_all_corrupted_data(mock_exists, mock_file):
    """
    Fault Injection/ Exception Handling:
    Injects corrupted JSON to trigger a JSONDecodeError
    """
    mock_exists.return_value = True
    
    repo = RestaurantRepository()
    results = repo.load_all()
    
    # Repo should catch the error and return []
    assert results == []


@patch("backend.repositories.restaurant_repository.open", new_callable=mock_open)
def test_save_all_serialization(mock_file):
    """
    Functional test:
    Verifies that the repository correctly writes data.
    """
    repo = RestaurantRepository()

    test_res = Restaurant(id=10, name="Grayson's Grill", address="Uni Way", phone="555-0000")
    
    success = repo.save_all([test_res])
    
    assert success is True
    
    # Check that the file was actually written to
    handle = mock_file()

    written_content = "".join(call.args[0] for call in handle.write.call_args_list)
    assert '"id": 10' in written_content
    assert "Grayson's Grill" in written_content
