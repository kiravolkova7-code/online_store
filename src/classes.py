class Product():
    name : str
    description : str
    __price : float
    quantity : int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: dict):
        """
        Класс-метод для создания объекта Product из словаря.
        """
        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )

    @property
    def price(self) -> float:
        """Возвращает значение приватного атрибута цены."""
        return self.__price

    @price.setter
    def price(self, value: float):
        """
        Устанавливает цену товара.
        Если цена <= 0, выводит предупреждение и не меняет текущую цену.
        """
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = value


class Category():
    name : str
    description : str
    __products: list

    category_count = 0
    product_count = 0

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.__products = []

        Category.category_count += 1
        if products is not None:
            for prod in products:
                self.add_product(prod)

    def add_product(self, product):
        """
        Добавляет товар в категорию.
        """
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise ValueError("Можно добавить только объект класса Product")

    @property
    def products(self):
        """Геттер для получения списка товаров в категории"""
        return self.__products

    def get_products(self):
        """
        Возвращает список товаров в виде отформатированных строк.
        """
        formatted_list = []
        for product in self.__products:
            line = f"{product.name}, {product.price:.2f} руб. Остаток: {product.quantity} шт."
            formatted_list.append(line)
        return formatted_list
