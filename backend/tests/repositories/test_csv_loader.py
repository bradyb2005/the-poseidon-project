# backend/tests/repositories/test_csv_loader.py
import pytest
import csv
from pathlib import Path
from backend.repositories.csv_loader import load_csv, validate_csv, EXPECTED_COLUMNS


@pytest.fixture
def mock_csv(tmp_path):
    """Helper to create a temporary CSV file with custom content."""
    def _create(filename, headers, rows):
        file_path = tmp_path / filename
        with open(file_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        return file_path
    return _create


def test_load_csv_success(mock_csv):
    """
    Feature 2
    Functional Test: Tests to ensure CSV is loaded properly
    """
    headers = ["order_id", "customer_id"]
    rows = [{"order_id": "1", "customer_id": "CUST100"}]
    path = mock_csv("test.csv", headers, rows)

    data = load_csv(path)
    assert len(data) == 1
    assert data[0]["order_id"] == "1"


def test_validate_csv_valid_data(mock_csv):
    """
    Feature 2
    Functional Test: Ensures we are retrieving the
    correct data
    """
    valid_row = {col: "val" for col in EXPECTED_COLUMNS}
    valid_row.update({
        "restaurant_id": "123",
        "age": "25",
        "delivery_distance": "5.5",
        "order_value": "20.0",
        "route_efficiency": "0.95",
        "small_route": "true",
        "bike_friendly_route": "no",
        "customer_id": "USER_1"
    })

    path = mock_csv("valid.csv", EXPECTED_COLUMNS, [valid_row])
    is_valid, errors = validate_csv(path)

    assert is_valid is True
    assert len(errors) == 0

## --- Edge case tests ---


def test_load_csv_file_not_found():
    """
    Feature 2
    Edge case: Tests loading a file that
    cannot be found
    """
    with pytest.raises(FileNotFoundError):
        load_csv("non_existent_file.csv")


def test_validate_csv_header_mismatch(mock_csv):
    """
    Feature 2
    Edge case: Tests validating data that is in the wrong
    order or missing columns
    """
    path = mock_csv("bad_header.csv", ["wrong_col"], [{"wrong_col": "data"}])
    is_valid, errors = validate_csv(path)

    assert is_valid is False
    assert any("Header mismatch" in e for e in errors)

@pytest.mark.parametrize("column, bad_value", [
    ("restaurant_id", "not_an_int"),
    ("delivery_distance", "five_miles"),
    ("small_route", "maybe"),
    ("customer_id", " ")
    ])


def test_validate_csv_invalid_types(mock_csv, column, bad_value):
    """
    Feature 2
    Edge case: Try to validate CSV of invalid types
    """
    row = {col: "1" for col in EXPECTED_COLUMNS}
    row[column] = bad_value

    path = mock_csv("invalid_type.csv", EXPECTED_COLUMNS, [row])
    is_valid, errors = validate_csv(path)

    assert is_valid is False
    assert any(column in e for e in errors)


def test_validate_empty_csv(mock_csv):
    """
    Feature 2
    Edge case: Tries to validate an empty CSV
    """
    # File with only headers
    path = mock_csv("empty.csv", EXPECTED_COLUMNS, [])
    is_valid, errors = validate_csv(path)

    assert is_valid is False
    assert "empty" in errors[0].lower()
