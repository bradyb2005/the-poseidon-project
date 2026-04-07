Search routes test documentation

<img width="600" height="123" alt="Screenshot 2026-04-02 at 3 12 42 PM" src="https://github.com/user-attachments/assets/c12654eb-7360-4e00-8d37-085ee48b1ad2" />

For get serch tests, we have a successful test that uses equivalence partitioning and an empty query that uses BVA.

We have location based tests for the getter method. 
First is a successful functional test that ensures nearby restaurants are able to be gotten.
Next we use BVA and error handling to try and get nearby restaurants with invalid parameters.
The third is same as the last, using BVA but for missing parameters

For homepage and feature tests, we have 2.
One test ensures we can get a proper list from the homepage.
Another test ensures we get featured items

For Detail view tests, we have 2.
The first test uses equivalence partitionig to ensure we add all the details successfully.
The next test uses exception handling and ensures the proper error is thrown when a restaurant doesnt exist
