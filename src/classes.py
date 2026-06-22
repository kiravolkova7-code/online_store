class Product():
    name: str
    description: str
    __price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price  # Используется сеттер для валидации
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

            raise ValueError("Цена не должна быть нулевая или отрицательная")
        self.__price = value

    def __str__(self):
        """Строковое представление товара."""
        return f"{self.name}, {self.price:.2f} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """
        Возвращает общую стоимость товаров на складе.
        Доработано по Заданию 2: складываются только товары одного класса.
        При попытке сложения объектов разных классов вызывается TypeError.
        """
        if isinstance(other, Product):
            if type(self) is type(other):
                total_cost = (self.price * self.quantity) + (other.price * other.quantity)
                return total_cost
        raise TypeError("Нельзя складывать товары разных типов")


class Smartphone(Product):
    """
    Класс для представления смартфонов.
    """
    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        # Вызов конструктора базового класса для инициализации общих атрибутов
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """
    Класс для представления газонной травы.
    """
    def __init__(self, name, description, price, quantity, country, germination_period, color):
        # Вызов конструктора базового класса для инициализации общих атрибутов
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


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
            print(f"Добавлен товар: {product.name}")
        else:
            raise TypeError("Можно добавить только объект класса Product или его наследников")

    @property
    def products(self):
        """
        Возвращает список товаров в виде отформатированных строк.
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
