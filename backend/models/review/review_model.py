from __future__ import annotations
from dataclasses import dataclass
from typing import Dict


@dataclass
class Review:
    id: int
    user_id: int
    restaurant_id: int
    rating: int
    comment: str = ""

    def __post_init__(self) -> None:
        if self.id < 0:
            raise ValueError("id must be non-negative")

        if self.user_id < 0:
            raise ValueError("user_id must be non-negative")

        if self.restaurant_id < 0:
            raise ValueError("restaurant_id must be non-negative")

        if not (1 <= self.rating <= 5):
            raise ValueError("rating must be between 1 and 5")

        if not isinstance(self.comment, str):
            raise ValueError("comment must be string")

    # -----------------------
    # helpers
    # -----------------------
    def update_rating(self, new_rating: int) -> None:
        if not (1 <= new_rating <= 5):
            raise ValueError("rating must be between 1 and 5")
        self.rating = new_rating

    def update_comment(self, new_comment: str) -> None:
        self.comment = new_comment

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "restaurant_id": self.restaurant_id,
            "rating": self.rating,
            "comment": self.comment,
        }

    @staticmethod
    def from_dict(data: Dict) -> "Review":
        return Review(
            id=int(data["id"]),
            user_id=int(data["user_id"]),
            restaurant_id=int(data["restaurant_id"]),
            rating=int(data["rating"]),
            comment=str(data.get("comment", "")),
        )