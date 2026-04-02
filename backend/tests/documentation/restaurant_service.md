Resaturant Service Test Documentation

<img width="603" height="146" alt="Screenshot 2026-04-02 at 10 41 57 AM" src="https://github.com/user-attachments/assets/b7e43833-9d9b-4931-8f68-2027d77effa3" />

There are two get by id methods to ensure success and error are both handled correctly. The successful one uses equivalence partitioning to test and returns a successful code in status.
The id not found also uses equivalence partitioning and returns a 404 error when the id is invalid.

There are two get all methods to ensure success and empty list are both handled correctly. The successful one uses Equivalence partitioning and mocking to get all published restaurants with nonsensitive data.
The get all published empty method is a boundary test to ensure an empty list is returned if no restaurants are published.

There are three tests for owner assignment to restaurants. The successful case uses equivalence partitioning and ensures a owner can be assigned to a restaurant.
There is an exception handling test that tries to assign a nonexistent owner to a restaurant.
There is an exceptiopn handling and fault injection test to ensure the proper error is thrown when the database has an error.

There is publishing tests to ensure it can be published successfully,
and an equivalence partitioining test to ensure the pripoer error is thrown if missing required data.

There are two tests for filtering view, one that uses exception handling to ensure a customer cannot view an unpublished restaurant.
Another test ensures customers cannot view sensitive data

There are three tests for boundary handling.
One to test latitude limits, another for longitude limits, and another one to test time limit.

We have a model validator test that tests the edge case to ensure open time cannot equal close time
