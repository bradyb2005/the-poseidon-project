# backend/tests/repositories/test_order_repo.py
import json
from pathlib import Path
import pytest
from unittest.mock import mock_open, patch
from backend.repositories.order_repo import OrderRepository

@patch("backend.repositories.order_repo.json.load")
@patch("backend.repositories.order_repo.open", new_callable=mock_open)
@patch("pathlib.Path.exists")
def test_load_all_valid_data(mock_exists, mock_file, mock_json_load):
    """
    Valid Equivalence Partitioning
    Load all of the order data from the JSON file
    """
    mock_exists.return_value = True
    fake_orders = [
        {"id": "abc123A", 
         "customer_id": "brady_b", 
         "status": "unpaid"}
    ]
    mock_json_load.return_value = fake_orders

    repo = OrderRepository()
    results = repo.load_all()
    
    assert len(results) == 1
    assert results[0]["id"] == "abc123A"
    assert results[0]["customer_id"] == "brady_b"


@patch("pathlib.Path.exists")
def test_load_all_missing_file(mock_exists):
    """
    Invalid Equivalence Partitioning
    Handles loading a file that doesn't exist by returning an empty list
    """
    mock_exists.return_value = False
    
    repo = OrderRepository()
    results = repo.load_all()
    
    assert results == []


@patch("backend.repositories.order_repo.json.load")
@patch("backend.repositories.order_repo.open", new_callable=mock_open) 
@patch("pathlib.Path.exists")
def test_load_all_corrupted_data(mock_exists, mock_file, mock_json_load):
    """
    Fault Injection/ Exception Handling
    Injects corrupted JSON to trigger a JSONDecodeError
    """
    mock_exists.return_value = True
    
    mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "", 0)

    repo = OrderRepository()
    results = repo.load_all()
    
    assert results == []


@patch("backend.repositories.order_repo.open", new_callable=mock_open)
def test_save_all_serialization(mock_file):
    """
    Mocking Functionality
    Verifies that the repository correctly writes data to the file
    """
    repo = OrderRepository()
    test_orders = [
        {"id": "xyz789B", 
         "customer_id": "test_user", 
         "status": "paid"}
    ]
    
    repo.save_all(test_orders)
    
    mock_file.assert_called_once_with(Path('backend/data/orders.json'), 'w')
    
    handle = mock_file()
    written_content = "".join(call.args[0] for call in handle.write.call_args_list)
    
    assert '"id": "xyz789B"' in written_content
    assert '"customer_id": "test_user"' in written_content

@patch.object(OrderRepository, 'load_all')
def test_find_by_id_success(mock_load_all):
    """
    Positive Functional Test
    Verifies that find_by_id correctly returns the matching order dictionary.
    """
    repo = OrderRepository()
    
    mock_load_all.return_value = [
        {"id": "abc123A", "customer_id": "user_1"},
        {"id": "xyz789B", "customer_id": "user_2"}
    ]

    result = repo.find_by_id("xyz789B")

    assert result == {"id": "xyz789B", "customer_id": "user_2"}


@patch.object(OrderRepository, 'load_all')
def test_find_by_id_not_found(mock_load_all):
    """
    Negative Functional Test
    Verifies that find_by_id returns None when the target ID does not exist.
    """
    repo = OrderRepository()
    
    mock_load_all.return_value = [
        {"id": "abc123A", "customer_id": "user_1"}
    ]

    result = repo.find_by_id("fake_id_999")

    assert result is None