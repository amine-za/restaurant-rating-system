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


def test_menu_item_valid_categories():
    """Should accept all valid categories."""
    for category in ["appetizer", "main", "dessert", "drink"]:
        item = MenuItem("Item", "Desc", 5.0, category)
        assert item.category == category


def test_menu_item_invalid_category():
    """Should raise ValueError for invalid category."""
    with pytest.raises(ValueError):
        MenuItem("Item", "Desc", 5.0, "invalid")


def test_menu_item_zero_price():
    """Should accept zero price."""
    item = MenuItem("Free Item", "Desc", 0.0, "main")
    assert item.price == 0.0


def test_menu_item_empty_description():
    """Should accept empty description."""
    item = MenuItem("Item", "", 5.0, "main")
    assert item.description == ""


def test_menu_item_str():
    """Should return readable string representation."""
    item = MenuItem("Pasta", "Creamy pasta", 12.99, "main")
    result = str(item)
    assert "Pasta" in result
    assert "main" in result
    assert "$12.99" in result


def test_menu_item_repr():
    """Should return detailed repr for debugging."""
    item = MenuItem("Pasta", "Desc", 12.99, "main")
    result = repr(item)
    assert "MenuItem" in result
    assert "Pasta" in result


# Restaurant tests
def test_restaurant_creation():
    """Should create a Restaurant with valid data."""
    restaurant = Restaurant("The Italian Place", "Italian", "123 Main St", 3)
    assert restaurant.name == "The Italian Place"
    assert restaurant.cuisine_type == "Italian"
    assert restaurant.address == "123 Main St"
    assert restaurant.price_range == 3


def test_restaurant_all_price_ranges():
    """Should accept price ranges 1-4."""
    for price in range(1, 5):
        r = Restaurant("Place", "Italian", "123 Main St", price)
        assert r.price_range == price


def test_restaurant_invalid_price_range_zero():
    """Should raise ValidationError for price range 0."""
    with pytest.raises(ValidationError):
        Restaurant("Place", "Italian", "123 Main St", 0)


def test_restaurant_invalid_price_range_five():
    """Should raise ValidationError for price range > 4."""
    with pytest.raises(ValidationError):
        Restaurant("Place", "Italian", "123 Main St", 5)


def test_restaurant_whitespace_names_trimmed():
    """Should trim whitespace from name, cuisine, address."""
    r = Restaurant("  Italian Place  ", "  Italian  ", "  123 Main St  ", 3)
    assert r.name == "Italian Place"
    assert r.cuisine_type == "Italian"
    assert r.address == "123 Main St"


def test_add_menu_item():
    """Should add a MenuItem to the restaurant."""
    restaurant = Restaurant("Place", "Italian", "123 Main St", 3)
    item = MenuItem("Pasta", "Desc", 12.99, "main")
    restaurant.add_menu_item(item)
    menu = restaurant.get_menu()
    assert len(menu) == 1
    assert menu[0] == item


def test_add_multiple_menu_items():
    """Should add multiple menu items."""
    restaurant = Restaurant("Place", "Italian", "123 Main St", 3)
    item1 = MenuItem("Pasta", "Desc", 12.99, "main")
    item2 = MenuItem("Tiramisu", "Desc", 8.99, "dessert")
    item3 = MenuItem("Wine", "Desc", 25.0, "drink")

    restaurant.add_menu_item(item1)
    restaurant.add_menu_item(item2)
    restaurant.add_menu_item(item3)

    menu = restaurant.get_menu()
    assert len(menu) == 3


def test_get_menu_returns_copy():
    """Should return a copy of menu, not the original list."""
    restaurant = Restaurant("Place", "Italian", "123 Main St", 3)
    item = MenuItem("Pasta", "Desc", 12.99, "main")
    restaurant.add_menu_item(item)

    menu1 = restaurant.get_menu()
    menu2 = restaurant.get_menu()
    assert menu1 == menu2
    assert menu1 is not menu2  # Different list objects


def test_add_menu_item_invalid_type():
    """Should raise TypeError if item is not a MenuItem."""
    restaurant = Restaurant("Place", "Italian", "123 Main St", 3)
    with pytest.raises(TypeError):
        restaurant.add_menu_item("not a menu item")


def test_rating_count_no_ratings():
    """Should return 0 rating count with no ratings."""
    restaurant = Restaurant("Place", "Italian", "123 Main St", 3)
    assert restaurant.get_rating_count() == 0


def test_average_rating_no_ratings():
    """Should return 0.0 average with no ratings."""
    restaurant = Restaurant("Place", "Italian", "123 Main St", 3)
    assert restaurant.get_average_rating() == 0.0


def test_average_rating_single_rating():
    """Should correctly calculate average with one rating."""
    restaurant = Restaurant("Place", "Italian", "123 Main St", 3)
    restaurant.add_rating({"score": 4})
    assert restaurant.get_rating_count() == 1
    assert restaurant.get_average_rating() == 4.0


def test_average_rating_multiple_ratings():
    """Should correctly calculate average with multiple ratings."""
    restaurant = Restaurant("Place", "Italian", "123 Main St", 3)
    restaurant.add_rating({"score": 3})
    restaurant.add_rating({"score": 5})
    restaurant.add_rating({"score": 4})
    assert restaurant.get_rating_count() == 3
    assert restaurant.get_average_rating() == 4.0


def test_average_rating_all_ones():
    """Should calculate average correctly for all low ratings."""
    restaurant = Restaurant("Place", "Italian", "123 Main St", 3)
    for _ in range(5):
        restaurant.add_rating({"score": 1})
    assert restaurant.get_average_rating() == 1.0


def test_average_rating_all_fives():
    """Should calculate average correctly for all high ratings."""
    restaurant = Restaurant("Place", "Italian", "123 Main St", 3)
    for _ in range(5):
        restaurant.add_rating({"score": 5})
    assert restaurant.get_average_rating() == 5.0


def test_average_rating_fractional():
    """Should handle fractional averages."""
    restaurant = Restaurant("Place", "Italian", "123 Main St", 3)
    restaurant.add_rating({"score": 2})
    restaurant.add_rating({"score": 3})
    assert restaurant.get_average_rating() == 2.5


def test_restaurant_str_no_ratings():
    """Should include restaurant info in string with no ratings."""
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)
    result = str(restaurant)
    assert "The Place" in result
    assert "Italian" in result
    assert "0.0" in result


def test_restaurant_str_with_ratings():
    """Should include rating info in string with ratings."""
    restaurant = Restaurant("The Place", "Italian", "123 Main St", 3)
    restaurant.add_rating({"score": 4})
    restaurant.add_rating({"score": 5})
    result = str(restaurant)
    assert "The Place" in result
    assert "Italian" in result
    assert "4.5" in result


def test_restaurant_repr():
    """Should return detailed repr for debugging."""
    restaurant = Restaurant("Place", "Italian", "123 Main St", 3)
    result = repr(restaurant)
    assert "Restaurant" in result
    assert "Place" in result
    assert "menu_items=0" in result
    assert "ratings=0" in result
