# backend/tests/restaurant/unit_tests/test_restaurant_repo.py
import json
from unittest.mock import mock_open
from backend.repositories.restaurant_repository import RestaurantRepository
from backend.models.restaurant.restaurant_model import Restaurant

def test_load_valid_data():
    """
    Equivalence Partitioning: Valid input class
    Load all of the data
    """
    fake_data = json.dumps([
        {"id": 1, "name": "The Poseidon", "address": "123 Street", "phone": "555-555-5555"}
    ])

    fake_storage = mock_open(read_data=fake_data)
    repo = RestaurantRepository(storage_service=fake_storage)

    results = repo.load_all()
    
    assert len(results) == 1
    assert results[0].id == 1
    assert results[0].name == "The Poseidon"
    print("✓ Valid data load test passed (Injection)")


def test_load_all_missing_file():
    """
    Equivalence Partitioning (Missing Input Class)
    Handles loading a file that doesnt exist and pass
    a FileNotFoundError
    """
    # mock_open can be told to raise an error when called
    fake_storage = mock_open()
    fake_storage.side_effect = FileNotFoundError
    
    repo = RestaurantRepository(storage_service=fake_storage)
    
    results = repo.load_all()
    
    # Should return an empty list instead of crashing
    assert results == []


def test_load_all_corrupted_data():
    """
    Fault Injection/ Exception Handling:
    Injects corrupted JSON to trigger a JSONDecodeError
    """
    fake_storage = mock_open(read_data="INVALID_JSON_STREAM")
    
    repo = RestaurantRepository(storage_service=fake_storage)
    
    results = repo.load_all()
    
    # Repo should catch the error and return []
    assert results == []


def test_save_all_serialization():
    """
    Functional test:
    Verifies that the repository correctly writes data.
    """
    fake_storage = mock_open()
    repo = RestaurantRepository(storage_service=fake_storage)
    
    # Create a real model object to save
    test_res = Restaurant(res_id=10, name="Grayson's Grill", address="Uni Way", phone="555-0000")
    
    success = repo.save_all([test_res])
    
    assert success is True
    
    # Check that the file was actually written to
    handle = fake_storage()
    written_content = "".join(call.args[0] for call in handle.write.call_args_list)
    assert '"id": 10' in written_content
    assert '"name": "Grayson\'s Grill"' in written_content
