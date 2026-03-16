# backend/models/restaurant/restaurant_model.py
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

# Read by VSCode for type checking but python ignores
if TYPE_CHECKING:
    from backend.models.restaurant.menu_item_model import MenuItem
    from backend.models.user.restaurant_owner_model import RestaurantOwner
    from backend.models.review.review_model import Review


@dataclass
class Restaurant:
    name: str
    owner: 'RestaurantOwner'
    open_time: Optional[int] = None
    close_time: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    distance_from_user: Optional[float] = None
    menu: List["MenuItem"] = field(default_factory=list)
    reviews: List["Review"] = field(default_factory=list)
    average_rating: float = 0.0

    # Defaults
    id: int = None
    is_open: bool = False
    is_published: bool = False

    def get_view(self, role: str):
        if role == "Customer" and not self.is_published:
            return None
        return {
            "id": self.id,
            "name": self.name,
            "average_rating": self.average_rating,
            "menu": [vars(item) for item in self.menu],
            "reviews": [vars(rev) for rev in self.reviews],
            "is_published": self.is_published
        }

    def update_average_rating(self):
        """
        Feat3-FR3: Functional logic for average logic to update when
        new ratings are added
        """
        if not self.reviews:
            self.average_rating = 0.0
            return

        total = sum(review.rating for review in self.reviews)
        self.average_rating = round(total / len(self.reviews), 1)

    def validate_for_publish(self):
        """
        Feat2-FR3: Ensure all required fields are valid before publishing
        - Check for missing values, type check and then logic check
        """
        if not self.menu:
            raise ValueError("Cannot publish restaurant: menu cannot be empty")

        required_fields = {
            "address": self.address,
            "phone": self.phone,
            "open_time": self.open_time,
            "close_time": self.close_time
        }

        for field_name, value in required_fields.items():
            # Check for missing values
            if value is None or (isinstance(value, str) and not value.strip()):
                raise ValueError(
                    f"Cannot publish restaurant: '{
                        field_name}' is required and cannot be empty.")

        if not isinstance(self.open_time, int) or not isinstance(
            self.close_time, int):
            # Type checking
            # Cannot fix flaking error without breaking code
            raise ValueError(
                "Cannot publish restaurant: 'open_time' and 'close_time' must be numbers")

        if self.open_time >= self.close_time:
            # Logic checking
            # Cannot fix flaking error without breaking code
            raise ValueError(
                "Cannot publish restaurant: 'open_time' must be before 'close_time'")
