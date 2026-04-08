# backend/tests/reviews/integration_tests/test_review_routes.py
import pytest
import json
from datetime import datetime
from unittest.mock import mock_open, patch
from pydantic import ValidationError
from backend.repositories.review_repository import ReviewRepository
from backend.schemas.review_schema import ReviewDisplay

@patch("backend.repositories.review_repository.open", new_callable=mock_open)
@patch("pathlib.Path.exists")
def test_load_valid_review_data(mock_exists, mock_file):
    """
    Equivalence Partitioning
    Ensures that valid JSON review data is shown in ReviewDisplay
    """
    mock_exists.return_value = True
    fake_data = json.dumps([{
        "id": "rev-1",
        "order_id": "ord-101",
        "customer_id": "user-1",
        "restaurant_id": 1,
        "rating": 5,
        "comment": "Tastes like victory",
        "created_at": "2026-04-06T22:00:00"
    }])
    mock_file.return_value.__enter__.return_value.read.return_value = fake_data

    repo = ReviewRepository()
    results = repo.load_all()
    
    assert len(results) == 1
    assert results[0].id == "rev-1"
    assert results[0].rating == 5
    assert isinstance(results[0].created_at, datetime)


@patch("pathlib.Path.exists")
def test_load_all_missing_review_file(mock_exists):
    """
    Equivalence Partitioning / Exception Handling
    If the review file doesnt exist, return empty list
    """
    mock_exists.return_value = False
    repo = ReviewRepository()
    results = repo.load_all()

    assert results == []


@patch("backend.repositories.review_repository.open", new_callable=mock_open)
@patch("pathlib.Path.exists")
def test_load_all_corrupted_review_data(mock_exists, mock_file):
    """
    Fault Injection / Exception Handling
    Injects bad JSON to ensure the repository catches JSONDecodeError
    """
    mock_exists.return_value = True

    mock_file.return_value.__enter__.return_value.read.return_value = "{ invalid: json }"

    repo = ReviewRepository()
    results = repo.load_all()

    assert results == []


@patch("backend.repositories.review_repository.open", new_callable=mock_open)
def test_save_all_review_serialization(mock_file):
    """
    Functional Test / Mocking Functionality
    Serializing a ReviewDisplay object 
    """
    repo = ReviewRepository()

    test_rev = ReviewDisplay(
        id="rev-unique",
        order_id="ord-99",
        customer_id="cust-42",
        restaurant_id=5,
        rating=4,
        comment="Good stuff",
        created_at=datetime(2026, 4, 6, 12, 0, 0)
    )
    
    success = repo.save_all([test_rev])
    
    assert success is True

    handle = mock_file()
    written_content = "".join(call.args[0] for call in handle.write.call_args_list)
    
    assert '"id": "rev-unique"' in written_content
    assert '"rating": 4' in written_content

    assert "2026-04-06T12:00:00" in written_content


def test_review_rating_bva():
    """
    Boundary Value Analysis (BVA)
    Ensures repo-bound objects respect the rating boundaries (1 and 5)
    """

    with pytest.raises(ValidationError):
        ReviewDisplay(
            id="rev-1", order_id="o-1", customer_id="c-1", 
            restaurant_id=1, rating=6, created_at=datetime.now()
        )