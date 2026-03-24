"""Tests for Customer class."""

import pytest

from src.customer import Customer
from src.exceptions import DuplicateRatingError
from src.restaurant import Restaurant


def test_customer_creation():
    """Should create a Customer with valid data."""
    customer = Customer("Alice", "alice@example.com", ["Italian"], 3)
    assert customer.name == "Alice"
    assert customer.email == "alice@example.com"
    assert customer.preferred_cuisines == ["Italian"]
    assert customer.budget_range == 3


def test_customer_invalid_email():
    """Should raise InvalidEmailError for invalid email."""
    from src.exceptions import InvalidEmailError

    with pytest.raises(InvalidEmailError):
        Customer("Alice", "not-an-email", [], 3)


def test_customer_invalid_budget():
    """Should raise ValidationError for invalid budget_range."""
    from src.exceptions import ValidationError

    with pytest.raises(ValidationError):
        Customer("Alice", "alice@example.com", [], 5)


def test_submit_rating():
    """Should submit a rating for a restaurant."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    rating = customer.submit_rating(restaurant, 4, "Great food!")
    assert rating.customer == customer
    assert rating.restaurant == restaurant
    assert rating.score == 4


def test_duplicate_rating_prevention():
    """Should prevent same customer from rating same restaurant twice."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    customer.submit_rating(restaurant, 4)
    with pytest.raises(DuplicateRatingError):
        customer.submit_rating(restaurant, 5)


def test_get_ratings_submitted():
    """Should return list of all ratings submitted by customer."""
    customer = Customer("Alice", "alice@example.com")
    restaurant1 = Restaurant("Place 1", "Italian", "123 Main", 3)
    restaurant2 = Restaurant("Place 2", "French", "456 Oak", 2)

    customer.submit_rating(restaurant1, 4)
    customer.submit_rating(restaurant2, 5)
    ratings = customer.get_ratings_submitted()
    assert len(ratings) == 2


def test_customer_str():
    """Should return readable string representation."""
    customer = Customer("Alice", "alice@example.com", budget_range=2)
    result = str(customer)
    assert "Alice" in result
    assert "alice@example.com" in result
    assert "2/4" in result
