item schema test documentation
<img width="632" height="131" alt="Screenshot 2026-03-25 at 8 20 27 PM" src="https://github.com/user-attachments/assets/8771d507-db91-4f2f-9f78-8f910cbe7707" />

For initialization tests there is equivalence partitioning that ensures data from conftest is correctly mapped to schema
Another test is functional and ensures alias and data name are both accepted.

For validation and boundary tests, There is a missing mandatory field using exception handling. It ensures a ValidationError is raised.
Another test tests negative price through boundary value analysis to ensure the price validator prevents negative values
Another test is for empty name and uses fault injection to test that names cannot be empty strings or whitespaces

For UUID logic tests, there is a fault injection test that tests that an invalid uuid string triggers a validation error.

For update schema tests, we have a positive functional test that ensures you can partially update an item.
Another test is a constraint test to ensure an invalid price is valid

For tag tests, there is a data transformation test taht ensures all tags are treated the same and filtered. Another test uses fault injection for invalid tags

For the Serialization test it ensures model_dump works
