Restaurant Router Test Documentation

<img width="553" height="144" alt="Screenshot 2026-03-25 at 3 33 23 PM" src="https://github.com/user-attachments/assets/99d8755e-0077-4251-97c2-7120980170d6" />

There are three get tests. 
One for restaurants list that uses equivalence partitioning to return test and proper code
The get by id test uses equivalence partitioning to get a single test.
The not found test uses exception handling to get a restaurant that doesnt exist

There are two post tests.
One to assign owner that uses equivalence partitioning to verify owner can be assigned and return proper code.
The publish missing coords test is an integration test an ensures we cannot publish with missing coords.

There is one put test.
This is a validation test for updates to ensure it is done properly
