import unittest
from backend.models.user.user_model import User
from backend.models.user.customer_model import Customer



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

        # Check two Customer-specific attributes
        self.assertEqual(self.customer.phone, "250-123-4567")
        self.assertEqual(self.customer.cart, {})  # Cart should be initialized as empty

    def test_update_info_valid_change(self):
        # Test updating a single attribute (valid)
        self.customer.update_info(phone="250-765-4321")
        self.assertEqual(self.customer.phone, "250-765-4321")
        # Assert that other attributes remain unchanged
        self.assertEqual(self.customer.city, "Kelowna")
    
    def test_update_info_does_not_exist_change(self):
        # Attempt to update an attribute that does not exist
        self.customer.update_info(non_existent_attr="some value")
        # Assert that the non-existent attribute was not added
        self.assertFalse(hasattr(self.customer, "non_existent_attr"))
            

    def test_add_to_cart_new_item(self):
        # Create a mock menu item that does not already exist in the cart
        menu_item = type('MockMenuItem', (), {
            'id': 1,
            'name': "Pizza",
            'description': "its pizza bro, not that deep",
            'price': 10.99
        })()
        # Add the item to the cart with quantity 2
        self.customer.add_to_cart(menu_item, 2)
        self.assertIn(menu_item.id, self.customer.cart)
        self.assertEqual(self.customer.cart[menu_item.id], 2)
    
    def test_add_to_cart_existing_item(self):
        # Create a sample menu item that already exists in the cart
        menu_item = type('MockMenuItem', (), {
            'id': 1,
            'name': "Pizza",
            'description': "its pizza bro, not that deep",
            'price': 10.99
        })()
        # Add the item to the cart with quantity 2
        self.customer.add_to_cart(menu_item, 2)
        # Add the same item again with quantity 3
        self.customer.add_to_cart(menu_item, 3)
        self.assertIn(menu_item.id, self.customer.cart)
        self.assertEqual(self.customer.cart[menu_item.id], 5)  # Quantity should be updated to 5
    
    def test_add_to_cart_invalid_quantity(self):
        # Create a sample menu item with invalid quantity
        menu_item = type('MockMenuItem', (), {
            'id': 1,
            'name': "Pizza",
            'description': "its pizza bro, not that deep",
            'price': 10.99
        })()
        # Attempt to add the item with an invalid quantity (0 or negative)
        with self.assertRaises(ValueError):
            self.customer.add_to_cart(menu_item, 0)
        with self.assertRaises(ValueError):
            self.customer.add_to_cart(menu_item, -1)
    
    def test_remove_from_cart(self):
        # Create a sample menu item and add it to the cart
        menu_item = type('MockMenuItem', (), {
            'id': 1,
            'name': "Pizza",
            'description': "its pizza bro, not that deep",
            'price': 10.99
        })()
        # Add the item to the cart with quantity 2
        self.customer.add_to_cart(menu_item, 2)
        # Remove the item from the cart
        self.customer.remove_from_cart(menu_item)
        # Assert that the item is no longer in the cart
        self.assertNotIn(menu_item.id, self.customer.cart)

    def test_clear_cart(self):
        # Create sample menu items and add them to the cart
        menu_item1 = type('MockMenuItem', (), {
            'id': 1,
            'name': "Pizza",
            'description': "its pizza bro, not that deep",
            'price': 10.99
        })()
        menu_item2 = type('MockMenuItem', (), {
            'id': 2,
            'name': "Burger",
            'description': "its a burger bro, not that deep",
            'price': 8.99
        })()
        # Add item 1 with quantity 2
        self.customer.add_to_cart(menu_item1, 2)
        # Add item 2 with quantity 3
        self.customer.add_to_cart(menu_item2, 3)
        # Clear the cart
        self.customer.clear_cart()
        # Assert that the cart is now empty
        self.assertEqual(self.customer.cart, {})
    # TODO: Add tests for place_order and submit_review once those methods are implemented