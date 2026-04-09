# EXTRA FEATURE: Loyalty Program Schemas
from pydantic import BaseModel
from enum import Enum

class LoyaltyTier(str, Enum):
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"

class LoyaltyConfig(BaseModel):
    """Configuration values for the loyalty rewards engine."""
    points_per_dollar: int = 10
    silver_threshold: int = 500
    gold_threshold: int = 1000
    gold_discount_rate: float = 0.10