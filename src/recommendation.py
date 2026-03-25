"""RecommendationEngine for suggesting restaurants to customers."""

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.customer import Customer
    from src.restaurant import Restaurant


class RecommendationEngine:
    """Stateless engine for recommending restaurants based on customer preferences."""

    @staticmethod
    def filter_by_cuisine(restaurants: List["Restaurant"], cuisine_type: str) -> List["Restaurant"]:
        """
        Filter restaurants by cuisine type.

        Args:
            restaurants: List of restaurants to filter
            cuisine_type: Target cuisine type (case-sensitive)

        Returns:
            List of restaurants matching the cuisine type
        """
        return [r for r in restaurants if r.cuisine_type == cuisine_type]

    @staticmethod
    def filter_by_price_range(
        restaurants: List["Restaurant"], max_price: int
    ) -> List["Restaurant"]:
        """
        Filter restaurants by maximum price range.

        Args:
            restaurants: List of restaurants to filter
            max_price: Maximum price range (1-4 scale)

        Returns:
            List of restaurants with price_range <= max_price
        """
        return [r for r in restaurants if r.price_range <= max_price]

    @staticmethod
    def sort_by_rating(restaurants: List["Restaurant"]) -> List["Restaurant"]:
        """
        Sort restaurants by average rating (descending), then by rating count.

        Args:
            restaurants: List of restaurants to sort

        Returns:
            Sorted list with highest-rated restaurants first
        """
        return sorted(
            restaurants,
            key=lambda r: (r.get_average_rating(), r.get_rating_count()),
            reverse=True,
        )

    @staticmethod
    def recommend_for_customer(
        customer: "Customer", all_restaurants: List["Restaurant"]
    ) -> List["Restaurant"]:
        """
        Recommend restaurants for a customer based on preferences and budget.

        Ranking factors (in order of importance):
        1. Cuisine preference match (whether restaurant cuisine is in customer's preferences)
        2. Average rating (quality of past customer reviews, 0-5)
        3. Budget compatibility (whether price_range <= customer's budget_range)
        4. Number of ratings (confidence/popularity)
        5. Restaurant name (tiebreaker for deterministic ordering)

        Args:
            customer: Customer object with preferences and budget
            all_restaurants: All available restaurants

        Returns:
            Sorted list of recommendations (best match first)
        """
        if not all_restaurants:
            return []

        # Score each restaurant using a tuple for deterministic sorting
        scored_restaurants = []

        for restaurant in all_restaurants:
            # Boolean scores (True=1, False=0 in tuple sorting)
            cuisine_match = restaurant.cuisine_type in customer.preferred_cuisines
            budget_match = restaurant.price_range <= customer.budget_range

            # Numeric scores
            avg_rating = restaurant.get_average_rating()
            rating_count = restaurant.get_rating_count()

            # Create scoring tuple (higher values = better match)
            # Priority: cuisine > rating > budget > count > name
            score_tuple = (
                cuisine_match,
                avg_rating,
                budget_match,
                rating_count,
                restaurant.name,
            )

            scored_restaurants.append((score_tuple, restaurant))

        # Sort by score tuple (descending)
        scored_restaurants.sort(reverse=True)

        # Return just the restaurants
        return [restaurant for _, restaurant in scored_restaurants]
