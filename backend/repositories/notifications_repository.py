import json
from pathlib import Path


class NotificationRepository:
    """Repository for loading and saving notifications."""

    def __init__(self, file_path: str = "backend/data/notifications.json"):
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)

    def load_all(self) -> list[dict]:
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_all(self, notifications: list[dict]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(notifications, file, indent=4)