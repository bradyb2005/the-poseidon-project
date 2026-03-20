**User Model – Unit Tests**

tests/user/unit_tests/test_user_model.py

*Screenshot attached in the folder*

<img width="716" height="186" alt="Screenshot 2026-03-17 at 5 55 21 PM" src="https://github.com/user-attachments/assets/1408f8f3-1ec4-4937-8cba-1f649644b05f" />


This pull request adds unit tests for the User model.  
The tests verify:

- User creation
- Role validation
- Password hashing (ensuring passwords are not stored in plain text)
- Serialization logic
- Inheritance behavior
- Edge case handling

All tests were executed using:

pytest -q

Result: 12 passed in 7.49 seconds.

Coordinate tests have been added to test that a customer can be created with coordinates, as well as invalid coordinate range and a full loop test.
