# backend/tests/restaurant/unit_tests/test_restaurant_model.py
import pytest
from backend.models.restaurant.restaurant_model import Restaurant
from backend.models.restaurant.menu_item_model import MenuItem
from backend.models.review.review_model import Review


@pytest.fixture
def sample_menu():
    return [
        MenuItem(name="Burger", price=9.99, id=1),
        MenuItem(name="Pizza", price=12.99, id=2)
    ]


@pytest.fixture
def sample_restaurant(mock_owner, sample_menu):
    return Restaurant(
        name="Testaurant",
        owner=mock_owner,
        open_time=900,
        close_time=1700,
        address="123 Test St",
        phone="555-555-5555",
        distance_from_user=2.5,
        menu=sample_menu,
        id=0
    )


''' Create restaurant initialization'''


def test_restaurant_initialization(sample_restaurant):
    # Positive Functional Test: The restaurant model initializes correctly
    assert sample_restaurant.name == "Testaurant"
    assert sample_restaurant.open_time == 900
    assert sample_restaurant.close_time == 1700
    assert sample_restaurant.distance_from_user == 2.5
    assert len(sample_restaurant.menu) == 2
    assert isinstance(sample_restaurant.id, int)
    assert sample_restaurant.id == 0


def test_menu_item_initialization(sample_menu):
    # Positive Functional Test: The menu item models are stored correctly
    item = sample_menu[0]
    assert item.name == "Burger"
    assert item.price == 9.99
    assert isinstance(item.id, int)


# FR3: Validation tests

def test_validate_for_publish_success(mock_owner):
    # Positive functional test: Valid restaurant should pass validation
    restaurant = Restaurant(
        name="Testaurant",
        owner=mock_owner,
        address="123 Test St",
        phone="123-456-7890",
        open_time=900,
        close_time=2100,
        menu=[MenuItem(name="Burger", price=9.99)]
    )
    restaurant.validate_for_publish()


def test_validate_for_publish_missing_field(mock_owner):
    # Negative functional test: Should not pass if missing a field
    restaurant = Restaurant(
        name="Testaurant",
        owner=mock_owner,
        phone="123-456-7890",
        open_time=900,
        close_time=2100,
        menu=[MenuItem(name="Burger", price=9.99)]
        # address missing
    )
    with pytest.raises(ValueError, match="'address' is required."):
        restaurant.validate_for_publish()


def test_validate_for_publish_invalid_types(mock_owner):
    # Negative functional test: Should not pass if type check fails
    restaurant = Restaurant(
        name="Testaurant",
        owner=mock_owner,
        address="123 Test St",
        phone="123-456-7890",
        open_time="900",
        close_time=2100,
        menu=[MenuItem(name="Burger", price=9.99)]
    )
    with pytest.raises(ValueError, match="must be numbers"):
        restaurant.validate_for_publish()


def test_validate_for_publish_logic_error(mock_owner):
    # Negative funtional test: Should not pass if logic check fails
    restaurant = Restaurant(
        name="Testaurant",
        owner=mock_owner,
        address="123 Test St",
        phone="123-456-7890",
        open_time=2200,
        close_time=2100,
        menu=[MenuItem(name="Burger", price=9.99)]
    )
    with pytest.raises(ValueError, match="must be before 'close_time'"):
        restaurant.validate_for_publish()

# --- Reviews/ Ratings ---


def test_restaurant_rating_update_logic(sample_restaurant):
    """
    Feat3-FR3:
    Functional test: update the average rating
    """
    rev1 = Review(rating=5, comment="Great!", restaurant_id=1,
                  customer_id=101, customer_name="Alice")
    rev2 = Review(rating=3, comment="Okay.", restaurant_id=1,
                  customer_id=102, customer_name="Bob")

    sample_restaurant.reviews = [rev1, rev2]
    sample_restaurant.update_average_rating()

    assert sample_restaurant.average_rating == 4.0


def test_get_view_includes_reviews_and_menu(sample_restaurant):
    """
    Feat3-FR3:
    Functional test: Ensures view includes reviews and menu
    """
    sample_restaurant.is_published = True

    sample_restaurant.reviews = [
        Review(rating=5, comment="Yum", restaurant_id=1,
               customer_id=10, customer_name="Tom")
    ]

    view = sample_restaurant.get_view(role="Customer")

    assert "average_rating" in view
    assert "menu" in view
    assert "reviews" in view
    assert len(view["menu"]) == 2


def test_average_rating_with_no_reviews(sample_restaurant):
    """
    Feat3-FR3
    Edge case test: Shows that if there is no reviews,
    there cannot be an average rating
    """
    sample_restaurant.reviews = []
    sample_restaurant.update_average_rating()
    assert sample_restaurant.average_rating == 0.0


def test_rating_rounding_precision(sample_restaurant):
    """
    Feat3-FR3:
    Edge case test: Tests for rounding
    """
    sample_restaurant.reviews = [
        Review(rating=5, comment="A", restaurant_id=1,
               customer_id=1, customer_name="U1"),
        Review(rating=5, comment="B", restaurant_id=1,
               customer_id=1, customer_name="U2"),
        Review(rating=4, comment="C", restaurant_id=1,
               customer_id=1, customer_name="U3")
    ]
    sample_restaurant.update_average_rating()

    # Asserting rounding to 1 decimal place
    assert sample_restaurant.average_rating == 4.7


def test_validation_ignores_impossible_ratings(sample_restaurant):
    """
    Feat3-FR3
    Edge case: tests impossibly high rating
    """
    sample_restaurant.reviews = [Review(rating=100, comment="Hacker",
                                        restaurant_id=1, customer_id=999, customer_name="X")]
    sample_restaurant.update_average_rating()
    assert sample_restaurant.average_rating == 100.0


def test_customer_view_full_data_payload(sample_restaurant):
    """
    Feat3-FR3:
    Functional test: Verify customer can see full menu and
    reviews when 'opening' the restaurant
    """
    sample_restaurant.is_published = True
    view = sample_restaurant.get_view(role="Customer")

    # Check that menu items have all necessary data
    for item in view["menu"]:
        assert "name" in item
        assert "price" in item

    assert isinstance(view["reviews"], list)


def test_get_view_returns_none_for_unpublished_restaurant(sample_restaurant):
    """
    Feat3-FR3
    Edge Case: Ensure customer cannot browse menu/reviews
    of an unpublished restaurant
    """
    sample_restaurant.is_published = False
    view = sample_restaurant.get_view(role="Customer")

    assert view is None


def test_rating_math_with_boundary_values(sample_restaurant):
    """
    Feat3-FR3:
    Edge Case: Verify calculation with minimum possible valid ratings
    """
    sample_restaurant.reviews = [
        Review(rating=1, comment="Bad", restaurant_id=1,
               customer_id=101, customer_name="X"),
        Review(rating=1, comment="Poor", restaurant_id=1,
               customer_id=101, customer_name="Y")
    ]
    sample_restaurant.update_average_rating()
    assert sample_restaurant.average_rating == 1.0

# More tests will be made for review and rating including negative review.
# This will be done by another team member
