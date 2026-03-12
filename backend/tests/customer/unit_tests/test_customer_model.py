import pytest
from unittest.mock import MagicMock
from backend.models.user.customer_model import Customer
from backend.models.cart.cart_model import Cart

@pytest.fixture
def test_customer():
    """Provides a standard set of data for creating a Customer."""
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

def test_customer_init(test_customer):
    # Action
    customer = Customer(**test_customer)
    
    # Assert Inherited Attributes (from User)
    assert customer.id == 1
    assert customer.username == "bbracken"
    assert customer.email == "b@example.com"
    
    # Assert Customer-Specific Attributes
    assert customer.phone == "250-222-2222"
    assert customer.address == "1234 University Way"
    assert customer.postal_code == "V1V 1V1"

    # Assert Automatic Cart Creation
    assert isinstance(customer.cart, Cart)
    assert customer.cart.customer == customer

## --- Behavior Tests ---

def test_submit_review(test_customer):
    # TODO: Implement this for Feat9
    pass

def test_inheritance_check(test_customer):
    """Ensure Customer is actually a subclass of User."""
    from backend.models.user.user_model import User
    customer = Customer(**test_customer)
    assert isinstance(customer, User)