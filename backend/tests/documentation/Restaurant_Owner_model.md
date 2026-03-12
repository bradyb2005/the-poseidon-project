Restaurant_Owner Model test file

<img width="899" height="142" alt="Screenshot 2026-03-11 at 2 48 03 PM" src="https://github.com/user-attachments/assets/4e4d4f56-9918-4361-a11d-f1e10e2c23a9" />


This file tests all required methods and functionality of restaurent_owner_model.
It communicates with the user model and the menu_item model for tasks.

The tests for creaing a restaurant include positively testing that a restaurent can be made and testing if a restaurant can be made without a name.

In updating restaurant information this tests updating a random restaurant attributes and updating one attribute whem multiple are present.

In adding and removing menu items we simply test that adding and removing menu items is possible and running predictibly.

In updating menu items we have two positive functional tests and one edge case. 
The positive tests ensure we can update a menu item to a different real number or to zero for a free item. 
The edge case tests to ensure that negative prices will not be accepted.

In set item availability it allows restaurant owners to toggle on off items based on availability.

In test open closed it allows for restaurant owners to advertise weather or not they are open based on their store hours.
The edge case test ensures no value besides a boolean will be accepted for this test.

In test restaurant operating hours this test owners ability to update their store hours. They can decicde to update both the time they open and the time they close or just one.

In test owner prepares restaurant for publishing, owner is able to fill out all fields and validate for publishing and throws error if data is not filled in correctly

All tests pass with no errors.
