# The Poseidon Project
COSC 310 Final Project.

**Group Members:**
* Brady Bracken
* Anjana Ratnala
* Fabiha Afifa
* Grayson Gosse

Architecture Overview: Our architecture of choice is the Model-View-Controller (MVC) architecture because it provides a clear separation of responsibilities between the system's data, user interface, and interaction logic. The Model manages core application data such as users, restaurants, menus, orders, and reviews, ensuring that business rules and database operations remain centralized and consistent. The View handles all user-facing elements—screens for browsing menus, placing orders, and managing accounts—allowing the user interface to be updated and redesigned without affecting underlying logic. The Controller acts as the intermediary that processes user actions (e.g. logging in, adding items to a cart, or submitting reviews), coordinates with the Model to update or retrieve data, and selects the appropriate View to display results. This separation improves modularity, maintainability and scalability: team members can work on the UI, business logic, and data management independently. Future features, such as new payment methods or admin tools, can be added with minimal impact on existing components. Overall, MVC was selected to support clean organization, easier testing, and long-term extensibility for our food-ordering system.
