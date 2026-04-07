Item router test documentation

<img width="706" height="130" alt="Screenshot 2026-04-06 at 5 57 17 PM" src="https://github.com/user-attachments/assets/ee210f7d-8d08-4aa3-88ac-e2eb629c4e56" />

For POST tests, there are 2 tests
A successful equivalence partitioning test ensures a valid menu item can be added to a restaurant
The unauthourized test uses exception handling to ensure a 403 is returned if the user doesnt own the restaurant

For PUT tests, there is one test
A successful equivalence partitioning test ensures you can edit menu items

For DELETE tests, there are 2 tests
The first one uses equivalence partitioning to properly delete a menu item.
another test uses exception handling to return an error if the item is not found
