Item service test documentation

<img width="575" height="132" alt="Screenshot 2026-04-06 at 5 28 13 PM" src="https://github.com/user-attachments/assets/5d20e304-eceb-4949-b37b-29e06efbd6a3" />


There is two ownership tests.
They both use exception handling, one for if they don't have owner_id and another if they are not authorized to own a restaurant.

There are three add menu item tests.
The successful test is functional and ensures a valid item can be added.
Another test ensures decimal can be reused properly
The invalid price test uses equivalence partitioning and fault injection to ensure an error is thrown when there's a negative price.

There is one edit menu item test
This is a successful test to ensure you can edit the item properly.

There is two availability toggle tests.
The not found uses equivalence partitioning to ensure proper error is thrown when item is made.
The positive test ensures it can be toggled properly

There is one remove menu item test.
This ensures you can properly remove a menu item.

There is four validation and boundary tests
A Boundary test tests negative price using boundary value analysis
Another test uses fault injection to ensure that the name cannot be empty strings or whitespace
Another test uses fault injection  to ensures names cannot be anything other than strings.
A UUID test is for validation to ensure that bad UUIDs are caught and return 400 code
Another test tests for tag standardization and ensures all tags are treated the same regardless of case and duplicates.
