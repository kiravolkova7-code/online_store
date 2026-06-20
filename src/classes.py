class Product():
    name: str
    description: str
    __price: float
    quantity: int

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

    def __str__(self):
        """Строковое представление товара."""
        return f"{self.name}, {self.price:.2f} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """
        Возвращает общую стоимость двух товаров на складе.
        """
        if isinstance(other, Product):
            total_cost = (self.price * self.quantity) + (other.price * other.quantity)
            return total_cost
        else:
            raise TypeError(f"Неподдерживаемый тип для сложения: '{type(other).__name__}'. Ожидается 'Product'.")


class Category():
    name: str
    description: str
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
        Добавляет товар в категорию и увеличивает глобальный счетчик товаров.
        """
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += product.quantity
        else:
            raise ValueError("Можно добавить только объект класса Product")

    @property
    def products(self):
        """
        Теперь этот геттер при вызове автоматически форматирует список товаров.
        """
        return self.get_products()

    def get_products(self):
        """
        Возвращает список товаров в виде отформатированных строк.
        Оптимизировано за счет использования __str__ метода Product.
        """
        return [str(product) for product in self.__products]

    def __str__(self):
        """Строковое представление категории."""
        return f"{self.name}, количество продуктов: {Category.product_count} шт."
