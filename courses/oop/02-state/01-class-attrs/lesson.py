# Урок oop-class-attrs. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% class-attr
class Product:
    CURRENCY = "₽"  # атрибут класса: один на всех

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def label(self):
        return f"{self.name} — {self.price} {self.CURRENCY}"


latte = Product("Латте", 220)
tea = Product("Чай", 120)
print(Product.CURRENCY)
print(latte.CURRENCY, tea.CURRENCY)
print(latte.label())

# %% lookup
print(latte.__dict__)
print("CURRENCY" in latte.__dict__)
print("CURRENCY" in Product.__dict__)

# %% max-discount [exercise]
class Product:
    CURRENCY = "₽"
    MAX_DISCOUNT = 30

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def discounted(self, percent):
        percent = min(percent, self.MAX_DISCOUNT)
        return round(self.price * (100 - percent) / 100)
# ─── заготовка ───
class Product:
    CURRENCY = "₽"
    # объявите здесь MAX_DISCOUNT

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def discounted(self, percent):
        ...
# ─── проверка ───
def test_constant():
    "MAX_DISCOUNT = 30 — атрибут класса"
    assert "MAX_DISCOUNT" in Product.__dict__, "в классе нет атрибута MAX_DISCOUNT — объявите его в теле класса, а не в __init__"
    assert Product.MAX_DISCOUNT == 30, f"Product.MAX_DISCOUNT = {Product.MAX_DISCOUNT!r}, а нужно 30"


def test_small():
    "скидка до предела применяется как есть"
    got = Product("Латте", 200).discounted(10)
    assert got is not None, "discounted() ничего не возвращает — нужен return"
    assert got == 180, f"Product(\"Латте\", 200).discounted(10) = {got!r}, а нужно 180"


def test_capped():
    "больше 30 % — только 30 %"
    got = Product("Латте", 200).discounted(50)
    assert got != 100, "скидка 50 % применилась целиком, а больше MAX_DISCOUNT давать нельзя"
    assert got == 140, f"Product(\"Латте\", 200).discounted(50) = {got!r}, а нужно 140 — скидка не больше 30 %"


def test_uses_constant():
    "метод берёт предел из атрибута класса"
    assert "MAX_DISCOUNT" in Product.__dict__, "сначала объявите MAX_DISCOUNT в классе"
    old = Product.MAX_DISCOUNT
    try:
        Product.MAX_DISCOUNT = 50
        got = Product("Латте", 200).discounted(60)
    finally:
        Product.MAX_DISCOUNT = old
    assert got == 100, "когда Product.MAX_DISCOUNT = 50, предел должен стать 50 % — читайте его из self.MAX_DISCOUNT, а не пишите 30 в методе"
# ─── другое решение ───
class Product:
    CURRENCY = "₽"
    MAX_DISCOUNT = 30

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def discounted(self, percent):
        if percent > Product.MAX_DISCOUNT:
            percent = Product.MAX_DISCOUNT
        return round(self.price * (100 - percent) / 100)
# ─── ошибка ───
class Product:
    CURRENCY = "₽"
    MAX_DISCOUNT = 30

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def discounted(self, percent):
        return round(self.price * (100 - min(percent, 30)) / 100)
# ─── ошибка ───
class Product:
    CURRENCY = "₽"

    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.MAX_DISCOUNT = 30

    def discounted(self, percent):
        percent = min(percent, self.MAX_DISCOUNT)
        return round(self.price * (100 - percent) / 100)
# ─── ошибка ───
class Product:
    CURRENCY = "₽"
    MAX_DISCOUNT = 30

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def discounted(self, percent):
        return round(self.price * (100 - percent) / 100)

# %% shadow
latte = Product("Латте", 220)
tea = Product("Чай", 120)
latte.CURRENCY = "$"  # атрибут появился у экземпляра latte
print(latte.CURRENCY, tea.CURRENCY, Product.CURRENCY)
Product.CURRENCY = "руб."  # меняем атрибут класса
print(latte.CURRENCY, tea.CURRENCY, Product.CURRENCY)
Product.CURRENCY = "₽"  # вернём как было

# %% lookup-quiz [quiz]
class Cup:
    size = "M"


a = Cup()
b = Cup()
a.size = "L"
Cup.size = "S"
print(a.size, b.size)

# %% counter-bug
class Ticket:
    count = 0

    def __init__(self):
        self.count += 1  # ошибка: запись идёт в экземпляр


first = Ticket()
second = Ticket()
print(Ticket.count, first.count, second.count)

# %% numbering [exercise]
class Order:
    created = 0

    def __init__(self):
        Order.created += 1
        self.number = Order.created
# ─── заготовка ───
class Order:
    created = 0

    def __init__(self):
        ...
# ─── проверка ───
def _fresh_orders(n):
    "n новых заказов при счётчике, сброшенном на 0; счётчик потом возвращается"
    saved = Order.created
    try:
        Order.created = 0
        orders = [Order() for _ in range(n)]
        return orders, Order.created
    finally:
        Order.created = saved


def test_declared():
    "created — атрибут класса"
    assert "created" in Order.__dict__, "в классе нет атрибута created — объявите в теле класса created = 0"


def test_counter():
    "каждый заказ увеличивает Order.created"
    assert "created" in Order.__dict__, "сначала объявите created в классе"
    orders, created = _fresh_orders(3)
    assert created != 0, "после трёх заказов Order.created всё ещё 0: self.created += 1 меняет экземпляр, а не класс — пишите Order.created += 1"
    assert created == 3, f"после трёх заказов Order.created = {created!r}, а нужно 3"


def test_numbers():
    "номера заказов 1, 2, 3"
    assert "created" in Order.__dict__, "сначала объявите created в классе"
    orders, _ = _fresh_orders(3)
    assert all(hasattr(o, "number") for o in orders), "у заказа нет атрибута number — запишите его в __init__: self.number = …"
    numbers = [o.number for o in orders]
    assert numbers == [1, 2, 3], f"у трёх новых заказов номера {numbers}, а нужно [1, 2, 3]"
# ─── другое решение ───
class Order:
    created = 0

    def __init__(self):
        self.number = Order.created + 1
        Order.created = self.number
# ─── ошибка ───
class Order:
    created = 0

    def __init__(self):
        self.created += 1
        self.number = self.created
# ─── ошибка ───
class Order:
    created = 0

    def __init__(self):
        self.number = Order.created
        Order.created += 1

# %% shared-list
class Basket:
    items = []  # ошибка: один список на все корзины

    def add(self, name):
        self.items.append(name)


anna = Basket()
boris = Basket()
anna.add("Латте")
boris.add("Чай")
print(anna.items)
print(boris.items)

# %% fix-table [exercise]
class Table:
    def __init__(self, number):
        self.number = number
        self.orders = []

    def order(self, drink):
        self.orders.append(drink)
# ─── заготовка ───
class Table:
    orders = []

    def __init__(self, number):
        self.number = number

    def order(self, drink):
        self.orders.append(drink)
# ─── проверка ───
def _tables():
    try:
        return Table(1), Table(2)
    except TypeError as e:
        assert False, f"Table(1) не создаётся: {e}. У __init__ параметры self и number"


def test_own_lists():
    "у двух столиков — свои заказы"
    a, b = _tables()
    assert hasattr(a, "orders"), "у столика нет атрибута orders — создайте список в __init__: self.orders = []"
    a.order("Латте")
    b.order("Чай")
    assert a.orders != ["Латте", "Чай"], "заказы обоих столиков попали в один список — у каждого столика должен быть свой: self.orders = [] в __init__"
    assert a.orders == ["Латте"] and b.orders == ["Чай"], f"у столиков заказы {a.orders} и {b.orders}, а нужно ['Латте'] и ['Чай']"
    assert a.number == 1 and b.number == 2, "номер столика по-прежнему берётся из параметра number"


def test_new_empty():
    "у нового столика заказов нет"
    first, _ = _tables()
    assert hasattr(first, "orders"), "у столика нет атрибута orders — создайте список в __init__"
    first.order("Раф")
    fresh, _ = _tables()
    assert fresh.orders == [], f"у нового столика уже есть заказы {fresh.orders} — список не должен быть общим"
# ─── другое решение ───
class Table:
    def __init__(self, number):
        self.orders = list()
        self.number = number

    def order(self, drink):
        self.orders.append(drink)
# ─── ошибка ───
class Table:
    orders = []

    def __init__(self, number):
        self.number = number
        self.orders = Table.orders

    def order(self, drink):
        self.orders.append(drink)
