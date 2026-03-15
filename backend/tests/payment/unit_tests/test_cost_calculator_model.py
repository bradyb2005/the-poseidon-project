import pytest
from unittest.mock import MagicMock

from backend.models.payment.cost_calculator_model import (
    CostBreakdown,
    CostCalculator,
)


@pytest.fixture
def mock_order():
    item1 = MagicMock()
    item1.price = 10.0
    item1.quantity = 2

    item2 = MagicMock()
    item2.price = 5.0
    item2.quantity = 3

    order = MagicMock()
    order.items = [item1, item2]
    return order


@pytest.fixture
def calculator():
    return CostCalculator()


def test_calculate_subtotal(calculator, mock_order):
    subtotal = calculator.calculateSubtotal(mock_order)
    assert subtotal == 35.0


def test_calculate_tax(calculator, mock_order):
    tax = calculator.calculateTax(mock_order)
    assert tax == 35.0 * 0.12


def test_calculate_delivery_fee(calculator, mock_order):
    delivery_fee = calculator.calculateDeliveryFee(mock_order)
    assert delivery_fee == 5.0


def test_calculate_service_fee(calculator, mock_order):
    service_fee = calculator.calculateServiceFee(mock_order)
    assert service_fee == 35.0 * 0.05


def test_calculate_total(calculator, mock_order):
    total = calculator.calculateTotal(mock_order)
    expected_total = 35.0 + (35.0 * 0.12) + 5.0 + (35.0 * 0.05)

    assert total == expected_total


def test_get_breakdown(calculator, mock_order):
    breakdown = calculator.getBreakdown(mock_order)

    assert isinstance(breakdown, CostBreakdown)
    assert breakdown.subtotal == 35.0
    assert breakdown.tax == 35.0 * 0.12
    assert breakdown.deliveryFee == 5.0
    assert breakdown.serviceFee == 35.0 * 0.05
    assert breakdown.total == 35.0 + (35.0 * 0.12) + 5.0 + (35.0 * 0.05)