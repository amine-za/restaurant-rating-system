"""Validation helpers for the Restaurant Rating System."""

import re
from typing import Any

from src.exceptions import InvalidEmailError, InvalidRatingError, ValidationError


def validate_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field_name} cannot be empty or whitespace only.")
    return value.strip()


def validate_email(email: str) -> str:
    email = validate_non_empty_string(email, "Email")

    pattern = r"^[^@]+@[^@]+\.[^@]+$"
    if not re.match(pattern, email):
        raise InvalidEmailError(f"Invalid email format: {email}")

    return email


def validate_rating_score(score: Any) -> int:
    if not isinstance(score, int) or score < 1 or score > 5:
        raise InvalidRatingError(f"Rating score must be an integer between 1 and 5, got {score}.")
    return score


def validate_price_range(price_range: Any) -> int:
    if not isinstance(price_range, int) or price_range < 1 or price_range > 4:
        raise ValidationError(f"Price range must be an integer between 1 and 4, got {price_range}.")
    return price_range


def validate_non_negative(value: Any, field_name: str) -> float:
    if not isinstance(value, (int, float)) or value < 0:
        raise ValidationError(f"{field_name} must be non-negative, got {value}.")
    return value
