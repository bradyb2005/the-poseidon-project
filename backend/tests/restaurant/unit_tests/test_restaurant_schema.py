# backend/tests/restaurant/unit_tests/test_restaurant_schema.py
import pytest
from pydantic import ValidationError
from backend.schemas.restaurant_schema import Restaurant, UpdateRestaurantSchema

@pytest.fixture
def base_json_data():
    return{
        "id": 1,
        "name": "Restaurant 1",
        "menu": ["Beef Pie", "Burger"]
    }

@pytest.fixture
def optional_metadata():
    return{
        "open_time": 900,
        "close_time": 2200,
        "latitude": 49.49,
        "longitude": -149.49,
        "is_published": True,
        "phone": "555-555-5555"
    }

@pytest.fixture
def full_restaurant_data(base_json_data, optional_metadata):
    """Combines both for testing a fully populated model."""
    return {**base_json_data, **optional_metadata}

# --- Initialization tests ---

def test_restaurant_schema_initialization(base_json_data):
    """
    Equivalence Partitioning
    Ensures that the mandatory data is correctly mapped to the schema
    """
    restaurant = Restaurant(**base_json_data)
    assert restaurant.id == 1
    assert restaurant.name == "Restaurant 1"
    assert "Burger" in restaurant.menu

def test_restaurant_populate_by_alias_and_name():
    """
    Functional logic test
    Tests that populate_by_name accepts name and alias
    """
    data_with_alias = {"id": 1, "name": "A", "menu": [], "_phone": "123"}
    data_with_name = {"id": 1, "name": "A", "menu": [], "phone": "123"}
    
    assert Restaurant(**data_with_alias).phone == "123"
    assert Restaurant(**data_with_name).phone == "123"

def test_restaurant_missing_mandatory_fields():
    """
    Exception Handling
    Ensures a Validation Error is raised when
    a mandatory field is missing
    """
    with pytest.raises(ValidationError) as exc_info:
        Restaurant(id=1)
    
    assert "name" in str(exc_info.value)
    assert "menu" in str(exc_info.value)


# --- Handling Boundaries ---


def test_restaurant_latitude_limits(base_json_data):
    """
    Test Boundary Value
    Tests the edges of the latitude
    """
    # Valid boundaries
    base_json_data["latitude"] = 90.0
    assert Restaurant(**base_json_data).latitude == 90.0
    base_json_data["latitude"] = -90.0
    assert Restaurant(**base_json_data).latitude == -90.0
    
    # Invalid boundaries
    for invalid_lat in [90.1, -90.1]:
        base_json_data["latitude"] = invalid_lat
        with pytest.raises(ValidationError):
            Restaurant(**base_json_data)

def test_restaurant_longitude_limits(base_json_data):
    """
    Test Boundary Value
    Tests the edges of the longitude
    """
    # Valid boundaries
    base_json_data["longitude"] = 180.0
    assert Restaurant(**base_json_data).longitude == 180.0
    base_json_data["longitude"] = -180.0
    assert Restaurant(**base_json_data).longitude == -180.0

    # Invalid boundaries
    for invalid_lon in [180.1, -180.1]:
        base_json_data["longitude"] = invalid_lon
        with pytest.raises(ValidationError):
            Restaurant(**base_json_data)


def test_restaurant_time_limits(base_json_data):
    """
    Test Boundary Value
    Test edges of the 2400 clock
    """
    # Test lower boundary
    base_json_data["open_time"] = 0
    assert Restaurant(**base_json_data).open_time == 0

    # Test invalid upper boundary
    base_json_data["open_time"] = 2401
    with pytest.raises(ValidationError):
        Restaurant(**base_json_data)


# --- Model Validators ---


def test_restaurant_edge_case_equal_times(base_json_data):
    """
    Edge Case
    Tests open and close times cannot equal one another
    """
    base_json_data["open_time"] = 1200
    base_json_data["close_time"] = 1200
    with pytest.raises(ValidationError, match="open_time must be before close_time"):
        Restaurant(**base_json_data)


def test_restaurant_invalid_time(base_json_data):
    """
    Fault injection
    Tests handling invalid data in open time
    to trigger the field validator logic
    """
    base_json_data["open_time"] = 2500
    with pytest.raises(ValidationError, match="Invalid time format"):
        Restaurant(**base_json_data)


# --- Update tests ---

def test_update_functional_partial_update():
    """
    Functional Test
    Tests that changing a field doesn't require changing other fields 
    """
    update_data = {"name": "Updated Name"}
    update_obj = UpdateRestaurantSchema(**update_data)
    assert update_obj.name == "Updated Name"
    assert update_obj.menu is None


def test_update_schema_with_partial_none():
    """
    Functional Test
    Tests that updating a field while others are none still passes
    """
    update_data = {"name": "New Name"}
    try:
        UpdateRestaurantSchema(**update_data)
    except ValidationError as e:
        pytest.fail(f"UpdateRestaurantSchema failed on partial update: {e}")


# --- Serialization test ---

def test_restaurant_serialization(full_restaurant_data):
    """
    Serialization
    Mocks the behaviour of the repository and uses model_dump properly
    """
    restaurant = Restaurant(**full_restaurant_data)
    db_ready_data = restaurant.model_dump(by_alias=True, exclude_none=True)

    assert "id" in db_ready_data
    assert "_phone" in db_ready_data
    assert "_open_time" in db_ready_data
