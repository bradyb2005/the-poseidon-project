Restaurant Repository Tests

<img width="703" height="120" alt="Screenshot 2026-03-12 at 3 39 15 PM" src="https://github.com/user-attachments/assets/77e26b84-a846-4ef8-9c06-e0f3f7e83703" />

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
