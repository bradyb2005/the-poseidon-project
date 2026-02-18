# backend/repositories/user_repository.py
#this file is responsible for saving and loading user data to/from the JSON file.
import json
import os
from typing import Optional, List, Dict


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

        next_id = 1 if not users else max(u["id"] for u in users) + 1
        user_dict["id"] = next_id

        users.append(user_dict)
        self._save_all(users)
        return user_dict
