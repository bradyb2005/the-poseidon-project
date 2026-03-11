Tests for restaurant_model

<img width="561" height="135" alt="Screenshot 2026-03-11 at 2 41 19 PM" src="https://github.com/user-attachments/assets/86c641f5-bd9e-4848-91c3-7fae0f63c668" />


Restaurant Initialization
In the restaurant initialization test, it ensures all core attributes—including open/close times, distance from the user, and the menu—are accurately stored upon the restaurant page's creation. This is verified using a positive functional test to ensure the system meets the primary storage requirements.

Publish Method
For the publish method, we use a positive functional test to verify that a restaurant can transition from a "stored" state to a "published" state. Additionally, a negative edge case test is used to ensure that a restaurant cannot be published if the menu is empty, preventing incomplete information from being shown to customers.

View Perspectives
In the view perspective tests, we verify the Admin and Customer visibility logic. A positive functional test ensures that the "Restaurant" view is always available, while the "Customer" view is only accessible after the restaurant is published. A negative functional test ensures that requesting an invalid or non-existent perspective returns a null value rather than causing a system crash.

Menu Item Core Data
For the menu item test, a positive edge case ensures that the system accurately handles and stores minimum data points for menu items, such as a name and a price of zero, while automatically generating a unique identifier.

Publishing Tests
For publishing, this tests that a restaurant can be published when all files are correctly and accurately inputted. It also ensures that it will not be published if you are missing a key feature, have an invalid data type, or your opening time is after your closing time
