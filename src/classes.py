from abc import ABC, abstractmethod

class BaseProduct(ABC):
    """
    Абстрактный базовый класс для всех продуктов.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str):
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @description.setter
    @abstractmethod
    def description(self, value: str):
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        pass

    @price.setter
    @abstractmethod
    def price(self, value: float):
        pass

    @property
    @abstractmethod
    def quantity(self) -> int:
        pass

    @quantity.setter
    @abstractmethod
    def quantity(self, value: int):
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Должен возвращать строковое представление товара."""
        pass


class CreationLoggerMixin:
    """
    Миксин, который формирует лог создания объекта,
    возвращая имя класса и переданные аргументы в виде строки.
    """

    def __init__(self, *args, **kwargs):
        self._creation_args = args
        self._creation_kwargs = kwargs
        super().__init__()

    def get_creation_log(self) -> str:
        """Возвращает строку с информацией о создании объекта."""
        args_repr = [repr(a) for a in self._creation_args]
        kwargs_repr = [f"{k}={v!r}" for k, v in self._creation_kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        return f"Создан объект класса {self.__class__.__name__} с аргументами: ({signature})"


class Product(CreationLoggerMixin, BaseProduct):
    """
    Конкретный класс продукта.
    Наследует логирование от CreationLoggerMixin и обязательный интерфейс от BaseProduct.
    """

    def __init__(self, name, description, price, quantity):
        self._name = name
        self._description = description
        self.price = price
        self._quantity = quantity

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

    def __add__(self, other):
        """
        Возвращает общую стоимость товаров на складе.
        """
        if isinstance(other, Product):
            if type(self) is type(other):
                total_cost = (self.price * self.quantity) + (other.price * other.quantity)
                return total_cost
        raise TypeError("Нельзя складывать товары разных типов")

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    _price: float = 0.0

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if value <= 0:
            raise ValueError("Цена не должна быть нулевая или отрицательная")
        self._price = value

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        self._quantity = value

    def __str__(self) -> str:
        return f"{self.name}, {self.price:.2f} руб. Остаток: {self.quantity} шт."


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
