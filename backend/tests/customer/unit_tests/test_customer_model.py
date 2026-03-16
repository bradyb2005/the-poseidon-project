# python3 -m pytest backend/tests/customer/unit_tests/test_customer_model.py
import pytest
from unittest.mock import MagicMock
from backend.models.user.customer_model import Customer
from backend.models.user.user_model import User



@pytest.fixture
def test_customer_data():
    """Provides a standard dictionary of data for creating a Customer."""
    return {
        "id": 1,
        "username": "bbracken",
        "email": "b@example.com",
        "password_hash": "supersecret123",
        "phone": "250-222-2222",
        "address": "1234 University Way",
        "city": "Kelowna",
        "postal_code": "V1V 1V1"
    }

## --- Initialization Tests ---

def test_customer_init(test_customer_data):
    """Test that a Customer object initializes correctly with valid data."""
    customer = Customer(**test_customer_data)
    
    # Check that all attributes are set correctly
    assert customer.id == test_customer_data["id"]
    assert customer.username == test_customer_data["username"]
    assert customer.email == test_customer_data["email"]
    assert customer.password_hash == test_customer_data["password_hash"]
    assert customer.phone == test_customer_data["phone"]
    assert customer.address == test_customer_data["address"]
    assert customer.city == test_customer_data["city"]
    assert customer.postal_code == test_customer_data["postal_code"]
    
    # Check that the cart is initialized (not None)
    assert customer.cart is not None

def test_customer_init_invalid_phone(test_customer_data):
    """Test that initializing a Customer with an invalid phone raises ValueError."""
    test_customer_data["phone"] = ""  # Invalid phone
    with pytest.raises(ValueError, match="phone must be a non-empty string"):
        Customer(**test_customer_data)
    test_customer_data["phone"] = "   "  # Invalid phone (only whitespace)
    with pytest.raises(ValueError, match="phone must be a non-empty string"):
        Customer(**test_customer_data)

def test_customer_init_invalid_address(test_customer_data):
    """Test that initializing a Customer with an invalid address raises ValueError."""
    test_customer_data["address"] = ""  # Invalid address
    with pytest.raises(ValueError, match="address must be a non-empty string"):
        Customer(**test_customer_data)
    test_customer_data["address"] = "   "  # Invalid address (only whitespace)
    with pytest.raises(ValueError, match="address must be a non-empty string"):
        Customer(**test_customer_data)

def test_customer_init_invalid_city(test_customer_data):
    """Test that initializing a Customer with an invalid city raises ValueError."""
    test_customer_data["city"] = ""  # Invalid city
    with pytest.raises(ValueError, match="city must be a non-empty string"):
        Customer(**test_customer_data)
    test_customer_data["city"] = "   "  # Invalid city (only whitespace)
    with pytest.raises(ValueError, match="city must be a non-empty string"):
        Customer(**test_customer_data)

def test_customer_init_invalid_postal_code(test_customer_data):
    """Test that initializing a Customer with an invalid postal code raises ValueError."""
    test_customer_data["postal_code"] = ""  # Invalid postal code
    with pytest.raises(ValueError, match="postal_code must be a non-empty string"):
        Customer(**test_customer_data)
    test_customer_data["postal_code"] = "   "  # Invalid postal code (only whitespace)
    with pytest.raises(ValueError, match="postal_code must be a non-empty string"):
        Customer(**test_customer_data)

## --- Review Tests ---
def test_submit_review():
    # TODO: Implement this with Feat9.
    pass