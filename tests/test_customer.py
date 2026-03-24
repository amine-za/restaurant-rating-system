"""Tests for Customer class."""

import pytest

from src.customer import Customer
from src.exceptions import DuplicateRatingError
from src.restaurant import Restaurant


# Customer creation and properties
def test_customer_creation():
    """Should create a Customer with valid data."""
    customer = Customer("Alice", "alice@example.com", ["Italian"], 3)
    assert customer.name == "Alice"
    assert customer.email == "alice@example.com"
    assert customer.preferred_cuisines == ["Italian"]
    assert customer.budget_range == 3


def test_customer_default_cuisines():
    """Should default to empty list for preferred_cuisines."""
    customer = Customer("Alice", "alice@example.com", budget_range=2)
    assert customer.preferred_cuisines == []


def test_customer_default_budget():
    """Should default budget_range to 2."""
    customer = Customer("Alice", "alice@example.com")
    assert customer.budget_range == 2


def test_customer_all_budget_ranges():
    """Should accept budget ranges 1-4."""
    for budget in range(1, 5):
        customer = Customer("Alice", f"alice{budget}@example.com", budget_range=budget)
        assert customer.budget_range == budget


def test_customer_multiple_cuisines():
    """Should accept multiple preferred cuisines."""
    cuisines = ["Italian", "Japanese", "French"]
    customer = Customer("Alice", "alice@example.com", cuisines, 3)
    assert customer.preferred_cuisines == cuisines


def test_customer_invalid_email():
    """Should raise InvalidEmailError for invalid email."""
    from src.exceptions import InvalidEmailError

    with pytest.raises(InvalidEmailError):
        Customer("Alice", "not-an-email", [], 3)


def test_customer_invalid_budget_zero():
    """Should raise ValidationError for budget 0."""
    from src.exceptions import ValidationError

    with pytest.raises(ValidationError):
        Customer("Alice", "alice@example.com", [], 0)


def test_customer_invalid_budget_five():
    """Should raise ValidationError for budget > 4."""
    from src.exceptions import ValidationError

    with pytest.raises(ValidationError):
        Customer("Alice", "alice@example.com", [], 5)


def test_customer_name_trimmed():
    """Should trim whitespace from name."""
    customer = Customer("  Alice  ", "alice@example.com")
    assert customer.name == "Alice"


def test_customer_email_trimmed():
    """Should trim whitespace from email."""
    customer = Customer("Alice", "  alice@example.com  ")
    assert customer.email == "alice@example.com"


# Rating submission
def test_submit_rating():
    """Should submit a rating for a restaurant."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    rating = customer.submit_rating(restaurant, 4, "Great food!")
    assert rating.customer == customer
    assert rating.restaurant == restaurant
    assert rating.score == 4


def test_submit_rating_without_review():
    """Should submit rating without review text."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    rating = customer.submit_rating(restaurant, 5)
    assert rating.score == 5
    assert rating.review_text == ""


def test_submit_rating_all_scores():
    """Should accept rating scores 1-5."""
    customer = Customer("Alice", "alice@example.com")

    for score in range(1, 6):
        restaurant = Restaurant(
            f"Place {score}", "Italian", f"{score} Main St", 3
        )
        rating = customer.submit_rating(restaurant, score)
        assert rating.score == score


def test_submit_rating_adds_to_customer():
    """Should add submitted rating to customer's list."""
    customer = Customer("Alice", "alice@example.com")
    restaurant1 = Restaurant("Place 1", "Italian", "123 Main", 3)
    restaurant2 = Restaurant("Place 2", "French", "456 Oak", 2)

    customer.submit_rating(restaurant1, 4)
    assert len(customer.get_ratings_submitted()) == 1

    customer.submit_rating(restaurant2, 5)
    assert len(customer.get_ratings_submitted()) == 2


def test_submit_rating_adds_to_restaurant():
    """Should add rating to restaurant's ratings."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    assert restaurant.get_rating_count() == 0
    customer.submit_rating(restaurant, 4)
    assert restaurant.get_rating_count() == 1
    assert restaurant.get_average_rating() == 4.0


def test_submit_multiple_ratings_to_different_restaurants():
    """Should submit ratings to multiple different restaurants."""
    customer = Customer("Alice", "alice@example.com")
    restaurants = [
        Restaurant("Place 1", "Italian", "123 Main", 3),
        Restaurant("Place 2", "French", "456 Oak", 2),
        Restaurant("Place 3", "Japanese", "789 Pine", 4),
    ]

    for i, restaurant in enumerate(restaurants, start=1):
        customer.submit_rating(restaurant, i)

    ratings = customer.get_ratings_submitted()
    assert len(ratings) == 3


def test_duplicate_rating_prevention():
    """Should prevent same customer from rating same restaurant twice."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    customer.submit_rating(restaurant, 4)
    with pytest.raises(DuplicateRatingError):
        customer.submit_rating(restaurant, 5)


def test_duplicate_rating_error_message():
    """DuplicateRatingError should contain restaurant name."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    customer.submit_rating(restaurant, 4)
    try:
        customer.submit_rating(restaurant, 5)
        assert False, "Should have raised DuplicateRatingError"
    except DuplicateRatingError as e:
        assert "Alice" in str(e)
        assert "The Place" in str(e)


def test_duplicate_check_per_restaurant():
    """Duplicate check should be per restaurant, not global."""
    customer = Customer("Alice", "alice@example.com")
    restaurant1 = Restaurant("Place 1", "Italian", "123 Main", 3)
    restaurant2 = Restaurant("Place 2", "Italian", "123 Main", 3)

    # Same customer can rate different restaurants
    customer.submit_rating(restaurant1, 4)
    customer.submit_rating(restaurant2, 5)
    assert len(customer.get_ratings_submitted()) == 2


# Rating retrieval
def test_get_ratings_submitted_empty():
    """Should return empty list when no ratings submitted."""
    customer = Customer("Alice", "alice@example.com")
    ratings = customer.get_ratings_submitted()
    assert ratings == []


def test_get_ratings_submitted_multiple():
    """Should return all submitted ratings."""
    customer = Customer("Alice", "alice@example.com")
    restaurant1 = Restaurant("Place 1", "Italian", "123 Main", 3)
    restaurant2 = Restaurant("Place 2", "French", "456 Oak", 2)

    rating1 = customer.submit_rating(restaurant1, 4)
    rating2 = customer.submit_rating(restaurant2, 5)

    ratings = customer.get_ratings_submitted()
    assert len(ratings) == 2
    assert rating1 in ratings
    assert rating2 in ratings


def test_get_ratings_submitted_returns_copy():
    """Should return a copy of ratings list."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("Place 1", "Italian", "123 Main", 3)
    customer.submit_rating(restaurant, 4)

    ratings1 = customer.get_ratings_submitted()
    ratings2 = customer.get_ratings_submitted()
    assert ratings1 == ratings2
    assert ratings1 is not ratings2  # Different list objects


# String representation
def test_customer_str_no_ratings():
    """Should include customer info in string with no ratings."""
    customer = Customer("Alice", "alice@example.com", budget_range=2)
    result = str(customer)
    assert "Alice" in result
    assert "alice@example.com" in result
    assert "2/4" in result
    assert "0" in result  # 0 ratings


def test_customer_str_with_ratings():
    """Should include rating count in string."""
    customer = Customer("Alice", "alice@example.com")
    restaurant1 = Restaurant("Place 1", "Italian", "123 Main", 3)
    restaurant2 = Restaurant("Place 2", "French", "456 Oak", 2)
    customer.submit_rating(restaurant1, 4)
    customer.submit_rating(restaurant2, 5)

    result = str(customer)
    assert "Alice" in result
    assert "2" in result  # 2 ratings submitted


def test_customer_repr():
    """Should return detailed repr for debugging."""
    customer = Customer("Alice", "alice@example.com", ["Italian"], 3)
    result = repr(customer)
    assert "Customer" in result
    assert "Alice" in result
    assert "alice@example.com" in result
    assert "Italian" in result
