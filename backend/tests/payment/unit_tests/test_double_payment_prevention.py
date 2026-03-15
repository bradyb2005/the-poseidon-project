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


# Functional Test: Payment should not be processed twice
def test_double_payment_prevention(valid_payment):
    first_attempt = valid_payment.processPayment()
    second_attempt = valid_payment.processPayment()

    assert first_attempt is True
    assert second_attempt is False
    assert valid_payment.status == PaymentStatus.ACCEPTED