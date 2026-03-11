from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
import bcrypt


@dataclass
class User:
    """
    User model for authentication/basic user storage.
    """

    id: int
    username: str
    password_hash: str

    def __post_init__(self) -> None:
        if not isinstance(self.id, int) or self.id < 0:
            raise ValueError("id must be a non-negative integer")

        if not isinstance(self.username, str) or not self.username.strip():
            raise ValueError("username must be a non-empty string")

        if not isinstance(self.password_hash, str) or not self.password_hash.strip():
            raise ValueError("password_hash must be a non-empty string")

    @staticmethod
    def hash_password(raw_password: str) -> str:
        if not isinstance(raw_password, str) or not raw_password.strip():
            raise ValueError("password must be a non-empty string")

        hashed_bytes = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt())
        return hashed_bytes.decode("utf-8")

    @staticmethod
    def verify_password(raw_password: str, password_hash: str) -> bool:
        if not isinstance(raw_password, str) or not isinstance(password_hash, str):
            return False

        return bcrypt.checkpw(
            raw_password.encode("utf-8"),
            password_hash.encode("utf-8")
        )

    def check_password(self, raw_password: str) -> bool:
        return User.verify_password(raw_password, self.password_hash)

    def login(self, raw_password: str) -> bool:
        return self.check_password(raw_password)

    def update_password(self, new_password: str) -> None:
        self.password_hash = User.hash_password(new_password)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            "user_type": "User",
        }

    @staticmethod
    def from_dict(data: Dict) -> "User":
        return User(
            id=int(data["id"]),
            username=str(data["username"]),
            password_hash=str(data["password_hash"]),
        )