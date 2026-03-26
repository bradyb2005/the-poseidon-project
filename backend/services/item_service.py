# backend/services/item_service.py
from typing import List, Optional, Tuple, Dict, Any
from uuid import UUID
from backend.schemas.items_schema import MenuItem, CreateMenuItemSchema, UpdateMenuItemSchema

class MenuService:
    def __init__(self, repository):
        self.repository = repository

    def _get_and_verify_owner(self, restaurant_id: str, owner_id: str) -> Tuple[Optional[Any], int]:
        restaurant = self.repository.get_by_id(restaurant_id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404

        actual_owner_id = str(getattr(restaurant, 'owner_id', '')) or str(restaurant.get('owner_id', ''))
        
        if actual_owner_id != str(owner_id):
            return {"error": "Access denied: You do not own this restaurant."}, 403
        
        return restaurant, 200

    def add_menu_item(self, owner_id: str, restaurant_id: str, item_data: dict) -> Tuple[Dict, int]:
        """
        Feat2-FR4: Adding and editing menu items
        Add new item to a specific restaurant menu
        """
        _, status = self._get_and_verify_owner(restaurant_id, owner_id)
        if status != 200:
            return _, status

        try:
            item_data['restaurant_id'] = restaurant_id
            new_item_schema = CreateMenuItemSchema(**item_data)

            success = self.repository.add_menu_item(restaurant_id, new_item_schema)
            if not success:
                return {"error": "Failed to add item to database"}, 500
                
            return {
                "message": "Item added successfully", 
                "item_id": str(new_item_schema.item_id)
            }, 201
        except (ValueError, TypeError) as e:
            return {"error": str(e)}, 400

    def edit_menu_item(self, owner_id: str, restaurant_id: str, item_id: str, updated_data: dict) -> Tuple[Dict, int]:
        """
        Feat2-FR4: Adding and editing menu items
        Edit an existing menu item.
        """
        _, status = self._get_and_verify_owner(restaurant_id, owner_id)
        if status != 200:
            return _, status

        try:
            update_schema = UpdateMenuItemSchema(**updated_data)
            
            success = self.repository.update_menu_item(restaurant_id, item_id, update_schema)
            if not success:
                return {"error": f"Menu item {item_id} not found"}, 404

            return {"message": "Menu item updated successfully"}, 200
        except (ValueError, TypeError) as e:
            return {"error": str(e)}, 400


    def remove_menu_item(self, owner_id: str, restaurant_id: str, item_id: str) -> Tuple[Dict, int]:
        """
        Feat2-FR4: Adding and editing menu items
        Remove an item from the menu
        """
        _, status = self._get_and_verify_owner(restaurant_id, owner_id)
        if status != 200:
            return _, status

        success = self.repository.remove_menu_item(restaurant_id, item_id)
        if not success:
            return {"error": f"Menu item {item_id} not found."}, 404
            
        return {"message": "Item removed successfully"}, 200

    def update_item_availability(self, owner_id: str, restaurant_id: str, item_id: str, status_bool: bool) -> Tuple[Dict, int]:
        """
        Feat2-FR4: Adding and Editing menu items
        Toggle visibility/availability of a menu item.
        """
        _, status = self._get_and_verify_owner(restaurant_id, owner_id)
        if status != 200:
            return _, status

        success = self.repository.update_menu_item_availability(restaurant_id, item_id, status_bool)
        if not success:
            return {"error": f"Menu Item with ID {item_id} not found."}, 404
            
        return {"message": "Availability updated", "status": status_bool}, 200
    