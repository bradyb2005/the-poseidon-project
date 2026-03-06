# backend/services/user_service.py

from backend.models.user.init.user import User
from backend.models.user.roles import CUSTOMER
from backend.repositories.user_repository import UserRepository


class UserService:
    """
    Service layer for Users.

    this is like the 'brain' that decides what should happen
    (register, login), and it uses the repository to access storage.
    """

    def __init__(self) -> None:
        # Repo = the storage helper (reads/writes users.json)
        self.repo = UserRepository()

    def register(self, username: str, password: str, role: str = CUSTOMER) -> dict:
        """
        Create a new user if username is not already taken.
        Returns the created user dict (including id) if successful.
        """
        # 1) Check if username already exists
        existing = self.repo.find_by_username(username)
        if existing:
            raise ValueError("Username already exists")

        # 2) Hash the password (never store raw password)
        password_hash = User.hash_password(password)

        # 3) Create the User model (validation happens in __post_init__)
        user = User(id=0, username=username, password_hash=password_hash, role=role)

        # 4) Save using repository (repo assigns the real id)
        created_user_dict = self.repo.create(user.to_dict())

        return created_user_dict

    def login(self, username: str, password: str) -> bool:
        """
        Check username + password.

        Returns True if valid, False if not.
        """
        # 1) Look up user in storage
        user_dict = self.repo.find_by_username(username)
        if not user_dict:
            return False

        # 2) Turn dict -> User object
        user = User.from_dict(user_dict)

        # 3) Use the User model's login() (returns bool)
        return user.login(password)
