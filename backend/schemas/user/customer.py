from backend.models.user.user_model import User
from dataclasses import dataclass


@dataclass
class Customer(User):
    address: str = ""
    latitude: float = 0.0
    longitude: float = 0.0

    def __post_init__(self) -> None:
        super().__post_init__()

        # Change to float
        try:
            self.latitude = float(self.latitude)
            self.longitude = float(self.longitude)
        except (ValueError, TypeError):
            raise ValueError("Latitude and Longitude must be valid numbers.")

        # Add basic coordinate validation
        if not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
