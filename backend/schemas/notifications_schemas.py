from dataclasses import dataclass


@dataclass
class Notification:
    id: str
    user_id: str
    type: str
    message: str
    enabled: bool = True
    is_read: bool = False

    def __post_init__(self) -> None:
        required_fields = {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "message": self.message,
        }

        for field_name, value in required_fields.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        if not isinstance(self.enabled, bool):
            raise ValueError("enabled must be a boolean")

        if not isinstance(self.is_read, bool):
            raise ValueError("is_read must be a boolean")