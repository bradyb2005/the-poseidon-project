from backend.schemas.cart_schema import Cart, OrderItem
from backend.schemas.items_schema import MenuItem

from backend.repositories.items_repository import ItemRepository
from backend.repositories.user_repository import UserRepository

class CartService:
    def __init__(self):
        menu_repo = ItemRepository()
        self.menu_repo = menu_repo
        user_repo = UserRepository()
        self.user_repo = user_repo


    def add_to_cart(self, customer_id: str, menu_item_id: str, quantity: int):
        users = self.user_repo.load_all()
        user = next((u for u in users if u["id"] == customer_id), None)
        if not user:
            return {"error": "User not found"}, 404

        items = self.menu_repo.load_all()
        menu_item = next((i for i in items if i.item_id == menu_item_id), None)
        if not menu_item:
            return {"error": "Menu item not found"}, 404
        
        if not menu_item.availability:
            return {"error": "Menu item is not available"}, 400

        cart_items = user.get("cart", {}).get("items", [])

        if cart_items:
            first_item_id = cart_items[0].get("menu_item_id")
            
            first_item_details = next((i for i in items if str(i.item_id) == str(first_item_id)), None)
            
            if first_item_details and str(first_item_details.restaurant_id) != str(menu_item.restaurant_id):
                return {"error": "All items in the cart must be from the same restaurant."}, 400

        existing_item = next((item for item in cart_items if str(item.get("menu_item_id")) == str(menu_item_id)), None)

        if existing_item:
            existing_item["quantity"] += quantity
        else:
            new_item = OrderItem(
                menu_item_id=str(menu_item_id),
                quantity=quantity,
                price_at_time=menu_item.price 
            )
            cart_items.append(new_item.model_dump(mode='json'))

        if "cart" not in user:
            user["cart"] = {"customer_id": customer_id, "items": cart_items}
        else:
            user["cart"]["items"] = cart_items

        self.user_repo.save_all(users)

        return {"message": "Item added to cart successfully", "cart": user["cart"]}, 200
    
    def update_quantity(self, customer_id: str, menu_item_id: str, new_quantity: int):
        users = self.user_repo.load_all()
        user = next((u for u in users if u["id"] == customer_id), None)
        if not user:
            return {"error": "User not found"}, 404

        cart_items = user.get("cart", {}).get("items", [])
        existing_item = next((item for item in cart_items if str(item.get("menu_item_id")) == str(menu_item_id)), None)

        if not existing_item:
            return {"error": "Menu item not found in cart"}, 404

        if new_quantity <= 0:
            return self.remove_from_cart(customer_id, menu_item_id)        
        else:
            existing_item["quantity"] = new_quantity

        self.user_repo.save_all(users)

        return {"message": "Cart updated successfully", "cart": user["cart"]}, 200
    
    def remove_from_cart(self, customer_id: str, menu_item_id: str):
        users = self.user_repo.load_all()
        user = next((u for u in users if u["id"] == customer_id), None)
        if not user:
            return {"error": "User not found"}, 404

        cart_items = user.get("cart", {}).get("items", [])
        existing_item = next((item for item in cart_items if str(item.get("menu_item_id")) == str(menu_item_id)), None)

        if not existing_item:
            return {"error": "Menu item not found in cart"}, 404

        cart_items.remove(existing_item)

        self.user_repo.save_all(users)

        return {"message": "Item removed from cart successfully", "cart": user["cart"]}, 200
    
    def clear_cart(self, customer_id: str):
        users = self.user_repo.load_all()
        user = next((u for u in users if u["id"] == customer_id), None)
        if not user:
            return {"error": "User not found"}, 404

        user["cart"] = {"customer_id": customer_id, "items": []}

        self.user_repo.save_all(users)

        return {"message": "Cart cleared successfully", "cart": user["cart"]}, 200