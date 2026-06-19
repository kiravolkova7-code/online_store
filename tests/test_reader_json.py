import json
import pytest
from src.reader_json import load_categories_from_json

TEST_JSON_DATA = [
    {
        "name": "Смартфоны",
        "description": "Смартфоны, как средство не только коммуникации...",
        "products": [
            {
                "name": "Samsung Galaxy S23 Ultra",
                "description": "256GB, Серый цвет, 200MP камера",
                "price": 180000.0,
                "quantity": 5
            }
        ]
    }
]


def test_load_categories_from_json_success(tmp_path):
    """
    Проверяет, что функция корректно загружает данные из JSON-файла и создает объекты.
    """
    d = tmp_path / "data"
    d.mkdir()
    json_file = d / "categories.json"
    json_file.write_text(json.dumps(TEST_JSON_DATA), encoding='utf-8')

    categories = load_categories_from_json(str(json_file))

    assert isinstance(categories, list)
    assert len(categories) == 1

    category = categories[0]

    #   - Проверяем атрибуты объекта Category
    assert category.name == "Смартфоны"
    assert category.description == "Смартфоны, как средство не только коммуникации..."
    assert len(category.products) == 1

    #   - Проверяем атрибуты вложенного объекта Product
    product = category.products[0]
    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.price == 180000.0
    assert product.quantity == 5


def test_load_categories_from_json_file_not_found():
    """
    Проверяет, что функция корректно вызывает исключение FileNotFoundError,
    если файл не существует.
    """
    non_existent_path = "data/non_existent_file.json"
    with pytest.raises(FileNotFoundError):
        load_categories_from_json(non_existent_path)
