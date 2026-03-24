"""Custom exceptions for the Restaurant Rating System."""


class ValidationError(Exception):
    """Base exception for validation errors."""

    pass


class InvalidRatingError(ValidationError):
    """Raised when a rating score or related data is invalid."""

    pass


class DuplicateRatingError(ValidationError):
    """Raised when a customer attempts to rate the same restaurant twice."""

    pass


class InvalidEmailError(ValidationError):
    """Raised when an email address format is invalid."""

    pass
