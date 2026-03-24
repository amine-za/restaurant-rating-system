"""Tests for Rating class."""

import pytest

from src.customer import Customer
from src.exceptions import InvalidRatingError
from src.rating import Rating
from src.restaurant import Restaurant


def test_rating_creation():
    """Should create a Rating with valid data."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    rating = Rating(customer, restaurant, 4, "Amazing!")
    assert rating.customer == customer
    assert rating.restaurant == restaurant
    assert rating.score == 4
    assert rating.review_text == "Amazing!"


def test_rating_invalid_score():
    """Should raise InvalidRatingError for invalid score."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    with pytest.raises(InvalidRatingError):
        Rating(customer, restaurant, 6)


def test_rating_is_positive_true():
    """Should return True for positive ratings (score >= 4)."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    rating_4 = Rating(customer, restaurant, 4)
    rating_5 = Rating(customer, restaurant, 5)

    assert rating_4.is_positive() is True
    assert rating_5.is_positive() is True


def test_rating_is_positive_false():
    """Should return False for non-positive ratings (score < 4)."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    rating_1 = Rating(customer, restaurant, 1)
    rating_3 = Rating(customer, restaurant, 3)

    assert rating_1.is_positive() is False
    assert rating_3.is_positive() is False


def test_rating_str():
    """Should return readable string representation."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    rating = Rating(customer, restaurant, 4)
    result = str(rating)
    assert "Alice" in result
    assert "The Place" in result
    assert "4/5" in result


def test_rating_timestamp():
    """Should have a timestamp when created."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    rating = Rating(customer, restaurant, 4)
    assert rating.timestamp is not None
    assert hasattr(rating.timestamp, "year")
