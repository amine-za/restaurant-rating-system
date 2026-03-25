"""Tests for RecommendationEngine class."""

import pytest

from src.customer import Customer
from src.recommendation import RecommendationEngine
from src.restaurant import Restaurant


# Filter by cuisine tests
def test_filter_by_cuisine_single_match():
    """Should filter restaurants by cuisine type."""
    italian = Restaurant("Italian Place", "Italian", "123 Main", 3)
    french = Restaurant("French Place", "French", "456 Oak", 2)
    restaurants = [italian, french]

    result = RecommendationEngine.filter_by_cuisine(restaurants, "Italian")
    assert result == [italian]


def test_filter_by_cuisine_multiple_matches():
    """Should return all restaurants matching the cuisine."""
    italian1 = Restaurant("Italian 1", "Italian", "123 Main", 3)
    italian2 = Restaurant("Italian 2", "Italian", "456 Oak", 2)
    french = Restaurant("French Place", "French", "789 Pine", 3)
    restaurants = [italian1, italian2, french]

    result = RecommendationEngine.filter_by_cuisine(restaurants, "Italian")
    assert len(result) == 2
    assert italian1 in result
    assert italian2 in result


def test_filter_by_cuisine_no_matches():
    """Should return empty list if no restaurants match cuisine."""
    italian = Restaurant("Italian Place", "Italian", "123 Main", 3)
    french = Restaurant("French Place", "French", "456 Oak", 2)
    restaurants = [italian, french]

    result = RecommendationEngine.filter_by_cuisine(restaurants, "Japanese")
    assert result == []


def test_filter_by_cuisine_case_sensitive():
    """Should be case-sensitive in matching cuisine."""
    restaurant = Restaurant("Place", "Italian", "123 Main", 3)
    restaurants = [restaurant]

    result = RecommendationEngine.filter_by_cuisine(restaurants, "italian")
    assert result == []


def test_filter_by_cuisine_empty_list():
    """Should handle empty restaurant list."""
    result = RecommendationEngine.filter_by_cuisine([], "Italian")
    assert result == []


# Filter by price range tests
def test_filter_by_price_range_single_match():
    """Should filter restaurants by price range."""
    cheap = Restaurant("Cheap", "Italian", "123 Main", 1)
    expensive = Restaurant("Expensive", "French", "456 Oak", 4)
    restaurants = [cheap, expensive]

    result = RecommendationEngine.filter_by_price_range(restaurants, 2)
    assert result == [cheap]


def test_filter_by_price_range_multiple_matches():
    """Should return all restaurants with price_range <= max."""
    budget = Restaurant("Budget", "Italian", "123 Main", 1)
    mid = Restaurant("Mid", "French", "456 Oak", 2)
    upscale = Restaurant("Upscale", "Japanese", "789 Pine", 3)
    expensive = Restaurant("Expensive", "Spanish", "999 Elm", 4)
    restaurants = [budget, mid, upscale, expensive]

    result = RecommendationEngine.filter_by_price_range(restaurants, 2)
    assert len(result) == 2
    assert budget in result
    assert mid in result


def test_filter_by_price_range_includes_exact_match():
    """Should include restaurants with exactly max_price."""
    restaurant = Restaurant("Place", "Italian", "123 Main", 3)
    restaurants = [restaurant]

    result = RecommendationEngine.filter_by_price_range(restaurants, 3)
    assert result == [restaurant]


def test_filter_by_price_range_no_matches():
    """Should return empty list if no restaurants match budget."""
    expensive = Restaurant("Expensive", "French", "456 Oak", 4)
    restaurants = [expensive]

    result = RecommendationEngine.filter_by_price_range(restaurants, 1)
    assert result == []


def test_filter_by_price_range_empty_list():
    """Should handle empty restaurant list."""
    result = RecommendationEngine.filter_by_price_range([], 3)
    assert result == []


# Sort by rating tests
def test_sort_by_rating_single_restaurant():
    """Should handle sorting single restaurant."""
    restaurant = Restaurant("Place", "Italian", "123 Main", 3)
    restaurant.add_rating({"score": 5})
    restaurants = [restaurant]

    result = RecommendationEngine.sort_by_rating(restaurants)
    assert result == [restaurant]


def test_sort_by_rating_sorts_by_average():
    """Should sort restaurants by average rating (descending)."""
    high_rating = Restaurant("High", "Italian", "123 Main", 3)
    high_rating.add_rating({"score": 5})
    high_rating.add_rating({"score": 5})

    low_rating = Restaurant("Low", "French", "456 Oak", 2)
    low_rating.add_rating({"score": 1})

    restaurants = [low_rating, high_rating]
    result = RecommendationEngine.sort_by_rating(restaurants)
    assert result == [high_rating, low_rating]


def test_sort_by_rating_tiebreak_by_count():
    """Should use rating count as tiebreaker for equal average ratings."""
    same_avg_low_count = Restaurant("Low Count", "Italian", "123 Main", 3)
    same_avg_low_count.add_rating({"score": 3})

    same_avg_high_count = Restaurant("High Count", "French", "456 Oak", 2)
    same_avg_high_count.add_rating({"score": 3})
    same_avg_high_count.add_rating({"score": 3})

    restaurants = [same_avg_low_count, same_avg_high_count]
    result = RecommendationEngine.sort_by_rating(restaurants)
    assert result == [same_avg_high_count, same_avg_low_count]


def test_sort_by_rating_no_ratings():
    """Should handle restaurants with no ratings (average = 0.0)."""
    no_ratings = Restaurant("No Ratings", "Italian", "123 Main", 3)
    with_ratings = Restaurant("With Ratings", "French", "456 Oak", 2)
    with_ratings.add_rating({"score": 4})

    restaurants = [no_ratings, with_ratings]
    result = RecommendationEngine.sort_by_rating(restaurants)
    assert result == [with_ratings, no_ratings]


def test_sort_by_rating_empty_list():
    """Should handle empty restaurant list."""
    result = RecommendationEngine.sort_by_rating([])
    assert result == []


# Recommend for customer tests
def test_recommend_for_customer_no_restaurants():
    """Should return empty list if no restaurants available."""
    customer = Customer("Alice", "alice@example.com", ["Italian"], 3)
    result = RecommendationEngine.recommend_for_customer(customer, [])
    assert result == []


def test_recommend_for_customer_single_restaurant():
    """Should recommend single restaurant."""
    customer = Customer("Alice", "alice@example.com", ["Italian"], 3)
    restaurant = Restaurant("Italian Place", "Italian", "123 Main", 3)

    result = RecommendationEngine.recommend_for_customer(customer, [restaurant])
    assert result == [restaurant]


def test_recommend_for_customer_prioritizes_cuisine():
    """Should prioritize restaurants matching customer's preferred cuisines."""
    customer = Customer("Alice", "alice@example.com", ["Italian"], 3)

    italian = Restaurant("Italian Place", "Italian", "123 Main", 3)
    italian.add_rating({"score": 2})  # Low rating

    french = Restaurant("French Place", "French", "456 Oak", 3)
    french.add_rating({"score": 5})  # High rating

    result = RecommendationEngine.recommend_for_customer(
        customer, [french, italian]
    )
    # Italian should be first despite lower rating (cuisine match is primary)
    assert result[0] == italian


def test_recommend_for_customer_prioritizes_budget():
    """Should prioritize budget compatibility after cuisine."""
    customer = Customer("Alice", "alice@example.com", [], 2)

    affordable = Restaurant("Affordable", "Italian", "123 Main", 2)
    expensive = Restaurant("Expensive", "Italian", "456 Oak", 4)

    result = RecommendationEngine.recommend_for_customer(
        customer, [expensive, affordable]
    )
    # Affordable (matches budget) should come first
    assert result[0] == affordable


def test_recommend_for_customer_considers_rating_and_count():
    """Should consider rating and rating count when other factors are equal."""
    customer = Customer("Alice", "alice@example.com", [], 3)

    low_rating = Restaurant("Low Rating", "Italian", "123 Main", 3)
    low_rating.add_rating({"score": 3})

    high_rating = Restaurant("High Rating", "Italian", "456 Oak", 3)
    high_rating.add_rating({"score": 5})
    high_rating.add_rating({"score": 5})

    result = RecommendationEngine.recommend_for_customer(
        customer, [low_rating, high_rating]
    )
    assert result[0] == high_rating


def test_recommend_for_customer_no_preferences():
    """Should handle customer with no cuisine preferences gracefully."""
    customer = Customer("Alice", "alice@example.com", [], 3)

    italian = Restaurant("Italian", "Italian", "123 Main", 3)
    italian.add_rating({"score": 4})

    french = Restaurant("French", "French", "456 Oak", 3)
    french.add_rating({"score": 4})

    result = RecommendationEngine.recommend_for_customer(
        customer, [italian, french]
    )
    assert len(result) == 2


def test_recommend_for_customer_multiple_cuisines():
    """Should handle customers with multiple preferred cuisines."""
    customer = Customer(
        "Alice", "alice@example.com", ["Italian", "Japanese"], 3
    )

    italian = Restaurant("Italian", "Italian", "123 Main", 3)
    japanese = Restaurant("Japanese", "Japanese", "456 Oak", 3)
    french = Restaurant("French", "French", "789 Pine", 3)

    result = RecommendationEngine.recommend_for_customer(
        customer, [french, italian, japanese]
    )
    # Italian and Japanese should come before French
    assert italian in result[:2]
    assert japanese in result[:2]
    assert french == result[2]


def test_recommend_for_customer_deterministic():
    """Should return deterministic results (same input = same output)."""
    customer = Customer("Alice", "alice@example.com", ["Italian"], 2)

    italian = Restaurant("Italian", "Italian", "123 Main", 2)
    italian.add_rating({"score": 4})

    french = Restaurant("French", "French", "456 Oak", 2)
    french.add_rating({"score": 4})

    restaurants = [italian, french]

    result1 = RecommendationEngine.recommend_for_customer(customer, restaurants)
    result2 = RecommendationEngine.recommend_for_customer(customer, restaurants)

    assert result1 == result2


def test_recommend_for_customer_complete_scenario():
    """Should rank correctly in a mixed scenario."""
    customer = Customer(
        "Alice", "alice@example.com", ["Italian"], 3
    )

    # Italian, affordable, high rating, many reviews
    perfect = Restaurant("Perfect", "Italian", "111 Main", 2)
    perfect.add_rating({"score": 5})
    perfect.add_rating({"score": 5})

    # Italian, affordable, low rating
    decent = Restaurant("Decent", "Italian", "222 Main", 2)
    decent.add_rating({"score": 2})

    # French, affordable, high rating
    other = Restaurant("Other", "French", "333 Main", 2)
    other.add_rating({"score": 5})
    other.add_rating({"score": 5})

    # Italian, expensive, high rating
    fancy = Restaurant("Fancy", "Italian", "444 Main", 4)
    fancy.add_rating({"score": 5})

    restaurants = [decent, other, fancy, perfect]
    result = RecommendationEngine.recommend_for_customer(customer, restaurants)

    # Order: perfect (Italian + affordable + high rating) > fancy (Italian + high rating) >
    # decent (Italian + affordable + low rating) > other (French + no match)
    assert result[0] == perfect
    assert result[1] == fancy
    assert result[2] == decent
    assert result[3] == other
