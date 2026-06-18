import json
from src.classes import Category, Product


def _read_json_file(file_path: str):
    """
    Внутренняя функция для чтения данных из JSON-файла.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def load_categories_from_json(file_path: str):
    """
    Читает данные из JSON-файла и создает список объектов Category с товарами.
    """
    raw_data = _read_json_file(file_path)

    categories = []

    for cat_data in raw_data:
        product_objects = []
        for prod_data in cat_data.get('products', []):
            product = Product(
                name=prod_data['name'],
                description=prod_data['description'],
                price=prod_data['price'],
                quantity=prod_data['quantity']
            )
            product_objects.append(product)

        category = Category(
            name=cat_data['name'],
            description=cat_data['description'],
            products=product_objects
        )
        categories.append(category)

    return categories
