# backend/tests/payment/unit_tests/test_payment_service.py
import pytest
from pydantic import ValidationError


from backend.schemas.payment_schema import (
    CostBreakdown,
    PaymentSchema,
    PaymentStatus,
    UpdatePaymentSchema,
)
from backend.services.payment_service import PaymentService

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


def test_calculate_subtotal_valid():
    service = PaymentService()
    order = {
        "items": [
            {"price_at_time": 10.0, "quantity": 2},
            {"price_at_time": 5.0, "quantity": 3},
        ]
    }


    subtotal = service.calculate_subtotal(order)
   
    assert subtotal == 35.0


def test_calculate_subtotal_invalid_quantity():
    service = PaymentService()
    order = {
        "items": [
            {"price_at_time": 10.0, "quantity": 0}
        ]
    }

    with pytest.raises(ValueError):
        service.calculate_subtotal(order)




def test_calculate_subtotal_negative_price():
    service = PaymentService()
    order = {
        "items": [
            {"price_at_time": -5.0, "quantity": 2},
        ]
    }
    with pytest.raises(ValueError):
        service.calculate_subtotal(order)




def test_calculate_fees_and_taxes_valid():
    service = PaymentService()


    subtotal = 40.0
    result = service.calculate_fees_and_taxes(subtotal)


    assert result["delivery_fee"] == 5.00
    assert result["service_fee"] == 2.00
    assert result["tax"] == 4.80




def test_calculate_fees_and_taxes_free_delivery():
    service = PaymentService()


    subtotal = 60.0
    result = service.calculate_fees_and_taxes(subtotal)


    assert result["delivery_fee"] == 0.00




def test_calculate_fees_and_taxes_invalid_subtotal():
    service = PaymentService()


    with pytest.raises(ValueError):
        service.calculate_fees_and_taxes(-10)




def test_calculate_total_valid():
    service = PaymentService()


    subtotal = 40.0
    breakdown = service.calculate_total(subtotal)


    assert breakdown.subtotal == 40.0
    assert breakdown.delivery_fee == 5.00
    assert breakdown.service_fee == 2.00
    assert breakdown.tax == 4.80
    assert breakdown.total == 51.80


def test_calculate_total_free_delivery():
    service = PaymentService()


    subtotal = 60.0
    breakdown = service.calculate_total(subtotal)


    assert breakdown.delivery_fee == 0.00




def test_calculate_total_invalid_subtotal():
    service = PaymentService()


    with pytest.raises(ValueError):
        service.calculate_total(-10)


def test_retrieve_payment_info_valid(base_payment_data):
    service = PaymentService()
    payment = PaymentSchema(**base_payment_data)


    result = service.retrieve_payment_info(payment)
    assert result["id"] == 1
    assert result["order"]["order_id"] == 101
    assert result["card_name"] == "Fabiha Afifa"
    assert result["card_number"] == 1234567812345678
    assert result["expiration"] == "12/27"
    assert result["status"] == PaymentStatus.ACCEPTED
    assert result["amount"] == 42.50




def test_retrieve_payment_info_none():
    service = PaymentService()
    with pytest.raises(ValueError):
        service.retrieve_payment_info(None)


def test_process_payment_success(base_payment_data):
    service = PaymentService()
    payment = PaymentSchema(**base_payment_data)


    result = service.process_payment(payment)


    assert result.status == PaymentStatus.ACCEPTED




def test_process_payment_failure(base_payment_data):
    service = PaymentService()


    base_payment_data["card_number"] = 123  # invalid short number
    payment = PaymentSchema(**base_payment_data)


    result = service.process_payment(payment)


    assert result.status == PaymentStatus.DENIED




def test_process_payment_none():
    service = PaymentService()


    with pytest.raises(ValueError):
        service.process_payment(None)

def test_create_fulfillment_request_success(base_payment_data):
    service = PaymentService()
    payment = PaymentSchema(**base_payment_data)
    payment.status = PaymentStatus.ACCEPTED

    result = service.create_fulfillment_request(payment)

    assert result["payment_id"] == 1
    assert result["order"]["order_id"] == 101
    assert result["status"] == "fulfillment_requested"


def test_create_fulfillment_request_denied_payment(base_payment_data):
    service = PaymentService()
    payment = PaymentSchema(**base_payment_data)
    payment.status = PaymentStatus.DENIED

    with pytest.raises(ValueError):
        service.create_fulfillment_request(payment)


def test_create_fulfillment_request_none():
    service = PaymentService()

    with pytest.raises(ValueError):
        service.create_fulfillment_request(None)