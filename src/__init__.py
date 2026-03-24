"""Restaurant Rating System — OOP assessment project."""

from src.customer import Customer
from src.exceptions import (
    DuplicateRatingError,
    InvalidEmailError,
    InvalidRatingError,
    ValidationError,
)
from src.rating import Rating
from src.restaurant import MenuItem, Restaurant
from src.validation import (
    validate_email,
    validate_non_empty_string,
    validate_non_negative,
    validate_price_range,
    validate_rating_score,
)

__all__ = [
    # Exceptions
    "ValidationError",
    "InvalidRatingError",
    "DuplicateRatingError",
    "InvalidEmailError",
    # Domain models
    "Restaurant",
    "MenuItem",
    "Customer",
    "Rating",
    # Validation
    "validate_non_empty_string",
    "validate_email",
    "validate_rating_score",
    "validate_price_range",
    "validate_non_negative",
]
