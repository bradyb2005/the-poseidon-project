Review Repository Test Documentation

<img width="596" height="128" alt="Screenshot 2026-04-06 at 10 17 05 PM" src="https://github.com/user-attachments/assets/cb5c83c0-e25f-46ca-b79e-28b9cd184ad4" />

There are 2 initialization tests
- One that ensures all repo defaults to the correct directory structure.
- One test uses equivalence partitioning to create a directory if it is missing

There are 4 Save/ Load tests
- There is a functional test that ensures you can save all properly without issue
- A similar test is done for load all to ensure everything is done correctly
- The load all empty file test utilizes equivalence partitioning to return an empty file if it does not exist
- The load all invalid json uses Equivalence partitioning to ensure load_all handles corrupted JSON gracefully

There is 1 Serialization tests
- This test ensures that data integrity remains after a save and load. Ensures it is handled correctly.
