import pytest
from pydantic import ValidationError

from backend.models.payment.payment_schema import (
    CostBreakdown,
    PaymentSchema,
    PaymentStatus,
    UpdatePaymentSchema,
)


@pytest.fixture
def base_payment_data():
    return {
        "id": 1,
        "order": {"order_id": 101, "items": ["Burger", "Fries"]},
        "card_name": "Fabiha Afifa",
        "card_number": 1234567812345678,
        "security_number": 123,
        "expiration": "12/27",
        "status": PaymentStatus.ACCEPTED,
        "amount": 42.50,
    }


@pytest.fixture
def valid_cost_breakdown_data():
    return {
        "subtotal": 30.00,
        "delivery_fee": 5.00,
        "service_fee": 2.00,
        "tax": 3.60,
        "total": 40.60,
    }


def test_payment_schema_initialization(base_payment_data):
    payment = PaymentSchema(**base_payment_data)

    assert payment.id == 1
    assert payment.order["order_id"] == 101
    assert payment.card_name == "Fabiha Afifa"
    assert payment.card_number == 1234567812345678
    assert payment.security_number == 123
    assert payment.expiration == "12/27"
    assert payment.status == PaymentStatus.ACCEPTED
    assert payment.amount == 42.50


def test_payment_missing_required_fields():
    with pytest.raises(ValidationError):
        PaymentSchema(id=1)


def test_payment_amount_cannot_be_negative(base_payment_data):
    base_payment_data["amount"] = -1.00

    with pytest.raises(ValidationError):
        PaymentSchema(**base_payment_data)


def test_update_payment_schema_partial_update():
    update_data = {"status": PaymentStatus.ACCEPTED}
    update_obj = UpdatePaymentSchema(**update_data)

    assert update_obj.status == PaymentStatus.ACCEPTED
    assert update_obj.card_name is None


def test_cost_breakdown_initialization(valid_cost_breakdown_data):
    breakdown = CostBreakdown(**valid_cost_breakdown_data)

    assert breakdown.total == 40.60


def test_cost_breakdown_invalid_total(valid_cost_breakdown_data):
    valid_cost_breakdown_data["total"] = 100.00

    with pytest.raises(ValidationError):
        CostBreakdown(**valid_cost_breakdown_data)