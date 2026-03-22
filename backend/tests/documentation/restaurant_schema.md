Test documentation for restaurant_schema

<img width="688" height="124" alt="Screenshot 2026-03-22 at 2 40 04 PM" src="https://github.com/user-attachments/assets/cf830af0-f8ba-4dad-9f9a-3436514e3581" />

The schema initialization test uses equivalence partitioning and maps the data from the fixture to the schema

the restaurant populate by alias and name test is a functional logic test that tests the populate_by_name accepts both the name and alias identically

The missing mandatory fields test uses exception handling to ensure a validation error is raised when a mandatory field is missing

There are two boundary tests to test for latitude and longitude. It checks for valid and invalid boundaries

Another boundary test tests the boundaries of time for open and close

The model validator test is an edge case for if the open and close time is the same time and a fault injection test to checl if invalid data raises the correct error

There is update tests that are both functional that checks that updating a field doesnt require changing other fields and updating while some elements are none still passes. There is an error there just in case we add more complex validation tests later on

The restaurant serialization test uses mocking to ensure you are able to save through the repository
