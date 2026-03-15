# backend/repositories/user_repository.py
#this file is responsible for saving and loading user data to/from the JSON file.
import json
import os
from typing import Optional, List, Dict
from backend.models.user.user_model import User


DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "users.json"
)


class UserRepository:
    def _load_all(self) -> List[Dict]:
        if not os.path.exists(DATA_FILE):
            # if file doesn't exist yet, treat as empty db
            return []
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_all(self, users: List[Dict]) -> None:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2)

    def find_by_username(self, username: str) -> Optional[Dict]:
        users = self._load_all()
        for u in users:
            if u["username"] == username:
                return u
        return None

    def find_by_id(self, user_id: int) -> Optional[Dict]:
        users = self._load_all()
        for u in users:
            if u["id"] == user_id:
                return u
        return None

    def create(self, user_dict: Dict) -> Dict:
        users = self._load_all()

        # Make a cope to avoid replacing keys in the original dict passed by caller
        user_to_save = dict(user_dict)

        # --- SECURITY: never persist raw password ---
        if "password" in user_to_save:
            raw = user_to_save.pop("password")
            user_to_save["password_hash"] = User.hash_password(raw)

        if "raw_password" in user_to_save:
            raw = user_to_save.pop("raw_password")
            user_to_save["password_hash"] = User.hash_password(raw)

        if "password_hash" not in user_to_save or not str(user_to_save["password_hash"]).strip():
            raise ValueError("UserRepository.create requires password_hash (or password/raw_password to hash)")

        # Assign ID (ignore any incoming id)
        next_id = 1 if not users else max(u["id"] for u in users) + 1
        user_to_save["id"] = next_id

        # Final safety check: do not store raw password keys
        user_to_save.pop("password", None)
        user_to_save.pop("raw_password", None)

        users.append(user_to_save)
        self._save_all(users)
        return user_to_save
    
    from backend.models.user.user_model import User
    
    def update_username(self, user_id: int, new_username: str):
        users = self._load_all()
        for u in users:
            if u["id"] == user_id:
                u["username"] = new_username
                self._save_all(users)
                return u
        return None

    def update_email(self, user_id: int, new_email: str):
        users = self._load_all()
        for u in users:
            if u["id"] == user_id:
                u["email"] = new_email
                self._save_all(users)
                return u
        return None

    def update_password(self, user_id: int, new_password: str):
        users = self._load_all()
        for u in users:
            if u["id"] == user_id:
                u["password_hash"] = User.hash_password(new_password)

                # safety: ensure we NEVER keep raw password keys
                u.pop("password", None)
                u.pop("raw_password", None)

                self._save_all(users)
                return u
        return None
