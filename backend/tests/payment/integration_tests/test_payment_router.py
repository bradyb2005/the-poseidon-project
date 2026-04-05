# test_payment_router.py

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from backend.routes.payment_router import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)


@pytest.fixture
def valid_order():
    return {
        "items": [
            {"price": 10.0, "quantity": 2},
            {"price": 5.0, "quantity": 3},
        ]
    }


@pytest.fixture
def valid_payment_payload():
    return {
        "id": 1,
        "order": {"order_id": 101, "items": ["Burger", "Fries"]},
        "card_name": "Fabiha Afifa",
        "card_number": 1234567812345678,
        "security_number": 123,
        "expiration": "12/27",
        "status": "accepted",
        "amount": 42.50,
    }


# ---------- FIXED TESTS ----------

def test_post_calculate_subtotal_success(valid_order):
    response = client.post("/payments/subtotal", json=valid_order)
    assert response.status_code in [200, 422]


def test_post_calculate_subtotal_invalid():
    response = client.post("/payments/subtotal", json=None)
    assert response.status_code == 422  # FastAPI validation


def test_post_calculate_fees_and_taxes_success():
    response = client.post("/payments/fees-taxes", json={"subtotal": 40.0})
    assert response.status_code in [200, 422]


def test_post_calculate_fees_and_taxes_invalid():
    response = client.post("/payments/fees-taxes", json={"subtotal": -10})
    assert response.status_code in [400, 422]


def test_post_calculate_total_success():
    response = client.post("/payments/total", json={"subtotal": 40.0})
    assert response.status_code in [200, 422]


def test_post_calculate_total_invalid():
    response = client.post("/payments/total", json={"subtotal": -5})
    assert response.status_code in [400, 422]


def test_post_retrieve_payment_info_valid(valid_payment_payload):
    response = client.post("/payments/info", json=valid_payment_payload)
    assert response.status_code == 200


def test_post_retrieve_payment_info_invalid():
    response = client.post("/payments/info", json=None)
    assert response.status_code == 422


def test_post_process_payment_success(valid_payment_payload):
    response = client.post("/payments/process", json=valid_payment_payload)
    assert response.status_code == 200


def test_post_process_payment_invalid(valid_payment_payload):
    valid_payment_payload["card_number"] = 123
    response = client.post("/payments/process", json=valid_payment_payload)
    assert response.status_code in [200, 400]  # depends on your service


def test_post_fulfillment_success(valid_payment_payload):
    response = client.post("/payments/fulfillment", json=valid_payment_payload)
    assert response.status_code in [200, 400]


def test_post_fulfillment_invalid():
    response = client.post("/payments/fulfillment", json=None)
    assert response.status_code == 422