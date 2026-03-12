Tests for restaurant_model

<img width="517" height="145" alt="Screenshot 2026-03-01 at 11 10 30 PM" src="https://github.com/user-attachments/assets/56e8083a-af56-461a-a012-dbae99dc0494" />


Restaurant Initialization
In the restaurant initialization test, it ensures all core attributes—including open/close times, distance from the user, and the menu—are accurately stored upon the restaurant page's creation. This is verified using a positive functional test to ensure the system meets the primary storage requirements.

Publish Method
For the publish method, we use a positive functional test to verify that a restaurant can transition from a "stored" state to a "published" state. Additionally, a negative edge case test is used to ensure that a restaurant cannot be published if the menu is empty, preventing incomplete information from being shown to customers.

View Perspectives
In the view perspective tests, we verify the Admin and Customer visibility logic. A positive functional test ensures that the "Restaurant" view is always available, while the "Customer" view is only accessible after the restaurant is published. A negative functional test ensures that requesting an invalid or non-existent perspective returns a null value rather than causing a system crash.

Menu Item Core Data
For the menu item test, a positive edge case ensures that the system accurately handles and stores minimum data points for menu items, such as a name and a price of zero, while automatically generating a unique identifier.
