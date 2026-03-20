Tests for customer model
<img width="303" height="82" alt="Screenshot 2026-03-17 at 5 53 54 PM" src="https://github.com/user-attachments/assets/28fbc58f-e31e-468b-8195-5544a3b620ed" />


There is an initialization test that ensures customer attributes are set up and passed right

Another functional test is to ensure coordinates default to 0,0

The third is a functional test to set up bounds for the latitude and longitude. This is like 90 and -90

We have two edge cases for exact boarder boundaries to ensure they pass

Another edge case tests to ensure string coordinates do not pass.

Another is an edge case for a customer with no address
