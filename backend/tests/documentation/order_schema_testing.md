Test documentation for order schema

![1774237908442](image/order_schema_testing/1774237908442.png)

This new test file thoroughly validates the Pydantic schemas used for creating and updating orders (`OrderCreate`, `OrderUpdate`, `OrderItemCreate`, `OrderItemUpdate`).

It utilizes Boundary Value Testing to ensure geographic coordinates (latitude and longitude) strictly fall within valid global ranges. 
Additionally, it uses Equivalence Class Partitioning via `pytest.mark.parametrize` to test the Canadian postal code with regex, ensuring it accepts valid formats while properly rejecting various invalid cases (e.g., wrong format, bad separators, incorrect lengths). 
Finally, it verifies that the OrderUpdate schema correctly enforces these same validation rules on optional fields.