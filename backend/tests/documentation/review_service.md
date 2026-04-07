Review service Test documentation

<img width="654" height="129" alt="Screenshot 2026-04-07 at 10 28 35 AM" src="https://github.com/user-attachments/assets/1edcd8fc-5e9b-428b-97fb-8109c4984658" />

There are four review submission tests
- The successful test uses equivalence partitioning to ensure a review can be submitted when an order is complete
- The next test uses exception handling and tries to submit a review for a non existent order
- The next test is a functional test that tries to review before an order is complete
- The next test uses equivalence partitioning to ensure only one review can be submitted per order

There are two edit review tests
- There is a successful review test that ensures you can edit within thirty minutes of review
- There is a boundary value analysis test that ensures no editing shall be done after thirty minutes

There are two Average rating tests
- The first is a functional test that ensures average rating is calculated correctly.
- The next uses boundary value analysis that tries to get average from a restaurant with no reviews.

There is one deletion test
- There is a successful test that uses equivalence partitioning to ensure a review can be deleted
