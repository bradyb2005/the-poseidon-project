Restaurant Repository Tests

<img width="659" height="126" alt="Restaurant_repo" src="https://github.com/user-attachments/assets/7940efd8-2167-4045-9f4c-7b17434e8b7f" />

Creating a restaurant (Feat2-FR1)
Functional test ensures a restaurant can be made and data passed in repo

Information Management (Feat2-FR3)
The Update test ensures that existing records can be modified accurately.
It proves that you can change a specific field without accidentally overwriting or deleting other existing fields.

Menu Retrieval (Feat3-FR3)
The Get by ID test validates the logic for opening specific restaurant menus.
It checks the positive functional path and the edge case which prevents the application from crashing when a user requests a missing page.

Tags (Feat2-FR2)
This test ensures that you can add a menu item with tags

Editing Menu (Feat2-FR4)
These tests test updating and removing a menu item.

Search & Filtering (Feat3-FR4)
The Search by Cuisine test verifies that the system can filter results based on specific tags.
It confirms that when a user searches for a specific cuisine, the repository returns only the matching restaurants.

Performance & Pagination (Feat3-FR5)
The Pagination test ensures the system handles large data volumes efficiently.
By requesting data in small chunks across multiple pages, it confirms that the limit is strictly followed.

Restaurant Edge Cases (Feat2-FR3)
The two edge cases ensure you cannot get or update a nonexistaant restaurant.

Rating and Reviewing (Feat3-FR3)
There is a functional test to ensure rating is updated properly, and that it is added properly.
There are two edge cases for rating a nonexistent restaurant and adding a review to a nonexistent restaurant.
