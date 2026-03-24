# Restaurant Rating System

An OOP assessment project modeling a restaurant recommendation and rating system.

## Setup

```bash
pip install -r requirements.txt
```

## Running Tests

```bash
pytest                    # all tests
pytest --cov=src          # with coverage
pytest -v                 # verbose
```

## Running the Demo

```bash
python main.py
```

## Structure

```
src/
├── __init__.py
├── restaurant.py      # Restaurant, MenuItem
├── customer.py        # Customer
├── rating.py          # Rating
├── recommendation.py   # RecommendationEngine
├── manager.py         # RestaurantManager
└── exceptions.py      # ValidationError, etc.

tests/
├── __init__.py
├── test_restaurant.py
├── test_customer.py
├── test_rating.py
├── test_recommendation.py
├── test_manager.py
└── test_integration.py
```

## Core Classes

- **Restaurant** — name, cuisine_type, address, price_range (1–4), menu items, ratings
- **MenuItem** — name, description, price, category
- **Customer** — name, email, preferred_cuisines, budget_range (1–4), submitted ratings
- **Rating** — customer, restaurant, score (1–5), review_text, timestamp
- **RecommendationEngine** — ranks restaurants by cuisine match, price, and ratings
- **RestaurantManager** — coordinates restaurants, customers, and ratings

## Key Rules

- Names, cuisine types, addresses cannot be empty
- Email must be valid
- Price ranges: 1–4
- Rating scores: 1–5
- Same customer cannot rate the same restaurant twice
- Empty rating list returns average of 0

## License

See LICENSE.
