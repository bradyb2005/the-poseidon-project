from __future__ import annotations
from typing import Literal

from backend.models.user.user_model import User
from backend.repositories.user_repository import UserRepository
from backend.models.user.customer import Customer
from backend.models.user.restaurant_owner_model import RestaurantOwner
from backend.models.user.admin import Admin

RoleType = Literal["Customer", "RestaurantOwner", "Admin"]

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, username: str, email: str, password: str, role: RoleType) -> User:
    

        if self.user_repo.find_by_username(username) is not None:
            raise ValueError("username already exists")

        password_hash = User.hash_password(password)

        if role == "Customer":
            user = Customer(id=0, username=username, email=email, password_hash=password_hash)

        elif role == "Admin":
            user = Admin(id=0, username=username, email=email, password_hash=password_hash)

        elif role == "RestaurantOwner":
            # requirement: admin verification needed
            raise ValueError("restaurant owner requires admin verification")
            # if later allowed:
            # user = RestaurantOwner(id=0, username=username, email=email, password_hash=password_hash)

        else:
            raise ValueError(f"Invalid role: {role}")

        created_dict = self.user_repo.create(user.to_dict())
        return User.from_dict(created_dict)