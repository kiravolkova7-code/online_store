import json
from src.classes import Category, Product


def _read_json_file(file_path: str):
    """
    Внутренняя функция для чтения данных из JSON-файла.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def load_categories_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    categories = []
    for cat_data in data:
        name = cat_data.get('name')
        description = cat_data.get('description')
        category = Category(name, description)

        for prod_data in cat_data.get('products', []):
            try:
                product = Product.new_product(prod_data)
                category.add_product(product)
            except Exception as e:
                print(f"Не удалось создать продукт из данных {prod_data}: {e}")

        categories.append(category)
    return categories
