from typing import List, TYPE_CHECKING

# Read by VSCode for type checking but python ignores
if TYPE_CHECKING:
    from backend.models.user.restaurant_owner_model import RestaurantOwner
    from backend.models.restaurant.menu_item_model import MenuItem


# Restaurant information
class Restaurant:
    def __init__(self, id: int, name: str, owner: "RestaurantOwner"):
        self.id = id
        self.name = name
        self.owner = owner

        # Hours
        self.open_time: str = ""
        self.close_time: str = ""

        # Operational details
        self.address = ""
        self.city = ""
        self.postal_code = ""
        self.phone = ""
        self.cuisine_type = ""
        self.rating = 0.0

        # Status
        self.is_open: bool = False

        # Menu
        self.menu: List["MenuItem"] = []

        # Reviews
        self.reviews: List = []
        self.total_reviews: int

    def get_average_rating(self) -> float:
        if not self.reviews:
            return 0.0
        average = sum(review.rating for review in self.reviews
                      ) / len(self.reviews)
        return round(average, 1)
