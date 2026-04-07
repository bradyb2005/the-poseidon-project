Search service test documentation

<img width="597" height="133" alt="Screenshot 2026-04-02 at 7 48 28 PM" src="https://github.com/user-attachments/assets/7d932db5-6252-433f-b1ae-c7ab93966c95" />
<img width="603" height="126" alt="Screenshot 2026-04-02 at 3 10 33 PM" src="https://github.com/user-attachments/assets/addd678c-3dea-4ac1-b765-1e4dad8b6e2e" />

We have functional tests to test browsing homepage and ensure it only returns published and another tests to get restaurant details.

We have edge case tests to try to get restaurant details of an unpublished restaurant, get details of a nonexistent restaurant, and tests that homepage does not crash if no restaurants are published.

There is three more home page tests,
One tests to ensure it will filter out unpublished on the home page.
Another test ensures you can successfully get restaurant details from home.
Another test ensures tries to get info of a restaurant that isnt found or hidden.

There are two tests for pagination.
One test tests the boundaries using BVA to ensure the limit of 20 works
The next one is purely functional to ensure total pages are correctly calculated and everything runs smoothly
There is three location based tests.
One test is a functional test that ensures restaurants are sorted correctly
Another test uses equivalence partitioning to filter by unpublished.
The last test is a boundary test that ensures only 10 restaurants are provided
