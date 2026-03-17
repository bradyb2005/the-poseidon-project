import sys
import types
import pytest

mock_cost_calculator_module = types.ModuleType("backend.models.payment.cost_calculator_model")
mock_payment_model_module = types.ModuleType("backend.models.payment.payment_model")


class MockCostCalculator:
    def calculateTotal(self, order):
        return 42.50

    def getBreakdown(self, order):
        return {
            "subtotal": 20.00,
            "tax": 2.40,
            "fees": 1.60,
            "total": 24.00,
        }


class MockPaymentStatus:
    DENIED = types.SimpleNamespace(value="denied")


class MockPayment:
    def __init__(
        self,
        id,
        order,
        card_name,
        card_number,
        security_number,
        expiration,
        status,
        amount,
    ):
        self.id = id
        self.order = order
        self.card_name = card_name
        self.card_number = card_number
        self.security_number = security_number
        self.expiration = expiration
        self.status = status
        self.amount = amount

    def validate(self):
        return True

    def processPayment(self):
        self.status = types.SimpleNamespace(value="accepted")
        return True

    def get_payment_info(self):
        return {
            "card_name": self.card_name,
            "amount": self.amount,
            "status": self.status.value,
        }

    def request_fulfillment(self):
        return True


mock_cost_calculator_module.CostCalculator = MockCostCalculator
mock_payment_model_module.Payment = MockPayment
mock_payment_model_module.PaymentStatus = MockPaymentStatus

sys.modules["backend.models.payment.cost_calculator_model"] = mock_cost_calculator_module
sys.modules["backend.models.payment.payment_model"] = mock_payment_model_module


from backend.services.payment_service import PaymentService


class MockOrder:
    def __init__(self, order_id=1):
        self.id = order_id


@pytest.fixture
def payment_service():
    return PaymentService()


@pytest.fixture
def order():
    return MockOrder()


# --- FR1: Retrieving Information ---

def test_create_payment_success(payment_service, order):
    # Positive Functional Test: Payment object is created successfully
    data = {
        "card_name": "John Doe",
        "card_number": 1234567812345678,
        "security_number": 123,
        "expiration": "12/28",
    }

    result = payment_service.create_payment(order, data)

    assert result["success"] is True
    assert result["payment"].card_name == "John Doe"
    assert result["payment"].amount == 42.50
    assert result["payment"].status.value == "denied"


def test_create_payment_defaults(payment_service, order):
    # Edge Test: Missing fields fall back to defaults
    result = payment_service.create_payment(order, {})

    assert result["success"] is True
    assert result["payment"].card_name == ""
    assert result["payment"].card_number == 0
    assert result["payment"].security_number == 0
    assert result["payment"].expiration == ""


def test_get_payment_info_success(payment_service, order):
    # Positive Functional Test: Payment info can be retrieved
    payment = MockPayment(
        id=1,
        order=order,
        card_name="Jane Doe",
        card_number=1111222233334444,
        security_number=321,
        expiration="10/27",
        status=types.SimpleNamespace(value="denied"),
        amount=25.00,
    )

    result = payment_service.get_payment_info(payment)

    assert result["success"] is True
    assert result["payment_info"]["card_name"] == "Jane Doe"
    assert result["payment_info"]["amount"] == 25.00


def test_get_payment_info_failure(payment_service):
    # Edge Test: Return error if payment info retrieval fails
    class BrokenPayment:
        def get_payment_info(self):
            raise Exception("Could not retrieve payment info")

    result = payment_service.get_payment_info(BrokenPayment())

    assert result["success"] is False
    assert "Could not retrieve payment info" in result["error"]


# --- FR2: Complete data types ---

def test_validate_payment_success(payment_service, order):
    # Positive Functional Test: Valid payment passes validation
    payment = MockPayment(
        id=1,
        order=order,
        card_name="John Doe",
        card_number=1234,
        security_number=123,
        expiration="12/28",
        status=types.SimpleNamespace(value="denied"),
        amount=42.50,
    )

    result = payment_service.validate_payment(payment)

    assert result["success"] is True


def test_validate_payment_failure(payment_service):
    # Negative Edge Test: Invalid payment fails validation
    class InvalidPayment:
        def validate(self):
            return False

    result = payment_service.validate_payment(InvalidPayment())

    assert result["success"] is False
    assert "Invalid payment information" in result["error"]


# --- FR3: Integrated payment gateway ---

def test_process_payment_success(payment_service, order):
    # Positive Functional Test: Payment is processed successfully
    payment = MockPayment(
        id=1,
        order=order,
        card_name="John Doe",
        card_number=1234,
        security_number=123,
        expiration="12/28",
        status=types.SimpleNamespace(value="denied"),
        amount=42.50,
    )

    result = payment_service.process_payment(payment)

    assert result["success"] is True
    assert result["status"] == "accepted"


def test_process_payment_failure(payment_service):
    # Negative Edge Test: Payment is denied
    class DeniedPayment:
        def processPayment(self):
            return False

    result = payment_service.process_payment(DeniedPayment())

    assert result["success"] is False
    assert "Payment was denied" in result["error"]


# --- FR4: Fulfillment request ---

def test_request_fulfillment_success(payment_service, order):
    # Positive Functional Test: Fulfillment request succeeds
    payment = MockPayment(
        id=1,
        order=order,
        card_name="John Doe",
        card_number=1234,
        security_number=123,
        expiration="12/28",
        status=types.SimpleNamespace(value="accepted"),
        amount=42.50,
    )

    result = payment_service.request_fulfillment(payment)

    assert result["success"] is True


def test_request_fulfillment_failure(payment_service):
    # Negative Edge Test: Fulfillment fails if payment not accepted
    class UnfulfillablePayment:
        def request_fulfillment(self):
            return False

    result = payment_service.request_fulfillment(UnfulfillablePayment())

    assert result["success"] is False
    assert "Payment not accepted" in result["error"]


# --- Cost breakdown ---

def test_get_cost_breakdown_success(payment_service, order):
    # Positive Functional Test: Cost breakdown is returned correctly
    result = payment_service.get_cost_breakdown(order)

    assert result["success"] is True
    assert result["breakdown"]["subtotal"] == 20.00
    assert result["breakdown"]["tax"] == 2.40
    assert result["breakdown"]["fees"] == 1.60
    assert result["breakdown"]["total"] == 24.00