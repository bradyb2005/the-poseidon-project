from backend.models.user.user_model import User
from dataclasses import dataclass

@dataclass
class Customer(User):
    address: str = ""
    latitude: float = 0.0
    longitude: float = 0.0

    def __post_init__(self) -> None:
        # Call the parent validation (username, email, etc.)
        super().__post_init__()
        
        # Add basic coordinate validation if needed
        if not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
