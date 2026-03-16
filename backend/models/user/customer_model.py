# Customer Model class

from dataclasses import dataclass
from backend.models.user.user_model import User

class Cart:
    # Placeholder Cart class
    def __init__(self, customer_id: int, customer: "Customer"):
        self.customer_id = customer_id
        self.customer = customer
        self.items = []

@dataclass
class Customer(User):
    phone: str
    address: str
    city: str
    postal_code: str

    """
    Customer Model (based on UML diagram)

    UML Attributes:
      - phone: String
      - address: String
      - city: String
      - postal_code: String

    UML Methods:
      - submit_review(order: Order, rating: int, comment: String) -> Review

    Additional Attributes:
      - cart: Cart (initialized in __post_init__)
    """

    def __post_init__(self) -> None:
        """
        This runs right after the dataclass constructor, which means it runs after we create a Customer object.
        We use it to validate that the Customer object is not invalid.
        """
        super().__post_init__()
        if not isinstance(self.phone, str) or not self.phone.strip():
            raise ValueError("phone must be a non-empty string")
        if not isinstance(self.address, str) or not self.address.strip():
            raise ValueError("address must be a non-empty string")
        if not isinstance(self.city, str) or not self.city.strip():
            raise ValueError("city must be a non-empty string")
        if not isinstance(self.postal_code, str) or not self.postal_code.strip():
            raise ValueError("postal_code must be a non-empty string")
        self.cart = Cart(self.id, self)
        

    def submit_review(self, order: "Order", rating: int, comment: str) -> "Review":
        # Feat9: Submits a review for a completed order
        # TODO: Replace with actual Order implementation once Order class is created
        # TODO: Replace with actual review implementation once Review class is created
        pass