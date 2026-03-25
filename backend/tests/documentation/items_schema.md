item schema test documentation
<img width="707" height="136" alt="Screenshot 2026-03-24 at 7 15 15 PM" src="https://github.com/user-attachments/assets/eae7cb3f-3e03-4d20-8cf1-808577f1ec93" />

For initialization tests there is equivalence partitioning that ensures data from conftest is correctly mapped to schema
Another test is functional and ensures alias and data name are both accepted.

For validation and boundary tests, There is a missing mandatory field using exception handling. It ensures a ValidationError is raised.
Another test tests negative price through boundary value analysis to ensure the price validator prevents negative values
Another test is for empty name and uses fault injection to test that names cannot be empty strings or whitespaces

For UUID logic tests, there is a fault injection test that tests that an invalid uuid string triggers a validation error.

For update schema tests, we have a positive functional test that ensures you can partially update an item.
Another test is a constraint test to ensure an invalid price is valid

For the Serialization test it ensures model_dump works
