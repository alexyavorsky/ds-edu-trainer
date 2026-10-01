# Урок oop-super. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% init
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.price})"

    def label(self):
        return f"{self.name} — {self.price} ₽"

    def cost(self, quantity):
        return self.price * quantity


class Pastry(Product):
    def __init__(self, name, price, weight):
        super().__init__(name, price)  # name и price записывает Product
        self.weight = weight


croissant = Pastry("Круассан", 140, 70)
print(croissant.name, croissant.price, croissant.weight)
print(croissant.label())

# %% drink [exercise]
class Drink(Product):
    def __init__(self, name, price, volume):
        super().__init__(name, price)
        self.volume = volume

    def per_100ml(self):
        return round(self.price / self.volume * 100, 1)
# ─── заготовка ───
class Drink(Product):
    def __init__(self, name, price, volume):
        ...

    def per_100ml(self):
        ...
# ─── проверка ───
def _latte():
    try:
        return Drink("Латте", 220, 300)
    except TypeError as e:
        assert False, f"Drink(\"Латте\", 220, 300) не создаётся: {e}"


def test_attributes():
    "name, price и volume"
    assert issubclass(Drink, Product), "Drink должен наследовать от Product"
    latte = _latte()
    assert hasattr(latte, "name") and hasattr(latte, "price"), "у напитка нет name и price — вызовите в __init__ super().__init__(name, price)"
    assert (latte.name, latte.price) == ("Латте", 220), f"name и price = {latte.name!r}, {latte.price!r}"
    assert getattr(latte, "volume", None) == 300, "объём хранится в атрибуте volume"


def test_uses_super():
    "name и price записывает Product.__init__"
    calls = []
    original = Product.__init__

    def spy(self, *args, **kwargs):
        calls.append(1)
        original(self, *args, **kwargs)
    Product.__init__ = spy
    try:
        latte = Drink("Латте", 220, 300)
    finally:
        Product.__init__ = original
    assert calls == [1], "Product.__init__ не вызывался — используйте super().__init__(name, price), а не копируйте его строки"
    assert (latte.name, latte.price) == ("Латте", 220), "в super().__init__ переданы не те значения — нужны name и price"


def test_per_100ml():
    "per_100ml — цена за 100 мл"
    latte = _latte()
    assert hasattr(latte, "price"), "сначала вызовите super().__init__(name, price) — без цены per_100ml не посчитать"
    assert latte.per_100ml() == 73.3, f"per_100ml() у латте = {latte.per_100ml()!r}, а нужно 73.3"
    assert latte.label() == "Латте — 220 ₽", "label у напитка должен работать как у Product"
# ─── другое решение ───
class Drink(Product):
    def __init__(self, name, price, volume=250):
        super().__init__(name=name, price=price)
        self.volume = volume

    def per_100ml(self):
        return round(100 * self.price / self.volume, 1)
# ─── ошибка ───
class Drink(Product):
    def __init__(self, name, price, volume):
        self.volume = volume

    def per_100ml(self):
        return round(self.price / self.volume * 100, 1)
# ─── ошибка ───
class Drink(Product):
    def __init__(self, name, price, volume):
        self.name = name
        self.price = price
        self.volume = volume

    def per_100ml(self):
        return round(self.price / self.volume * 100, 1)

# %% forgot [raises=AttributeError]
class Cake(Product):
    def __init__(self, name, price, slices):
        self.slices = slices  # забыли super().__init__


cake = Cake("Медовик", 1200, 8)
print(cake.slices)
print(cake.label())

# %% extend
class Pastry(Product):
    def __init__(self, name, price, weight):
        super().__init__(name, price)
        self.weight = weight

    def label(self):
        return f"{super().label()}, {self.weight} г"


print(Pastry("Круассан", 140, 70).label())

# %% seasonal [exercise]
class SeasonalProduct(Product):
    def __init__(self, name, price, until):
        super().__init__(name, price)
        self.until = until

    def label(self):
        return f"{super().label()} (до {self.until})"
# ─── заготовка ───
class SeasonalProduct(Product):
    def __init__(self, name, price, until):
        ...

    def label(self):
        ...
# ─── проверка ───
def _item():
    try:
        return SeasonalProduct("Глинтвейн", 300, "31 декабря")
    except TypeError as e:
        assert False, f"SeasonalProduct(\"Глинтвейн\", 300, \"31 декабря\") не создаётся: {e}"


def test_init():
    "name, price и until"
    item = _item()
    assert hasattr(item, "name"), "у товара нет name — вызовите в __init__ super().__init__(name, price)"
    assert getattr(item, "until", None) == "31 декабря", "дата хранится в атрибуте until"


def test_label():
    "строка базового класса + пометка"
    item = _item()
    assert hasattr(item, "name"), "сначала вызовите super().__init__"
    got = item.label()
    assert got == "Глинтвейн — 300 ₽ (до 31 декабря)", f"label() вернул {got!r}"


def test_extends():
    "label берёт строку у Product"
    original = Product.label
    Product.label = lambda self: f"[{self.name}]"
    try:
        got = _item().label()
    finally:
        Product.label = original
    assert got == "[Глинтвейн] (до 31 декабря)", "label подкласса не использует label базового класса — вызовите super().label() вместо того, чтобы собирать строку заново"
# ─── другое решение ───
class SeasonalProduct(Product):
    def __init__(self, name, price, until):
        super().__init__(name, price)
        self.until = until

    def label(self):
        base = super().label()
        return base + " (до " + self.until + ")"
# ─── ошибка ───
class SeasonalProduct(Product):
    def __init__(self, name, price, until):
        super().__init__(name, price)
        self.until = until

    def label(self):
        return f"{self.name} — {self.price} ₽ (до {self.until})"
# ─── ошибка ───
class SeasonalProduct(Product):
    def __init__(self, name, price, until):
        super().__init__(name, price)
        self.until = until

    def label(self):
        return f"(до {self.until})"

# %% wholesale [exercise]
class WholesaleProduct(Product):
    def cost(self, quantity):
        full = super().cost(quantity)
        if quantity >= 10:
            return round(full * 85 / 100)
        return full
# ─── заготовка ───
class WholesaleProduct(Product):
    def cost(self, quantity):
        ...
# ─── проверка ───
def test_small():
    "меньше 10 штук — без скидки"
    beans = WholesaleProduct("Зёрна, 250 г", 120)
    got = beans.cost(9)
    assert got is not None, "cost ничего не возвращает — нужен return"
    assert got == 1080, f"cost(9) = {got!r}, а 9 пачек по 120 ₽ без скидки — 1080"


def test_bulk():
    "от 10 штук — скидка 15 %"
    beans = WholesaleProduct("Зёрна, 250 г", 120)
    assert beans.cost(10) != 1200, "от 10 штук должна быть скидка 15 %"
    assert beans.cost(10) == 1020, f"cost(10) = {beans.cost(10)!r}, а нужно 1020"
    got = WholesaleProduct("Сироп", 133).cost(12)
    assert got == 1357, f"12 бутылок сиропа по 133 ₽ = {got!r}, а со скидкой нужно 1357 (1356.6, округлите)"


def test_extends():
    "оптовая цена опирается на Product.cost"
    original = Product.cost
    Product.cost = lambda self, quantity: 1000
    try:
        got = WholesaleProduct("Сироп", 133).cost(12)
    finally:
        Product.cost = original
    assert got == 850, "cost подкласса не использует cost базового класса — вызовите super().cost(quantity) вместо умножения"
# ─── другое решение ───
class WholesaleProduct(Product):
    BULK = 10

    def cost(self, quantity):
        if quantity < self.BULK:
            return super().cost(quantity)
        return round(super().cost(quantity) * 0.85)
# ─── ошибка ───
class WholesaleProduct(Product):
    def cost(self, quantity):
        full = self.price * quantity
        if quantity >= 10:
            return round(full * 85 / 100)
        return full
# ─── ошибка ───
class WholesaleProduct(Product):
    def cost(self, quantity):
        full = super().cost(quantity)
        if quantity > 10:
            return round(full * 85 / 100)
        return full

# %% mro
print([cls.__name__ for cls in Pastry.__mro__])
print([cls.__name__ for cls in WholesaleProduct.__mro__])

# %% object-quiz [quiz]
print(Product.__mro__[-1].__name__)
