Test documentation for restaurant_schema

<img width="607" height="127" alt="Screenshot 2026-04-02 at 10 27 29 AM" src="https://github.com/user-attachments/assets/feaf38b8-63e1-46cc-89ab-bfb47f73fa18" />

The schema initialization test uses equivalence partitioning and maps the data from the fixture to the schema

the restaurant populate by alias and name test is a functional logic test that tests the populate_by_name accepts both the name and alias identically

The missing mandatory fields test uses exception handling to ensure a validation error is raised when a mandatory field is missing

There is update tests that are both functional that checks that updating a field doesnt require changing other fields and updating while some elements are none still passes. There is an error there just in case we add more complex validation tests later on

The restaurant serialization test uses mocking to ensure you are able to save through the repository
