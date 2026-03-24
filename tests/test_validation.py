"""Tests for exceptions and validation helpers."""

import pytest

from src.exceptions import (
    DuplicateRatingError,
    InvalidEmailError,
    InvalidRatingError,
    ValidationError,
)
from src.validation import (
    validate_email,
    validate_non_empty_string,
    validate_non_negative,
    validate_price_range,
    validate_rating_score,
)

# Validation helpers
def test_validate_non_empty_string_valid():
    result = validate_non_empty_string("hello", "Name")
    assert result == "hello"


def test_validate_non_empty_string_invalid():
    with pytest.raises(ValidationError):
        validate_non_empty_string("", "Name")


def test_validate_email_valid():
    result = validate_email("user@example.com")
    assert result == "user@example.com"


def test_validate_email_invalid():
    with pytest.raises(InvalidEmailError):
        validate_email("notanemail")


def test_validate_rating_score_valid():
    """Should accept score between 1 and 5."""
    result = validate_rating_score(3)
    assert result == 3


def test_validate_rating_score_invalid():
    """Should raise InvalidRatingError for score outside 1–5."""
    with pytest.raises(InvalidRatingError):
        validate_rating_score(6)


def test_validate_price_range_valid():
    """Should accept price range between 1 and 4."""
    result = validate_price_range(2)
    assert result == 2


def test_validate_price_range_invalid():
    """Should raise ValidationError for price outside 1–4."""
    with pytest.raises(ValidationError):
        validate_price_range(5)


def test_validate_non_negative_valid():
    """Should accept non-negative numbers."""
    result = validate_non_negative(10.50, "Price")
    assert result == 10.50


def test_validate_non_negative_invalid():
    """Should raise ValidationError for negative number."""
    with pytest.raises(ValidationError):
        validate_non_negative(-5, "Price")


# Exception hierarchy
def test_invalid_rating_error_inherits_from_validation_error():
    """InvalidRatingError should inherit from ValidationError."""
    assert issubclass(InvalidRatingError, ValidationError)


def test_duplicate_rating_error_inherits_from_validation_error():
    """DuplicateRatingError should inherit from ValidationError."""
    assert issubclass(DuplicateRatingError, ValidationError)


def test_invalid_email_error_inherits_from_validation_error():
    """InvalidEmailError should inherit from ValidationError."""
    assert issubclass(InvalidEmailError, ValidationError)
