Item service test documentation

<img width="631" height="125" alt="Screenshot 2026-03-25 at 6 42 44 PM" src="https://github.com/user-attachments/assets/2be3e16b-325f-4400-add4-3e0eeee584aa" />

There is two ownership tests.
They both use exception handling, one for if they don't have owner_id and another if they are not authorized to own a restaurant.

There are two add menu item tests.
The successful test is functional and ensures a valid item can be added.
The invalid price test uses equivalence partitioning and fault injection to ensure an error is thrown when there's a negative price.

There is one edit menu item test
This is a successful test to ensure you can edit the item properly.

There is two availability toggle tests.
The not found uses equivalence partitioning to ensure proper error is thrown when item is made.
The positive test ensures it can be toggled properly

There is one remove menu item test.
This ensures you can properly remove a menu item.
