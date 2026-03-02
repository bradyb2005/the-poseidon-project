# Customer Model class

from backend.models.user.user_model import User
from backend.models.restaurant.menu_item_model import MenuItem

class Customer(User):
    # Inherit info from user
    def __init__(self, id: int, username: str, email: str, password_hash: str, 
                 phone: str, address: str, city: str, postal_code: str):
        
        # Send the common attributes to the User constructor
        super().__init__(id, username, email, password_hash)        
        
        self.phone = phone
        self.address = address
        self.city = city
        self.postal_code = postal_code
        self.cart = {}  # Initialize an empty cart for the customer, TODO: Replace with actual Cart class once implemented
        
    def update_info(self, **kwargs):
        # Update customer's personal information
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
    def add_to_cart(self, item: MenuItem, quantity: int) -> None:
        # Adds a menu item to the customer's cart with the specified quantity
        # TODO: Replace with actual cart implementation once Cart class is created
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        if not hasattr(self, "cart"):
            self.cart = {}
        if item.id in self.cart:
            self.cart[item.id] += quantity
        else:
            self.cart[item.id] = quantity

    def remove_from_cart(self, item: MenuItem) -> None:
        # Removes all instances of a menu item from the customer's cart
        if item.id in self.cart:
            del self.cart[item.id]

    def clear_cart(self) -> None:
        # Clears the customer's cart
        self.cart = {}

    def place_order(self) -> "Order":
        # Places an order based on the items in the customer's cart
        # TODO: Replace with actual order implementation once Order class is created
        pass

    def submit_review(self, order: "Order", rating: int, comment: str) -> "Review":
        # Submits a review for a completed order
        # TODO: Replace with actual Order implementation once Order class is created
        # TODO: Replace with actual review implementation once Review class is created
        pass