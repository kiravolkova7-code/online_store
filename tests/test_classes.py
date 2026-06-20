import pytest
from src.classes import Product, Smartphone, LawnGrass, Category


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
    """
    Проверяет подсчет при создании нескольких категорий.
    """
    tv_product = Product("55\" QLED", "4K", 123000.0, 7)

    category_tv = Category("Телевизоры", "Помощник", [tv_product])

    category_phone = Category(
        "Смартфоны",
        "Для связи",
        [
            Product("A1", "", 1.0, 1),   # 1 штука
            Product("A2", "", 2.0, 2)    # 2 штуки
        ]
    )

    assert Category.category_count == 2
    assert Category.product_count == 10


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

    expected_string = f"{product.name}, {product.price:.2f} руб. Остаток: {product.quantity} шт."
    assert expected_string in category.products


def test_category_add_product_wrong_type():
    """
    Проверяет, что при добавлении неверного типа вызывается TypeError.
    """
    category = Category("Books", "Novels and textbooks")
    with pytest.raises(TypeError) as exc_info:
        category.add_product("Not a product object")

    assert str(exc_info.value) == "Можно добавить только объект класса Product или его наследников"


def test_category_products_getter():
    """
    Проверяет, что геттер products возвращает правильный список.
    Геттер теперь возвращает список СТРОК, поэтому и проверка должна быть соответствующей.
    """
    product = Product("Book", "Fantasy", 500.0, 1)
    category = Category("Books", "Stories", [product])

    retrieved_list = category.products

    assert isinstance(retrieved_list, list)
    assert len(retrieved_list) == 1

    expected_string = f"{product.name}, {product.price:.2f} руб. Остаток: {product.quantity} шт."
    assert retrieved_list[0] == expected_string


def test_category_get_products_formatting():
    """
    Проверяет форматирование строк в методе get_products.
    """
    product = Product("Книга", "Фэнтези", 499.99, 5)
    category = Category("Книги", "Истории", [product])

    formatted_list = category.get_products()
    expected_string = f"{product.name}, {product.price:.2f} руб. Остаток: {product.quantity} шт."

    assert formatted_list[0] == expected_string

# Новые тесты по домашке 15-1
# Тесты для класса Product


def test_product_str_representation():
    """Проверяет строковое представление товара (__str__)."""
    product = Product("Товар А", "Описание", 100.50, 10)
    expected_output = "Товар А, 100.50 руб. Остаток: 10 шт."
    assert str(product) == expected_output


def test_add_two_products():
    """Проверяет сложение стоимости двух товаров (__add__)."""
    a = Product("Товар А", "Описание", 100.50, 10)
    b = Product("Товар Б", "Описание", 200.75, 5)

    # Ручной расчет: (100.50 * 10) + (200.75 * 5) = 1005.0 + 1003.75 = 2008.75
    total_cost = a + b
    assert total_cost == 2008.75


def test_add_invalid_type_raises_error():
    """Проверяет, что при сложении с неподдерживаемым типом вызывается TypeError."""
    a = Product("Товар А", "Описание", 100, 10)

    with pytest.raises(TypeError) as error_info:
        result = a + 100

    assert "unsupported operand type(s) for +: 'Product' and 'int'" in str(error_info.value)


# Тесты для класса Category
@pytest.fixture(autouse=True)
def reset_category_count():
    """
    Фикстура, которая сбрасывает статический счетчик перед каждым тестом.
    """
    Category.product_count = 0


def test_category_str_representation_with_products():
    """Проверяет строковое представление категории с товарами."""
    p1 = Product("Телефон", "Хороший", 10000, 2)
    p2 = Product("Ноутбук", "Отличный", 50000, 1)

    category = Category("Электроника", "Вся электроника тут")
    category.add_product(p1)
    category.add_product(p2)
    assert str(category) == "Электроника, количество продуктов: 3 шт."


# Новые тесты по домашке 16-1
# Тесты для дочернего класса Smartphone
def test_smartphone_initialization():
    """Проверяет корректную инициализацию объекта Smartphone."""
    phone = Smartphone(
        name="TestPhone",
        description="A test device",
        price=50000.0,
        quantity=10,
        efficiency=92.5,
        model="X1",
        memory=128,
        color="Black"
    )

    assert phone.name == "TestPhone"
    assert phone.description == "A test device"
    assert phone.price == 50000.0
    assert phone.quantity == 10
    assert phone.efficiency == 92.5
    assert phone.model == "X1"
    assert phone.memory == 128
    assert phone.color == "Black"


# Тесты для дочернего класса LawnGrass
def test_lawn_grass_initialization():
    """Проверяет корректную инициализацию объекта LawnGrass."""
    grass = LawnGrass(
        name="TestGrass",
        description="For testing",
        price=400.0,
        quantity=5,
        country="Testland",
        germination_period="10 days",
        color="Green"
    )

    assert grass.name == "TestGrass"
    assert grass.description == "For testing"
    assert grass.price == 400.0
    assert grass.quantity == 5
    assert grass.country == "Testland"
    assert grass.germination_period == "10 days"
    assert grass.color == "Green"


def test_inheritance_validation():
    """Проверяет, что валидация цены из родительского класса работает в наследниках."""
    # Проверка для Smartphone
    with pytest.raises(ValueError):
        # Если сеттер просто печатает, тест не упадет. Нужно, чтобы он вызывал ValueError.
        phone = Smartphone("Test", "Desc", -100, 1, 90, "M1", 64, "White")

    # Проверка для LawnGrass
    with pytest.raises(ValueError):
        grass = LawnGrass("Test", "Desc", -50, 2, "Land", "5 days", "Green")


# Тесты для класса Product
def test_add_same_class():
    """Проверяет, что сложение работает для объектов одного класса."""
    phone1 = Smartphone("P1", "Desc", 10000.0, 2, 95, "M1", 64, "Black")
    phone2 = Smartphone("P2", "Desc", 20000.0, 3, 98, "M2", 128, "White")

    # Ожидаемый результат: (10000 * 2) + (20000 * 3) = 80000
    total_cost = phone1 + phone2
    assert total_cost == 80000.0


def test_add_different_classes():
    """Проверяет, что сложение объектов разных классов вызывает TypeError."""
    phone = Smartphone("P1", "Desc", 1000.0, 1, 95, "M1", 64, "Black")
    grass = LawnGrass("G1", "Desc", 500.0, 1, "RU", "7 days", "Green")

    with pytest.raises(TypeError) as exc_info:
        result = phone + grass

    assert "unsupported operand type(s) for +: 'Smartphone' and 'LawnGrass'" in str(exc_info.value)


# Тесты для класса Category
def test_add_valid_product():
    """Проверяет добавление валидного продукта в категорию."""
    category = Category("Phones", "Category for phones")
    product = Product("Generic Product", "Desc", 10.0, 5)
    category.add_product(product)

    # Проверяем, что продукт добавлен в список и счетчик увеличился
    assert len(category.products) == 1
    assert category.products[0] == str(product)
    assert Category.product_count == 5


def test_add_invalid_object():
    """Проверяет, что добавление не-объекта вызывает ошибку."""
    category = Category("Phones", "Category for phones")

    # Ожидание: попытка добавить строку должна вызвать TypeError (согласно вашему исправлению)
    with pytest.raises(TypeError) as exc_info:
        category.add_product("Not a product")

    assert str(exc_info.value) == "Можно добавить только объект класса Product или его наследников"
