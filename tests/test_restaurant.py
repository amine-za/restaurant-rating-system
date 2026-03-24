"""Tests for Restaurant and MenuItem classes."""

import pytest

from src.exceptions import ValidationError
from src.restaurant import MenuItem, Restaurant


# MenuItem tests
def test_menu_item_creation():
    """Should create a MenuItem with valid data."""
    item = MenuItem("Pasta", "Creamy pasta", 12.99, "main")
    assert item.name == "Pasta"
    assert item.price == 12.99
    assert item.category == "main"


def test_menu_item_invalid_category():
    """Should raise ValueError for invalid category."""
    with pytest.raises(ValueError):
        MenuItem("Item", "Desc", 5.0, "invalid")


def test_menu_item_str():
    """Should return readable string representation."""
    item = MenuItem("Pasta", "Creamy pasta", 12.99, "main")
    result = str(item)
    assert "Pasta" in result
    assert "main" in result
    assert "$12.99" in result


# Restaurant tests
def test_restaurant_creation():
    """Should create a Restaurant with valid data."""
    restaurant = Restaurant("The Italian Place", "Italian", "123 Main St", 3)
    assert restaurant.name == "The Italian Place"
    assert restaurant.cuisine_type == "Italian"
    assert restaurant.address == "123 Main St"
    assert restaurant.price_range == 3


def test_restaurant_invalid_price_range():
    """Should raise ValidationError for invalid price range."""
    with pytest.raises(ValidationError):
        Restaurant("Place", "Italian", "123 Main St", 5)


def test_add_menu_item():
    """Should add a MenuItem to the restaurant."""
    restaurant = Restaurant("Place", "Italian", "123 Main St", 3)
    item = MenuItem("Pasta", "Desc", 12.99, "main")
    restaurant.add_menu_item(item)
    menu = restaurant.get_menu()
    assert len(menu) == 1
    assert menu[0] == item


def test_add_menu_item_invalid_type():
    """Should raise TypeError if item is not a MenuItem."""
    restaurant = Restaurant("Place", "Italian", "123 Main St", 3)
    with pytest.raises(TypeError):
        restaurant.add_menu_item("not a menu item")


def test_rating_count_and_average():
    """Should calculate rating count and average correctly."""
    restaurant = Restaurant("Place", "Italian", "123 Main St", 3)
    assert restaurant.get_rating_count() == 0
    assert restaurant.get_average_rating() == 0.0

    restaurant.add_rating({"score": 3})
    restaurant.add_rating({"score": 5})
    assert restaurant.get_rating_count() == 2
    assert restaurant.get_average_rating() == 4.0


def test_restaurant_str():
    """Should return readable string representation."""
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)
    restaurant.add_rating({"score": 4})
    restaurant.add_rating({"score": 5})
    result = str(restaurant)
    assert "The Place" in result
    assert "Italian" in result
    assert "4.5" in result
