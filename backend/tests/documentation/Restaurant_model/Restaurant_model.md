Tests for restaurant_model

Initialization
In the restaurant and menu item initialization test, it ensures all core attributes—including open/close times, distance from the user, and the menu—are accurately stored upon the restaurant page's creation. This is verified using a positive functional test to ensure the system meets the primary storage requirements.

Publishing Tests
For publishing, this tests that a restaurant can be published when all files are correctly and accurately inputted. It also ensures that it will not be published if you are missing a key feature, have an invalid data type, or your opening time is after your closing time

Feat3-FR2: Searching
Two edge cases will be added to throw an error if address is passed as an empty string instead of none and another that tests menu item without a restaurant id.
