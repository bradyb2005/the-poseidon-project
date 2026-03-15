import pytest
from unittest.mock import MagicMock
from backend.models.payment.payment_model import Payment, PaymentStatus


@pytest.fixture
def mock_order():
    order = MagicMock()
    order.id = 1
    return order


@pytest.fixture
def valid_payment(mock_order):
    return Payment(
        id=1,
        order=mock_order,
        card_name="John Doe",
        card_number=1234567812345678,
        security_number=123,
        expiration="12/26",
        status=PaymentStatus.DENIED,
        amount=50.0,
    )


# Functional Test: Payment info is retrieved correctly
def test_get_payment_info(valid_payment):
    info = valid_payment.get_payment_info()

    assert info["id"] == 1
    assert info["order_id"] == 1
    assert info["card_name"] == "John Doe"
    assert info["status"] == "denied"
    assert info["amount"] == 50.0
    assert info["expiration"] == "12/26"


# Functional Test: Valid payment is processed successfully
def test_process_payment_success(valid_payment):
    result = valid_payment.processPayment()

    assert result is True
    assert valid_payment.status == PaymentStatus.ACCEPTED


# Functional Test: Fulfillment request succeeds for accepted payment
def test_request_fulfillment_success(valid_payment):
    valid_payment.processPayment()

    assert valid_payment.request_fulfillment() is True


# Functional Test: Fulfillment request fails for denied payment
def test_request_fulfillment_denied(mock_order):
    payment = Payment(
        id=2,
        order=mock_order,
        card_name="John Doe",
        card_number=0,
        security_number=123,
        expiration="12/26",
        status=PaymentStatus.DENIED,
        amount=50.0,
    )

    assert payment.request_fulfillment() is False