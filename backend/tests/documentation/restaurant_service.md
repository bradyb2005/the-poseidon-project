Resaturant Service Test Documentation

<img width="708" height="129" alt="Screenshot 2026-03-24 at 1 37 48 PM" src="https://github.com/user-attachments/assets/b063a13e-982a-4077-824f-eda6819069a8" />


There are two get by id methods to ensure sucess and error are both handled correctly. The successful one uses equivalence partitioning to test and returns a successful code in status.
The id not found also uses equivalence partitioning and returns a 404 error when the id is invalid.

There are three tests for owner assignment to restaurants. The successful case uses equivalence partitioning and ensures a owner can be assigned to a restaurant.
There is an exception handling test that tries to assign a nonexistent owner to a restaurant.
There is an exceptiopn handling and fault injection test to ensure the proper error is thrown when the database has an error.

There is publishing tests to ensure it can be published successfully,
and an equivalence partitioining test to ensure the pripoer error is thrown if missing required data.

There are two tests for filtering view, one that uses exception handling to ensure a customer cannot view an unpublished restaurant.
Another test ensures customers cannot view sensitive data
