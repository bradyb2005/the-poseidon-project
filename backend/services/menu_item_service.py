# backend/ services/ menu_service.py

class EntityNotFoundError(Exception):
    # Throws error if something cant be found in database
    pass


class MenuService:
    def __init__(self, repository):
        self.repository = repository

    def update_item_availability(self, restaurant_id: int,
                                 item_id: int, status: bool):
        # Check if restaurant exists
        restaurant = self.repository.get_restaurant_by_id(restaurant_id)
        if not restaurant:
            raise EntityNotFoundError(
                f"Update failed: Restaurant with ID {
                    restaurant_id} not found.")

        # Check if menu item exists
        menu_item = self.repository.get_menu_item_by_id(item_id)
        if not menu_item:
            raise EntityNotFoundError(
                f"Update failed: Menu Item with ID {item_id} not found.")

        # Checks if menu item is in restaurant
        if menu_item.restaurant_id != restaurant_id:
            raise EntityNotFoundError(
                f"Item {item_id} does not belong to Restaurant {
                    restaurant_id}.")

        # Update
        menu_item.availability = status
        self.repository.save(menu_item)

        return menu_item
