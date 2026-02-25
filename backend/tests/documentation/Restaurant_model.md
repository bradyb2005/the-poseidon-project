Tests for restaurant_model

<img width="949" height="119" alt="Screenshot 2026-02-23 at 10 48 59 AM" src="https://github.com/user-attachments/assets/abfb01e0-68e6-46d0-8d77-ba66e17f9ca3" />

In the restaurant initialization test, it ensures all attributes are accurately initialized.
This is done using a positive functional test.

In Average rating, it tests three edge cases and one positive functional test.
The positive test ensures average rating is calculated properly.
The edge cases check for no reviews, and rounding up and down to the closest decimal.

For Update attributes, we test updating attributes as a functional test as well as ensuring an empty string is returned instead of None.
