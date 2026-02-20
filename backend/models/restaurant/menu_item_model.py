# backend/models/restaurant/restaurant_model.py

class MenuItem:
    def __init__(self, id: int, name: str, price: float, availability: bool = True):
        self.id = id
        self.name = name
        self.price = price
        self.availability = availability
        self.description = None
        self.category = None