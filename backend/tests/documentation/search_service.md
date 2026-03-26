Search service test documentation

<img width="691" height="128" alt="Screenshot 2026-03-25 at 9 11 41 PM" src="https://github.com/user-attachments/assets/94b8d578-e9d8-4457-bbc0-a2ab13855e64" />

We have functional tests to test browsing homepage and ensure it only returns published and another tests to get restaurant details.

We have edge case tests to try to get restaurant details of an unpublished restaurant, get details of a nonexistent restaurant, and tests that homepage does not crash if no restaurants are published.

There is three more home page tests,
One tests to ensure it will filter out unpublished on the home page.
Another test ensures you can successfully get restaurant details from home.
Another test ensures tries to get info of a restaurant that isnt found or hidden.
