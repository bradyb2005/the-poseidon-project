import unittest
from backend.models.user.user_model import User
from backend.models.user.customer_model import Customer

class testMenuItem:
    def __init__(self, id, name, description, price):
        self.id = id
        self.name = name
        self.description = description
        self.price = price

class TestCustomerModel(unittest.TestCase):

    def setUp(self):
        # Create a sample customer for testing
        self.customer = Customer(
            id=1,
            username="bbracken",
            password_hash=User.hash_password("verySecretPassword1234"),
            email="brady@example.com",
            phone="250-123-4567",
            address="3272 University Way",
            city="Kelowna",
            postal_code="V1V 1V7"
        )

    def test_initialization(self):
        # One check to ensure inheritance from User is working correctly
        self.assertEqual(self.customer.id, 1)

        # Check Customer-specific attributes
        self.assertEqual(self.customer.email, "brady@example.com")
        self.assertEqual(self.customer.phone, "250-123-4567")
        self.assertEqual(self.customer.address, "3272 University Way")
        self.assertEqual(self.customer.city, "Kelowna")
        self.assertEqual(self.customer.postal_code, "V1V 1V7")
        self.assertEqual(self.customer.cart, {})  # Cart should be initialized as empty

    def test_update_info(self):
        # Test updating a single attribute
        self.customer.update_info(email="brunomars@email.com")
        self.assertEqual(self.customer.email, "brunomars@email.com")
        # Assert that other attributes remain unchanged
        self.assertEqual(self.customer.phone, "250-123-4567")

    def test_add_to_cart_new_item(self):
        # Create a sample menu item that does not already exist in the cart
        menu_item = testMenuItem(id=1, name="Pizza", description="its pizza bro, not that deep", price=10.99)
        # Add the item to the cart with quantity 2
        self.customer.add_to_cart(menu_item, 2)
        self.assertIn(menu_item.id, self.customer.cart)
        self.assertEqual(self.customer.cart[menu_item.id], 2)
    
    def test_add_to_cart_existing_item(self):
        # Create a sample menu item that already exists in the cart
        menu_item = testMenuItem(id=1, name="Pizza", description="its pizza bro, not that deep", price=10.99)
        # Add the item to the cart with quantity 2
        self.customer.add_to_cart(menu_item, 2)
        # Add the same item again with quantity 3
        self.customer.add_to_cart(menu_item, 3)
        self.assertIn(menu_item.id, self.customer.cart)
        self.assertEqual(self.customer.cart[menu_item.id], 5)  # Quantity should be updated to 5
    
    def test_add_to_cart_invalid_quantity(self):
        # Create a sample menu item with invalid quantity
        menu_item = testMenuItem(id=1, name="Pizza", description="its pizza bro, not that deep", price=10.99)
        # Attempt to add the item with an invalid quantity (0 or negative)
        with self.assertRaises(ValueError):
            self.customer.add_to_cart(menu_item, 0)
        with self.assertRaises(ValueError):
            self.customer.add_to_cart(menu_item, -1)