# tests/test_reader_json.py

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

    # --- ИЗМЕНЕНИЕ ---
    # Получаем список СТРОК вместо объектов Product
    product_strings = category.products
    assert len(product_strings) == 1

    # Теперь проверяем, что нужная нам строка находится в этом списке
    expected_product_str = "Samsung Galaxy S23 Ultra, 180000.00 руб. Остаток: 5 шт."
    assert expected_product_str in product_strings

def test_load_categories_from_json_file_not_found():
    """
    Проверяет, что функция корректно вызывает исключение FileNotFoundError,
    если файл не существует.
    """
    non_existent_path = "data/non_existent_file.json"
    with pytest.raises(FileNotFoundError):
        load_categories_from_json(non_existent_path)
