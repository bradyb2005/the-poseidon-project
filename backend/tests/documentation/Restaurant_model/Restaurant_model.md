Tests for restaurant_model

Initialization
In the restaurant and menu item initialization test, it ensures all core attributes—including open/close times, distance from the user, and the menu—are accurately stored upon the restaurant page's creation. This is verified using a positive functional test to ensure the system meets the primary storage requirements.

Publishing Tests
For publishing, this tests that a restaurant can be published when all files are correctly and accurately inputted. It also ensures that it will not be published if you are missing a key feature, have an invalid data type, or your opening time is after your closing time

Reviews
We have functional tests to update the average rating, to ensure customer view includes reviewes and menu, and can view the full menu

We have edge case tests for Average rating with no reviews equalling zero, a test for rounding, out of bounds rating, and ensures customers cannot browse menus or reviews that are not published as well as calculations with minimum valid ratings
