import pytest
from unittest.mock import MagicMock

from backend.models.payment.payment_model import Payment, PaymentStatus


@pytest.fixture
def mock_order():
    order = MagicMock()
    order.id = 1
    return order


def test_validate_success(mock_order):
    payment = Payment(
        id=1,
        order=mock_order,
        card_name="John Doe",
        card_number=1234567812345678,
        security_number=123,
        expiration="12/28",
        status=PaymentStatus.ACCEPTED,
        amount=50.0,
    )

    assert payment.validate() is True


def test_validate_empty_card_name(mock_order):
    payment = Payment(
        id=1,
        order=mock_order,
        card_name="",
        card_number=1234567812345678,
        security_number=123,
        expiration="12/28",
        status=PaymentStatus.DENIED,
        amount=50.0,
    )

    assert payment.validate() is False


def test_validate_invalid_card_number(mock_order):
    payment = Payment(
        id=1,
        order=mock_order,
        card_name="John Doe",
        card_number=0,
        security_number=123,
        expiration="12/28",
        status=PaymentStatus.DENIED,
        amount=50.0,
    )

    assert payment.validate() is False


def test_validate_invalid_security_number(mock_order):
    payment = Payment(
        id=1,
        order=mock_order,
        card_name="John Doe",
        card_number=1234567812345678,
        security_number=0,
        expiration="12/28",
        status=PaymentStatus.DENIED,
        amount=50.0,
    )

    assert payment.validate() is False


def test_validate_empty_expiration(mock_order):
    payment = Payment(
        id=1,
        order=mock_order,
        card_name="John Doe",
        card_number=1234567812345678,
        security_number=123,
        expiration="",
        status=PaymentStatus.DENIED,
        amount=50.0,
    )

    assert payment.validate() is False


def test_validate_negative_amount(mock_order):
    payment = Payment(
        id=1,
        order=mock_order,
        card_name="John Doe",
        card_number=1234567812345678,
        security_number=123,
        expiration="12/28",
        status=PaymentStatus.DENIED,
        amount=-10.0,
    )

    assert payment.validate() is False