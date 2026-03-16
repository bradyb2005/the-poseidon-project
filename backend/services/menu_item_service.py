# backend/ services/ menu_service.py
from backend.models.restaurant.menu_item_model import MenuItem


class EntityNotFoundError(Exception):
    # Throws error if something cant be found in database
    pass


class PermissionError(Exception):
    pass


class MenuService:
    def __init__(self, repository):
        self.repository = repository


    # --- Helper method ---

    def get_and_verify_owner(self, restaurant_id: int, owner_id: int):
        restaurant = self.repository.get_by_id(restaurant_id)
        if not restaurant:
            raise EntityNotFoundError(
                f"Restaurant with ID {restaurant_id} not found.")

        if restaurant.get('owner_id') != owner_id:
            raise PermissionError(
                "Access denied: You do not own this restaurant.")
        return restaurant

    def add_menu_item(
            self, owner_id: int, restaurant_id: str, item_data: dict):
        # Fear2-FR4: Add new item
        self.get_and_verify_owner(restaurant_id, owner_id)

        new_item = MenuItem(
            name=item_data['name'],
            price=item_data['price'],
            tags=item_data.get('tags', [])
        )
        return self.repository.add_menu_item(restaurant_id, new_item)

    def edit_menu_item(self, owner_id: int,
                       restaurant_id: str, item_id: str, updated_data: dict):
        """Feat2-FR4: Edit an existing menu item."""
        self.get_and_verify_owner(restaurant_id, owner_id)

        updated_item = MenuItem(
            id=item_id,
            name=updated_data['name'],
            price=updated_data['price'],
            tags=updated_data.get('tags', [])
        )

        success = self.repository.update_menu_item(
            restaurant_id, item_id, updated_item)
        if not success:
            raise EntityNotFoundError(f"Menu item {item_id} not found.")
        return True

    def remove_menu_item(self, owner_id: int,
                         restaurant_id: str, item_id: str):
        """Feat2-FR4: Remove an item from the menu."""
        self.get_and_verify_owner(restaurant_id, owner_id)

        success = self.repository.remove_menu_item(restaurant_id, item_id)
        if not success:
            raise EntityNotFoundError(f"Menu item {item_id} not found.")
        return True

 
    def update_item_availability(self, owner_id: int, restaurant_id: int,
                                 item_id: int, status: bool):
        self.get_and_verify_owner(restaurant_id, owner_id)

        success = self.repository.update_menu_item_availability(restaurant_id, item_id, status)
    
        if not success:
            raise EntityNotFoundError(f"Menu Item with ID {item_id} not found.")
    
        return True
