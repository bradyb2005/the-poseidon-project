item schema test documentation

<img width="610" height="131" alt="Screenshot 2026-04-02 at 7 38 35 PM" src="https://github.com/user-attachments/assets/4d14529c-bf20-4857-acd5-d1a3abe5ef07" />


For initialization tests there is equivalence partitioning that ensures data from conftest is correctly mapped to schema
Another test is functional and ensures alias and data name are both accepted.

For UUID logic tests, there is a fault injection test that tests that an invalid uuid string triggers a validation error.

For update schema tests, we have a positive functional test that ensures you can partially update an item.
Another test is a constraint test to ensure an invalid price is valid

For tag tests, there is a data transformation test taht ensures all tags are treated the same and filtered. Another test uses fault injection for invalid tags

For the Serialization test it ensures model_dump works

For pagination tests, we have a functional test that ensures the pagination wrapper works and it can be initialized correctly.
We also have an edge case test that ensures that we can handle an empty test correctly
