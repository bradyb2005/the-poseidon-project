from backend.models.payment.cost_calculator_model import CostCalculator
from backend.models.payment.payment_model import Payment, PaymentStatus


class PaymentService:
    def __init__(self) -> None:
        self.cost_calculator = CostCalculator()

    def create_payment(self, order, data: dict):
        """
        FR1: Retrieving Information
        Creates a payment object for an order.
        """
        try:
            amount = self.cost_calculator.calculateTotal(order)

            payment = Payment(
                id=0,
                order=order,
                card_name=data.get("card_name", ""),
                card_number=data.get("card_number", 0),
                security_number=data.get("security_number", 0),
                expiration=data.get("expiration", ""),
                status=PaymentStatus.DENIED,
                amount=amount,
            )

            return {"success": True, "payment": payment}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def validate_payment(self, payment: Payment):
        """
        FR2: Complete data types
        Validates payment information.
        """
        if payment.validate():
            return {"success": True}
        return {"success": False, "error": "Invalid payment information"}

    def process_payment(self, payment: Payment):
        """
        FR3: Integrated payment gateway
        Processes the payment.
        """
        result = payment.processPayment()

        if result:
            return {"success": True, "status": payment.status.value}

        return {"success": False, "error": "Payment was denied"}

    def get_payment_info(self, payment: Payment):
        """
        FR1: Retrieving Information
        """
        try:
            info = payment.get_payment_info()
            return {"success": True, "payment_info": info}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def request_fulfillment(self, payment: Payment):
        """
        FR4: Fulfillment request
        """
        if payment.request_fulfillment():
            return {"success": True}

        return {"success": False, "error": "Payment not accepted"}

    def get_cost_breakdown(self, order):
        """
        Returns subtotal, tax, fees, and total for an order.
        """
        try:
            breakdown = self.cost_calculator.getBreakdown(order)
            return {"success": True, "breakdown": breakdown}

        except Exception as e:
            return {"success": False, "error": str(e)}
