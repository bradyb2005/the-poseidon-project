import json
import os
from typing import Optional, List, Dict
from backend.models.user.user_schema import User


DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "users.json"
)


class UserRepository:
    """Repository for loading and saving raw user JSON data."""

    def load_all(self) -> List[Dict]:
        """Load and return all users from the JSON file."""
        if not os.path.exists(DATA_FILE):
            return []

        if os.path.getsize(DATA_FILE) == 0:
            return []

        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_all(self, users: List[Dict]) -> None:
        """Save the full list of users to the JSON file."""
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2)