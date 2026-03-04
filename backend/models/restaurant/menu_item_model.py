# backend/models/restaurant/menu_item_model.py
import uuid

class MenuItem:
    def __init__(self, name: str, price: float):
        self.id = str(uuid.uuid4())
        self.name = name
        self.price = price
