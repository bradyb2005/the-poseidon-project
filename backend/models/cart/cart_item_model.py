from dataclasses import dataclass


@dataclass
class CartItem:
    product_id: int
    name: str
    price: float
    quantity: int = 1

    def __post_init__(self):
        if self.product_id < 0:
            raise ValueError("product_id must be non-negative")

        if self.price < 0:
            raise ValueError("price cannot be negative")

        if self.quantity <= 0:
            raise ValueError("quantity must be > 0")

    def update_quantity(self, qty: int):
        if qty <= 0:
            raise ValueError("quantity must be > 0")
        self.quantity = qty

    def subtotal(self) -> float:
        return self.price * self.quantity