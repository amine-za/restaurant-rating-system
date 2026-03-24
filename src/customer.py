"""Customer class for the rating system."""

from typing import TYPE_CHECKING, List

from src.validation import validate_email, validate_non_empty_string, validate_price_range

if TYPE_CHECKING:
    from src.rating import Rating
    from src.restaurant import Restaurant


class Customer:
    """Represents a restaurant customer with preferences and ratings."""

    def __init__(
        self,
        name: str,
        email: str,
        preferred_cuisines: List[str] | None = None,
        budget_range: int = 2,
    ) -> None:
        self.name = validate_non_empty_string(name, "Customer name")
        self.email = validate_email(email)
        self.preferred_cuisines = preferred_cuisines if preferred_cuisines is not None else []
        self.budget_range = validate_price_range(budget_range)

        self._ratings_submitted: List["Rating"] = []

    def submit_rating(
        self, restaurant: "Restaurant", score: int, review_text: str = ""
    ) -> "Rating":
        # Avoid circular import at module level
        from src.rating import Rating

        # Check for duplicate rating
        for rating in self._ratings_submitted:
            if rating.restaurant == restaurant:
                from src.exceptions import DuplicateRatingError

                raise DuplicateRatingError(
                    f"{self.name} has already rated {restaurant.name}"
                )

        # Create and store the rating
        rating = Rating(self, restaurant, score, review_text)
        self._ratings_submitted.append(rating)

        # Add rating to restaurant
        restaurant.add_rating({"score": score, "customer": self})

        return rating

    def get_ratings_submitted(self) -> List["Rating"]:
        return list(self._ratings_submitted)

    def __str__(self) -> str:
        """Return a readable string representation of the customer."""
        ratings_count = len(self._ratings_submitted)
        return (
            f"{self.name} ({self.email}) - Budget: {self.budget_range}/4, "
            f"Ratings submitted: {ratings_count}"
        )

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return (
            f"Customer(name={self.name!r}, email={self.email!r}, "
            f"budget_range={self.budget_range}, "
            f"preferred_cuisines={self.preferred_cuisines})"
        )
