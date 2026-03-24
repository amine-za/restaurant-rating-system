"""Rating class for restaurant reviews."""

from datetime import datetime
from typing import TYPE_CHECKING

from src.validation import validate_rating_score

if TYPE_CHECKING:
    from src.customer import Customer
    from src.restaurant import Restaurant


class Rating:
    """Represents a customer's rating and review of a restaurant."""

    def __init__(
        self,
        customer: "Customer",
        restaurant: "Restaurant",
        score: int,
        review_text: str = "",
    ) -> None:
        self.customer = customer
        self.restaurant = restaurant
        self.score = validate_rating_score(score)
        self.review_text = review_text
        self.timestamp = datetime.now()

    def is_positive(self) -> bool:
        return self.score >= 4

    def __str__(self) -> str:
        """Return a readable string representation of the rating."""
        customer_name = self.customer.name
        restaurant_name = self.restaurant.name
        return (
            f"{customer_name} rated {restaurant_name} "
            f"{self.score}/5 on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
        )

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return (
            f"Rating(customer={self.customer.name!r}, "
            f"restaurant={self.restaurant.name!r}, score={self.score}, "
            f"timestamp={self.timestamp!r})"
        )
