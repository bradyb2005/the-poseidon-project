item schema test documentation

<img width="602" height="129" alt="Screenshot 2026-04-02 at 10 05 42 AM" src="https://github.com/user-attachments/assets/8f25555e-f5c3-4bef-a7c6-1f6888b81a6b" />

For initialization tests there is equivalence partitioning that ensures data from conftest is correctly mapped to schema
Another test is functional and ensures alias and data name are both accepted.

For UUID logic tests, there is a fault injection test that tests that an invalid uuid string triggers a validation error.

For update schema tests, we have a positive functional test that ensures you can partially update an item.
Another test is a constraint test to ensure an invalid price is valid

For tag tests, there is a data transformation test taht ensures all tags are treated the same and filtered. Another test uses fault injection for invalid tags

For the Serialization test it ensures model_dump works
