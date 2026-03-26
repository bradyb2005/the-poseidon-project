import bcrypt

from backend.repositories.user_repository import UserRepository


class UserService:
    """Service layer for user business logic."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def hash_password(self, password: str) -> str:
        """Return a hashed version of a plain text password."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, password: str, password_hash: str) -> bool:
        """Check whether a plain text password matches its hash."""
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

    def create_user(self, username: str, email: str, password: str) -> dict:
        """Create a new user with a unique username."""
        users = self.user_repo.load_all()

        for existing_user in users:
            if existing_user["username"] == username:
                raise ValueError("username already exists")

        new_id = str(len(users) + 1)
        password_hash = self.hash_password(password)

        user = {
            "id": new_id,
            "username": username,
            "email": email,
            "password_hash": password_hash
        }

        users.append(user)
        self.user_repo.save_all(users)

        return user

    def update_username(self, user_id: str, new_username: str) -> dict:
        """Update a user's username."""
        users = self.user_repo.load_all()

        for user in users:
            if user["username"] == new_username and user["id"] != user_id:
                raise ValueError("username already exists")

        for user in users:
            if user["id"] == user_id:
                user["username"] = new_username
                self.user_repo.save_all(users)
                return user

        raise ValueError("user not found")

    def update_email(self, user_id: str, new_email: str) -> dict:
        """Update a user's email."""
        users = self.user_repo.load_all()

        for user in users:
            if user["id"] == user_id:
                user["email"] = new_email
                self.user_repo.save_all(users)
                return user

        raise ValueError("user not found")

    def update_password(self, user_id: str, current_password: str, new_password: str) -> dict:
        """Update a user's password after verifying the current password."""
        users = self.user_repo.load_all()

        for user in users:
            if user["id"] == user_id:
                if not self.verify_password(current_password, user["password_hash"]):
                    raise ValueError("current password is incorrect")

                user["password_hash"] = self.hash_password(new_password)
                self.user_repo.save_all(users)
                return user

        raise ValueError("user not found")
    
    def forgot_password(self, email: str, new_password: str) -> dict:
        """Reset a user's password using their email."""
        users = self.user_repo.load_all()

        for user in users:
            if user["email"] == email:
                user["password_hash"] = self.hash_password(new_password)
                self.user_repo.save_all(users)
                return user

        raise ValueError("user not found")