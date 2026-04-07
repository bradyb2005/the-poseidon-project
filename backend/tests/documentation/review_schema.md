Review Schema Test documentation

<img width="599" height="127" alt="Screenshot 2026-04-06 at 9 11 39 PM" src="https://github.com/user-attachments/assets/86839e94-6a03-48a2-b138-b309071b0161" />

There are four initialization tests.
- The review create initialization utilizes equivalence partitioning to ensure mandatory review data is mapped correctly
- There are two Rating boundaries for high and low. They use Boundary value analysis and raise validation errors
- The last test is if a review is missing mandatory fields and uses exception handling to ensure the error is passed.

There are two update tests.
- The first is a functional test that ensures that we can update only the comment and only the rating.
- The next tries to update with an invalid rating to ensure a proper error is passed.

There are two serialization and display tests.
- The first is a serealization test that ensure the schema is displayed properly with timestamp and id.
- The next is a functioanl logic test that ensures the alias can be called and everything is done the same.
