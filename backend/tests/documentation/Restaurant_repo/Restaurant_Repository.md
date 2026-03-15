Restaurant Repository Tests

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

Coordinates test (Feat3-FR1)
We have a safety net test that ensures a restaurant cannot be published without uploading its coordinate.
We also test creating a restaurant with missing coordinates. You should be able to create a restaurant and the coordinates defaul to 0, 0
