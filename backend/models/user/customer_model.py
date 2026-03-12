# Customer Model class

from backend.models.user.user_model import User
from backend.models.cart.cart_model import Cart

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
        self.cart = Cart(id, self)
        

    def submit_review(self, order: "Order", rating: int, comment: str) -> "Review":
        # Feat9: Submits a review for a completed order
        # TODO: Replace with actual Order implementation once Order class is created
        # TODO: Replace with actual review implementation once Review class is created
        pass