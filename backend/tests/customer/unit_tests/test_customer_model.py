# python3 -m pytest backend/tests/customer/unit_tests/test_customer_model.py
import pytest
from unittest.mock import patch
from backend.models.user.customer_model import Customer
from backend.models.cart.cart_model import Cart
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
    
    with patch('backend.models.user.customer_model.Cart') as MockCart:  
        customer = Customer(**test_customer_data)
        
        # Assert Basic Attributes
        assert customer.id == 1
        assert customer.username == "bbracken"
        assert customer.phone == "250-222-2222"
        
        # Assert Mock Behavior
        # Check that Cart was initialized with the right arguments
        MockCart.assert_called_once_with(customer.id, customer)
        # Ensure the customer's cart is actually our mock object
        assert customer.cart == MockCart.return_value

def test_inheritance_check(test_customer_data):
    """Ensure Customer is actually a subclass of User."""
    # We still patch Cart here just to keep the test 'pure' and fast
    with patch('backend.models.user.customer_model.Cart'):
        customer = Customer(**test_customer_data)
        assert isinstance(customer, User)

## --- Behavior Tests ---

def test_submit_review_interface(test_customer_data):
   # TODO: Do with Feat9
   pass