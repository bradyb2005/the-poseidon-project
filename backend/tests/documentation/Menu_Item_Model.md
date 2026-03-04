Test Documentation for menu item model

<img width="609" height="137" alt="Screenshot 2026-03-03 at 7 30 35 PM" src="https://github.com/user-attachments/assets/aeb7f965-5929-4532-9fa9-0c6706560e96" />

This test runs an initialization test to ensure everything is initialized correctly.
It makes sure all optional fields are none by default

Functional tests:
We have a test for checking type for price and availability to ensure they are taken as a float and boolean

Another test is done for toggling availability of a menu item.

We have one last test that checks that the tags are correctly assigned.

Edge case tests:

We test to ensure default tags are set to an empty list, you cannot insert a negative price, and you can have a free item.
