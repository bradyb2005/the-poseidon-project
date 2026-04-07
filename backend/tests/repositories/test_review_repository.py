# backend/tests/repositories/test_review_repository.py
import pytest
import json
import os
from pathlib import Path
from datetime import datetime
from backend.repositories.review_repository import ReviewRepository
from backend.schemas.review_schema import ReviewDisplay

@pytest.fixture
def temp_review_file(tmp_path):
    """Creates a temporary JSON file for testing."""
    d = tmp_path / "data"
    d.mkdir()
    f = d / "reviews_test.json"
    return str(f)

@pytest.fixture
def sample_reviews():
    """Generates a list of ReviewDisplay objects for testing."""
    return [
        ReviewDisplay(
            id="rev-1",
            order_id="ord-101",
            customer_id="cust-1",
            restaurant_id=1,
            rating=5,
            comment="Amazing!",
            created_at=datetime.now()
        ),
        ReviewDisplay(
            id="rev-2",
            order_id="ord-102",
            customer_id="cust-2",
            restaurant_id=1,
            rating=3,
            comment="Average.",
            created_at=datetime.now()
        )
    ]

# --- Initialization Tests ---

def test_repo_initialization_default_path():
    """
    Initialization Test
    Ensures the repo defaults to the correct directory structure.
    """
    repo = ReviewRepository()
    assert "data" in str(repo._file_path)
    assert repo._file_path.name == "reviews.json"

def test_repo_creates_directory_if_missing(tmp_path):
    """
    Equivalence Partitioning
    Ensures the repo creates the 'data' folder if it doesn't exist.
    """
    nested_path = tmp_path / "new_folder" / "test.json"
    ReviewRepository(file_path=str(nested_path))
    assert nested_path.parent.exists()

# --- Save and Load Tests ---

def test_save_all_success(temp_review_file, sample_reviews):
    """
    Functional Test/ Mocking
    Tests if the repo correctly serializes and writes to JSON.
    """
    repo = ReviewRepository(file_path=temp_review_file)
    success = repo.save_all(sample_reviews)
    
    assert success is True
    assert os.path.exists(temp_review_file)

    with open(temp_review_file, 'r') as f:
        data = json.load(f)
        assert len(data) == 2
        assert data[0]["id"] == "rev-1"
        assert isinstance(data[0]["created_at"], str)

def test_load_all_success(temp_review_file, sample_reviews):
    """
    Functional Test
    Tests if the repo correctly reads JSON and returns Pydantic objects
    """
    repo = ReviewRepository(file_path=temp_review_file)
    repo.save_all(sample_reviews)
    
    loaded_reviews = repo.load_all()
    assert len(loaded_reviews) == 2
    assert isinstance(loaded_reviews[0], ReviewDisplay)
    assert loaded_reviews[0].rating == 5
    assert loaded_reviews[1].order_id == "ord-102"

def test_load_all_empty_file(temp_review_file):
    """
    Equivalence Partitioning
    Ensures load_all returns an empty list if file doesn't exist.
    """
    repo = ReviewRepository(file_path=temp_review_file)
    assert repo.load_all() == []

def test_load_all_invalid_json(temp_review_file):
    """
    Equivalence Partitioning
    Ensures load_all handles corrupted JSON gracefully.
    """
    with open(temp_review_file, 'w') as f:
        f.write("not a json string")
    
    repo = ReviewRepository(file_path=temp_review_file)
    assert repo.load_all() == []

# --- Serialization Consistency ---

def test_serialization_round_trip(temp_review_file, sample_reviews):
    """
    Serialization Test
    Ensures data integrity remains after a save and a load.
    Checks that datetime objects are handled correctly.
    """
    repo = ReviewRepository(file_path=temp_review_file)
    repo.save_all(sample_reviews)
    loaded = repo.load_all()
    
    assert loaded[0].created_at.year == sample_reviews[0].created_at.year
    assert loaded[0].comment == sample_reviews[0].comment