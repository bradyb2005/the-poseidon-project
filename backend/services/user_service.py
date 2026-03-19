from __future__ import annotations

from backend.models.user.user_model import User
from backend.repositories.user_repository import UserRepository

# fixed email error - 19-03-2026

class UserService:
    """
    Service layer for Users.
    """

    def __init__(self) -> None:
        self.repo = UserRepository()

    def register(self, username: str, email: str, password: str) -> dict:
        existing = self.repo.find_by_username(username)
        if existing:
            raise ValueError("Username already exists")

        password_hash = User.hash_password(password)
        user = User(
            id=0,
            username=username,
            email=email,
            password_hash=password_hash
        )

        return self.repo.create(user.to_dict())

    def login(self, username: str, password: str) -> bool:
        user_dict = self.repo.find_by_username(username)
        if not user_dict:
            return False

        user = User.from_dict(user_dict)
        return user.check_password(password)