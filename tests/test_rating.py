"""Tests for Rating class."""

import pytest
from datetime import datetime

from src.rating import Rating
from src.customer import Customer
from src.restaurant import Restaurant


# Rating creation
def test_rating_creation():
    """Should create a Rating with valid data."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    rating = Rating(customer, restaurant, 4, "Great food!")
    assert rating.customer == customer
    assert rating.restaurant == restaurant
    assert rating.score == 4
    assert rating.review_text == "Great food!"


def test_rating_default_review_text():
    """Should default review_text to empty string."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    rating = Rating(customer, restaurant, 4)
    assert rating.review_text == ""


def test_rating_all_valid_scores():
    """Should accept scores 1-5."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    for score in range(1, 6):
        rating = Rating(customer, restaurant, score)
        assert rating.score == score


def test_rating_invalid_score_zero():
    """Should raise InvalidRatingError for score 0."""
    from src.exceptions import InvalidRatingError

    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    with pytest.raises(InvalidRatingError):
        Rating(customer, restaurant, 0)


def test_rating_invalid_score_six():
    """Should raise InvalidRatingError for score 6."""
    from src.exceptions import InvalidRatingError

    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    with pytest.raises(InvalidRatingError):
        Rating(customer, restaurant, 6)


def test_rating_invalid_score_negative():
    """Should raise InvalidRatingError for negative score."""
    from src.exceptions import InvalidRatingError

    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    with pytest.raises(InvalidRatingError):
        Rating(customer, restaurant, -1)


# Timestamp behavior
def test_rating_timestamp_created():
    """Should create timestamp on instantiation."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    before = datetime.now()
    rating = Rating(customer, restaurant, 4)
    after = datetime.now()

    assert hasattr(rating, "timestamp")
    assert before <= rating.timestamp <= after


def test_rating_timestamp_is_datetime():
    """Should store timestamp as datetime object."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    rating = Rating(customer, restaurant, 4)
    assert isinstance(rating.timestamp, datetime)


# Positive rating detection
def test_is_positive_score_five():
    """Score 5 should be positive."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)
    rating = Rating(customer, restaurant, 5)
    assert rating.is_positive() is True


def test_is_positive_score_four():
    """Score 4 should be positive (boundary)."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)
    rating = Rating(customer, restaurant, 4)
    assert rating.is_positive() is True


def test_is_positive_score_three():
    """Score 3 should be negative."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)
    rating = Rating(customer, restaurant, 3)
    assert rating.is_positive() is False


def test_is_positive_score_two():
    """Score 2 should be negative."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)
    rating = Rating(customer, restaurant, 2)
    assert rating.is_positive() is False


def test_is_positive_score_one():
    """Score 1 should be negative."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)
    rating = Rating(customer, restaurant, 1)
    assert rating.is_positive() is False


# String representation
def test_rating_str_with_review():
    """Should include score and review in string."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)
    rating = Rating(customer, restaurant, 4, "Great food!")

    result = str(rating)
    assert "4" in result
    assert "Great food!" in result


def test_rating_str_without_review():
    """Should handle empty review text in string."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)
    rating = Rating(customer, restaurant, 4)

    result = str(rating)
    assert "4" in result
    assert "Alice" in result or "The Place" in result


def test_rating_str_all_scores():
    """Should work for all valid scores."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)

    for score in range(1, 6):
        rating = Rating(customer, restaurant, score)
        result = str(rating)
        assert str(score) in result


def test_rating_repr():
    """Should return detailed repr for debugging."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)
    rating = Rating(customer, restaurant, 4, "Great!")

    result = repr(rating)
    assert "Rating" in result
    assert "4" in result


def test_rating_review_text_can_be_long():
    """Should handle long review text."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)
    long_review = "A" * 500

    rating = Rating(customer, restaurant, 4, long_review)
    assert rating.review_text == long_review


def test_rating_review_text_can_have_special_chars():
    """Should handle special characters in review."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)
    review = "Amazing! @#$%^&*() Love it!!"

    rating = Rating(customer, restaurant, 5, review)
    assert rating.review_text == review


def test_rating_review_text_can_be_multiline():
    """Should handle multiline review text."""
    customer = Customer("Alice", "alice@example.com")
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)
    review = "Line 1\nLine 2\nLine 3"

    rating = Rating(customer, restaurant, 4, review)
    assert rating.review_text == review
