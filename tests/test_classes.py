import pytest
from src.classes import Product, Category


@pytest.fixture
def sample_products():
    return [
        Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет", 180000.0, 5),
        Product("Iphone 15", "512GB, Gray space", 210000.0, 8),
        Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    ]


@pytest.fixture
def smartphone_category(sample_products):
    return Category(
        "Смартфоны",
        "Смартфоны для удобства жизни",
        sample_products
    )


# --- Автоматическая фикстура для сброса глобального состояния ---
@pytest.fixture(autouse=True)
def reset_class_counters():
    """
    Автоматически сбрасывает глобальные счетчики класса Category перед каждым тестом.
    """
    Category.category_count = 0
    Category.product_count = 0
    yield


# Тесты для класса Product
def test_product_initialization():
    """Проверяет корректность инициализации объекта Product."""
    name = "Тестовый товар"
    description = "Описание товара"
    price = 999.99
    quantity = 10

    product = Product(name, description, price, quantity)

    assert product.name == name
    assert product.description == description
    assert product.price == price
    assert product.quantity == quantity


# Тесты для класса Category
def test_category_initialization(smartphone_category):
    """Проверяет корректность инициализации объекта Category."""
    assert smartphone_category.name == "Смартфоны"
    assert smartphone_category.description == "Смартфоны для удобства жизни"
    assert isinstance(smartphone_category.products, list)
    assert len(smartphone_category.products) == 3


def test_multiple_categories_and_products():
    """Проверяет подсчет при создании нескольких категорий."""

    tv_product = Product("55\" QLED", "4K", 123000.0, 7)

    category_tv = Category("Телевизоры", "Помощник", [tv_product])

    category_phone = Category("Смартфоны", "Для связи", [
        Product("A1", "", 1.0, 1),
        Product("A2", "", 2.0, 2)
    ])

    # Итого: создано 2 категории и добавлено 1 + 2 = 3 продукта.

    assert Category.category_count == 2
    assert Category.product_count == 3
