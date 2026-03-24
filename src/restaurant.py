from typing import List

from src.validation import (
    validate_non_empty_string,
    validate_non_negative,
    validate_price_range,
)


class MenuItem:
    VALID_CATEGORIES = {"appetizer", "main", "dessert", "drink"}

    def __init__(
        self, name: str, description: str, price: float, category: str
    ) -> None:
        self.name = validate_non_empty_string(name, "MenuItem name")
        self.description = description
        self.price = validate_non_negative(price, "MenuItem price")

        if category not in self.VALID_CATEGORIES:
            raise ValueError(
                f"Invalid category: {category}. "
                f"Must be one of {self.VALID_CATEGORIES}."
            )
        self.category = category

    def __str__(self) -> str:
        """Return a readable string representation of the menu item."""
        return f"{self.name} ({self.category}) - ${self.price:.2f}"

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return (
            f"MenuItem(name={self.name!r}, category={self.category}, "
            f"price={self.price}, description={self.description!r})"
        )


class Restaurant:
    def __init__(
        self, name: str, cuisine_type: str, address: str, price_range: int
    ) -> None:
        self.name = validate_non_empty_string(name, "Restaurant name")
        self.cuisine_type = validate_non_empty_string(cuisine_type, "Cuisine type")
        self.address = validate_non_empty_string(address, "Address")
        self.price_range = validate_price_range(price_range)

        self._menu: List[MenuItem] = []
        self._ratings: List[dict] = []

    def add_menu_item(self, item: MenuItem) -> None:
        if not isinstance(item, MenuItem):
            raise TypeError("Item must be a MenuItem instance.")
        self._menu.append(item)

    def get_menu(self) -> List[MenuItem]:
        return list(self._menu)

    def add_rating(self, rating: dict) -> None:
        self._ratings.append(rating)

    def get_rating_count(self) -> int:
        return len(self._ratings)

    def get_average_rating(self) -> float:
        if not self._ratings:
            return 0.0

        total = sum(rating.get("score", 0) for rating in self._ratings)
        return total / len(self._ratings)

    def __str__(self) -> str:
        """Return a readable string representation of the restaurant."""
        avg_rating = self.get_average_rating()
        rating_count = self.get_rating_count()
        return (
            f"{self.name} ({self.cuisine_type}) - {self.address} "
            f"(Price: {self.price_range}/4, Rating: {avg_rating:.1f}/5 "
            f"from {rating_count} reviews)"
        )

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging."""
        return (
            f"Restaurant(name={self.name!r}, cuisine_type={self.cuisine_type!r}, "
            f"address={self.address!r}, price_range={self.price_range}, "
            f"menu_items={len(self._menu)}, ratings={len(self._ratings)})"
        )
