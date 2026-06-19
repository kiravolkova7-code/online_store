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


# Новые тесты по домашке 14-2

# Тесты для класса Product
def test_product_new_product_success():
    """
    Проверяет создание продукта через класс-метод new_product.
    """
    product_data = {
        "name": "Test Phone",
        "description": "A phone for testing.",
        "price": 15000.0,
        "quantity": 10
    }
    product = Product.new_product(product_data)

    assert isinstance(product, Product)
    assert product.name == "Test Phone"
    assert product.price == 15000.0


def test_product_price_setter_valid_value():
    """
    Проверяет установку корректной цены через сеттер.
    """
    product = Product("Name", "Desc", 100.0, 1)
    product.price = 250.5

    assert product.price == 250.5


def test_product_price_setter_invalid_value():
    """
    Проверяет, что при попытке установить некорректную цену (<= 0),
    внутренняя цена НЕ изменяется.
    """
    original_price = 300.0
    product = Product("Name", "Desc", original_price, 1)

    product.price = -50
    assert product.price == original_price, "Цена не должна была измениться"

    # Повторим проверку для нуля
    product.price = 0
    assert product.price == original_price, "Цена не должна была измениться и при установке в ноль"


# Тесты для класса Category

def test_category_add_product_success():
    """
    Проверяет успешное добавление товара в категорию.
    """
    category = Category("Electronics", "Gadgets")
    product = Product("Laptop", "Notebook", 60000.0, 3)

    initial_count = len(category.products)
    category.add_product(product)
    final_count = len(category.products)

    assert final_count == initial_count + 1
    assert product in category.products


def test_category_add_product_wrong_type():
    """
    Проверяет, что ValueError возникает при добавлении неверного типа.
    """
    category = Category("Books", "Novels and textbooks")

    with pytest.raises(ValueError) as exc_info:
        category.add_product("Not a product object")

    assert str(exc_info.value) == "Можно добавить только объект класса Product"


def test_category_products_getter():
    """
    Проверяет, что геттер products возвращает правильный список.
    """
    product = Product("Book", "Fantasy", 500.0, 1)
    category = Category("Books", "Stories", [product])

    retrieved_list = category.products

    assert isinstance(retrieved_list, list)
    assert len(retrieved_list) == 1
    assert retrieved_list[0] is product


def test_category_get_products_formatting():
    """
    Проверяет форматирование строк в методе get_products.
    """
    product = Product("Книга", "Фэнтези", 499.99, 5)
    category = Category("Книги", "Истории", [product])

    formatted_list = category.get_products()
    expected_string = f"{product.name}, {product.price:.2f} руб. Остаток: {product.quantity} шт."

    assert formatted_list[0] == expected_string
