from src.classes import *
from src.reader_json import load_categories_from_json


if __name__ == "__main__":
    json_file_path = 'data/products.json'
    categories_list = load_categories_from_json(json_file_path)

    print("=== Загруженные данные ===")
    for cat in categories_list:
        print(f"\nКатегория: {cat.name}")
        print(f"Описание: {cat.description}")
        print(f"Кол-во товаров: {len(cat.products)}")
        for p in cat.products:
            print(f" - Товар: {p.name}, Цена: {p.price} руб.")

    print("\n=== Статистика ===")
    print(f"Всего категорий создано: {Category.category_count}")
    print(f"Всего товаров создано: {Category.product_count}")
