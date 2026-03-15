Test documentation for restaurant service

There is a positive functional test to ensure a restaurant can be published when all information is inputted accurately and correctly.

Corresponding tests have been made to test for missing info error.

Another test has been made to test that an admin can view an unpublished restaurant and a customer cannot

We have a positive functionality test to ensure restaurant owners can create a restaurant.
The edge case ensures customers cannot create restaurants.

Another test ensures that a restaurant can be saved before publishing

One last edge case checks that a restaurant cannot be published without a menu

A collection of tests have been added for nearby search logic to allow to show restaurants near customers.
There are three functional tests including testing filtering by distance, ignoring unpublished restaurants when filtering, and testing the math helper that calculates distance.

There is a few edge cases as well. One that is a boundary tests at exactly 0,0 coordinates. Another that includes a large radius, and one that only shows exact (0) radius.
