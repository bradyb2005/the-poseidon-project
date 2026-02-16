from typing import List
from dataclasses import field
from datetime import time
from enum import Enum

# Enum for days of the week
# Allows easy ref to days consistently
class DayOfWeek(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

# Business hours for a restaurant
class BusinessHours:
    day: DayOfWeek
    open_time: time
    close_time: time
    is_closed: bool = False

# Restaurant information
class Restaurant:
    id: int
    name: str
    owner: RestaurantOwner
    address: str = ""
    city: str = ""
    postal_code: str = ""
    phone: str = ""
    cuisine_type: str = ""
    business_hours: List[BusinessHours] = field(default_factory=list)
    rating: float = 0.0
    total_reviews: int = 0
    reviews: List[Review] = field(default_factory=list) # new list created so no duplicates
    menu: List[MenuItem] = field(default_factory=list)

    # getter
    def get_menu(self) -> List[MenuItem]:
        return self.menu
    # method to calculate average rating
    def get_average_rating(self) -> float:
        if self.total_reviews == 0:
            return 0.0
        return sum(review.rating for review in self.reviews) / self.total_reviews
    
    def is_open(self) -> bool:
        # Check if restaurant is currently open
        # implementation would check current time against business hours
        pass


    