# backend/models/user/init.user.py
#this file defines a user class, it represnets users within our system (customers, restaurant owners, admins).

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
import bcrypt


@dataclass
class User:
    """
    User Model (based on UML diagram)

    UML Attributes:
      - id: int
      - username: String
      - password: String

    In our code:
      - we stored password_hash instead of raw password for safety, as hashing is a one way function and it is unsafe to store raw passwords.
        hashing takes a raw password and converts it into a fized length of random string, and we can check if raw password is correct by hash matching.
      - we also include role (customer/admin/restaurant_owner) so we can represent
        Admin + RestaurantOwner + Customer without needing 3 separate classes yet.
    """

    id: int
    username: str
    password_hash: str

    def __post_init__(self) -> None:
        """
        This runs right after the dataclass constructor, which means it runs after we create a User object.
        We use it to validate that the User object is not invalid.
        """
        if not isinstance(self.id, int) or self.id < 0:
            raise ValueError("id must be a non-negative integer")

        if not isinstance(self.username, str) or not self.username.strip():
            raise ValueError("username must be a non-empty string")

        if not isinstance(self.password_hash, str) or not self.password_hash.strip():
            raise ValueError("password_hash must be a non-empty string")


    
    # -----------------------------------------------------------------------------
    # Password helpers
    # -----------------------------------------------------------------------------

    @staticmethod
    def hash_password(raw_password: str) -> str:
        """
        Convert a raw password into a bcrypt hash string, bcrpyt is a hashing algorithm 
        and it is slow and salted, which is more secure against brute-force attacks than SHA256.
        """
        if not isinstance(raw_password, str) or not raw_password.strip():
            raise ValueError("password must be a non-empty string")

        hashed_bytes = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt())
        return hashed_bytes.decode("utf-8")  # store as string in JSON

    def check_password(self, raw_password: str) -> bool:
        """Return True if the raw password matches our stored password_hash."""
        if not isinstance(raw_password, str):
            return False
        return bcrypt.checkpw(
            raw_password.encode("utf-8"),
            self.password_hash.encode("utf-8")
        )

    def update_password(self, new_password: str) -> None:
        """Update user's password_hash using bcrypt."""
        self.password_hash = User.hash_password(new_password)
        

    # -----------------------------------------------------------------------------
    # Repo helpers (saving/loading)
    # -----------------------------------------------------------------------------
    def to_dict(self) -> Dict:
        """Convert User into a dictionary (easy to save to JSON later)."""
        return {
        "id": self.id,
        "username": self.username,
        "password_hash": self.password_hash,
        "user_type": self.__class__.__name__,
    }

    @staticmethod
    
    def from_dict(data: Dict) -> "User":
        user_type = data.get("user_type", "User")

        from backend.models.user.customer import Customer
        from backend.models.user.restaurant_owner import RestaurantOwner
        from backend.models.user.admin_model import Admin

        cls_map = {
            "User": User,
            "Customer": Customer,
            "RestaurantOwner": RestaurantOwner,
            "Admin": Admin,
        }

        cls = cls_map.get(user_type, User)

        return cls(
            id=int(data["id"]),
            username=str(data["username"]),
            password_hash=str(data["password_hash"]),
        )


