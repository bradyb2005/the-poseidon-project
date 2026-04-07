# backend/tests/restaurant/unit_tests/test_restaurant_schema.py
from decimal import Decimal

import pytest
from pydantic import ValidationError
from backend.schemas.restaurant_schema import PaginatedRestaurantResponse, Restaurant, UpdateRestaurantSchema

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

# --- Pagination Schema Tests ---

def test_paginated_restaurant_response_initialization(base_json_data):
    """
    Functional
    Ensures the pagination wrapper correctly accepts metadata and a list of restaurants.
    """
    paginated_data = {
        "items": [base_json_data],  # List containing one raw dict
        "total_count": 1,
        "page": 1,
        "per_page": 20,
        "has_next": False,
        "total_pages": 1
    }
    
    response = PaginatedRestaurantResponse(**paginated_data)
    
    assert len(response.items) == 1
    assert isinstance(response.items[0], Restaurant)
    assert response.items[0].name == "Restaurant 1"
    assert response.total_count == 1


def test_paginated_restaurant_response_empty():
    """
    Edge Case
    Ensures the schema handles an empty list of restaurants for the homepage.
    """
    empty_data = {
        "items": [],
        "total_count": 0,
        "page": 1,
        "per_page": 20,
        "has_next": False,
        "total_pages": 0
    }
    
    response = PaginatedRestaurantResponse(**empty_data)
    assert response.items == []
    assert response.total_count == 0

def test_restaurant_detail_response_logic(base_json_data, raw_menu_item_data):
    """
    Functional
    Tests that RestaurantDetailResponse correctly nests MenuItem objects.
    """
    from backend.schemas.restaurant_schema import RestaurantDetailResponse

    detail_data = {
        **base_json_data,
        "full_menu_details": [raw_menu_item_data]
    }
    
    response = RestaurantDetailResponse(**detail_data)
    
    assert response.id == base_json_data["id"]
    assert len(response.full_menu_details) == 1
    assert response.full_menu_details[0].name == "Beef Pie"
    assert isinstance(response.full_menu_details[0].price, Decimal)