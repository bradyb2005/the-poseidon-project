# backend/tests/loyalty/unit_tests/test_loyalty_service.py
import pytest
from backend.services.loyalty_service import LoyaltyService
from backend.schemas.loyalty_schema import LoyaltyTier, LoyaltyConfig

@pytest.fixture
def loyalty_service():
    return LoyaltyService()

@pytest.fixture
def custom_loyalty_service():
    config = LoyaltyConfig(points_per_dollar=10, silver_threshold=500, gold_threshold=1000, gold_discount_rate=0.10)
    return LoyaltyService(config=config)

# --- Point Calculation Tests ---

def test_calculate_earned_points_standard(loyalty_service):
    """Equivalence Partitioning: Standard positive subtotal"""
    assert loyalty_service.calculate_earned_points(15.50) == 155

def test_calculate_earned_points_zero(loyalty_service):
    """Boundary Value Analysis: Zero subtotal"""
    assert loyalty_service.calculate_earned_points(0.0) == 0

def test_calculate_earned_points_negative(loyalty_service):
    """Boundary Value Analysis: Negative subtotal"""
    assert loyalty_service.calculate_earned_points(-5.0) == 0

def test_calculate_earned_points_custom_config(custom_loyalty_service):
    """Functional Test: Proves the config multiplier works"""
    # 20.0 subtotal * 10 points per dollar config
    assert custom_loyalty_service.calculate_earned_points(20.0) == 200

# --- Tier Evaluation Tests ---

@pytest.mark.parametrize("points, expected_tier", [
    (0, LoyaltyTier.BRONZE.value),     # Boundary: Zero points
    (499, LoyaltyTier.BRONZE.value),   # Boundary: Just below Silver
    (500, LoyaltyTier.SILVER.value),   # Boundary: Exact Silver threshold
    (750, LoyaltyTier.SILVER.value),   # Equivalence: Middle of Silver
    (999, LoyaltyTier.SILVER.value),   # Boundary: Just below Gold
    (1000, LoyaltyTier.GOLD.value),    # Boundary: Exact Gold threshold
    (5000, LoyaltyTier.GOLD.value),    # Equivalence: Way above Gold
])
def test_evaluate_tier_standard(loyalty_service, points, expected_tier):
    """Parameterized testing for standard tier thresholds."""
    assert loyalty_service.evaluate_tier(points) == expected_tier

def test_evaluate_tier_custom_config(custom_loyalty_service):
    """Functional Test: Proves the config thresholds work"""
    assert custom_loyalty_service.evaluate_tier(550) == LoyaltyTier.SILVER.value
    assert custom_loyalty_service.evaluate_tier(1050) == LoyaltyTier.GOLD.value

# --- Benefit Application Tests ---

@pytest.fixture
def standard_cost_breakdown():
    return {
        "_subtotal": 20.0,
        "_delivery_fee": 5.0,
        "_service_fee": 2.0,
        "_tax": 1.0,
        "_total": 28.0
    }

def test_apply_tier_benefits_bronze(loyalty_service, standard_cost_breakdown):
    """Equivalence Partitioning: Bronze tier should not alter costs."""
    result = loyalty_service.apply_tier_benefits(LoyaltyTier.BRONZE.value, standard_cost_breakdown)
    
    assert result["_subtotal"] == 20.0
    assert result["_delivery_fee"] == 5.0
    assert result["_total"] == 28.0

def test_apply_tier_benefits_silver(loyalty_service, standard_cost_breakdown):
    """Equivalence Partitioning: Silver tier should waive delivery fee."""
    result = loyalty_service.apply_tier_benefits(LoyaltyTier.SILVER.value, standard_cost_breakdown)
    
    assert result["_subtotal"] == 20.0
    assert result["_delivery_fee"] == 0.0
    assert result["_total"] == 23.0  # Recalculated: 20 + 0 + 2 + 1

def test_apply_tier_benefits_gold(loyalty_service, standard_cost_breakdown):
    """Equivalence Partitioning: Gold tier should discount subtotal by 10% and waive delivery."""
    result = loyalty_service.apply_tier_benefits(LoyaltyTier.GOLD.value, standard_cost_breakdown)
    
    # 10% off 20.0 is 2.0. New subtotal: 18.0
    assert result["_subtotal"] == 18.0
    assert result["_delivery_fee"] == 0.0
    assert result["_total"] == 21.0  # Recalculated: 18 + 0 + 2 + 1

def test_apply_tier_benefits_missing_keys(custom_loyalty_service):
    """Robustness: Service should handle a partial dictionary without crashing."""
    partial_costs = {"_subtotal": 10.0} # Missing tax, delivery, service fee
    result = custom_loyalty_service.apply_tier_benefits(LoyaltyTier.BRONZE.value, partial_costs)
    
    # Should calculate total as 10.0 + 0 + 0 + 0
    assert result["_total"] == 10.0