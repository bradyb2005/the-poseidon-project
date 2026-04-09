from typing import Dict
from backend.schemas.loyalty_schema import LoyaltyTier, LoyaltyConfig

class LoyaltyService:
    """Handles business logic for the user rewards and loyalty program."""
    
    def __init__(self, config: LoyaltyConfig = None):
        self.config = config or LoyaltyConfig()

    def calculate_earned_points(self, subtotal: float) -> int:
        """Calculates points earned from an order subtotal."""
        if subtotal <= 0:
            return 0
        return int(subtotal * self.config.points_per_dollar)

    def evaluate_tier(self, current_points: int) -> str:
        """Determines the appropriate tier based on total accumulated points."""
        if current_points >= self.config.gold_threshold:
            return LoyaltyTier.GOLD.value
        elif current_points >= self.config.silver_threshold:
            return LoyaltyTier.SILVER.value
        
        return LoyaltyTier.BRONZE.value

    def apply_tier_benefits(self, tier: str, cost_breakdown: Dict[str, float]) -> Dict[str, float]:
        """
        Applies discounts or fee waivers based on the user's loyalty tier.
        Modifies and returns the cost breakdown dictionary.
        """
        updated_costs = dict(cost_breakdown)
        
        if tier == LoyaltyTier.GOLD.value:
            # Gold: 10% off subtotal AND free delivery
            discount = updated_costs.get("_subtotal", 0.0) * self.config.gold_discount_rate
            updated_costs["_subtotal"] = max(0.0, updated_costs.get("_subtotal", 0.0) - discount)
            updated_costs["_delivery_fee"] = 0.0 
            
        elif tier == LoyaltyTier.SILVER.value:
            # Silver: Waive delivery fee
            updated_costs["_delivery_fee"] = 0.0
            
        # Recalculate the final total after benefits are applied
        updated_costs["_total"] = (
            updated_costs.get("_subtotal", 0.0) + 
            updated_costs.get("_delivery_fee", 0.0) + 
            updated_costs.get("_service_fee", 0.0) + 
            updated_costs.get("_tax", 0.0)
        )
        
        updated_costs["_total"] = round(updated_costs["_total"], 2)
        
        return updated_costs