# Урок oop-repr. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% dunder
word = "латте"
print(len(word))
print(word.__len__())  # это и делает len

# %% repr
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price})"


latte = Product("Латте", 220)
print(repr(latte))
print([latte, Product("Чай", 120)])
latte  # значение последней строки ячейки показывается через repr

# %% drink-repr [exercise]
class Drink:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Drink({self.name!r}, {self.price})"
# ─── заготовка ───
class Drink:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        ...
# ─── проверка ───
def test_repr():
    "repr(Drink(\"Латте\", 220)) = Drink('Латте', 220)"
    assert "__repr__" in Drink.__dict__, "в классе нет метода __repr__ — объявите его"
    got = Drink.__dict__["__repr__"](Drink("Латте", 220))
    assert isinstance(got, str), f"__repr__ вернул {type(got).__name__}, а должен вернуть строку"
    assert got != "Drink(Латте, 220)", "название без кавычек — вставьте его с !r: {self.name!r}"
    assert got == "Drink('Латте', 220)", f"repr = {got!r}, а нужно \"Drink('Латте', 220)\""


def test_other():
    "repr другого напитка и списка"
    assert "__repr__" in Drink.__dict__, "сначала объявите __repr__"
    got = repr([Drink("Раф", 260), Drink("Чай", 120)])
    assert got == "[Drink('Раф', 260), Drink('Чай', 120)]", f"repr списка напитков: {got} — берите значения из self"
# ─── другое решение ───
class Drink:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return "Drink(" + repr(self.name) + ", " + str(self.price) + ")"
# ─── ошибка ───
class Drink:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Drink({self.name}, {self.price})"
# ─── ошибка ───
class Drink:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"Drink({self.name!r}, {self.price})"

# %% str
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price})"

    def __str__(self):
        return f"{self.name} за {self.price} ₽"


latte = Product("Латте", 220)
print(latte)
print(str(latte), "|", repr(latte))
print(f"Сегодня советуем: {latte}")
latte

# %% order-str [exercise]
class Order:
    def __init__(self, number, total):
        self.number = number
        self.total = total

    def __repr__(self):
        return f"Order({self.number}, {self.total})"

    def __str__(self):
        return f"Заказ №{self.number} на {self.total} ₽"
# ─── заготовка ───
class Order:
    def __init__(self, number, total):
        self.number = number
        self.total = total

    def __repr__(self):
        ...

    def __str__(self):
        ...
# ─── проверка ───
def test_repr():
    "repr — Order(17, 640)"
    assert "__repr__" in Order.__dict__, "в классе нет __repr__ — объявите его"
    got = Order.__dict__["__repr__"](Order(17, 640))
    assert got == "Order(17, 640)", f"repr заказа = {got!r}, а нужно \"Order(17, 640)\""


def test_str():
    "str — Заказ №17 на 640 ₽"
    assert "__str__" in Order.__dict__, "в классе нет __str__ — объявите его"
    got = Order.__dict__["__str__"](Order(17, 640))
    assert got != "Order(17, 640)", "__str__ вернул то же, что __repr__, а нужен текст для кассира"
    assert got == "Заказ №17 на 640 ₽", f"str заказа = {got!r}, а нужно \"Заказ №17 на 640 ₽\""
    assert str(Order(3, 150)) == "Заказ №3 на 150 ₽", "у Order(3, 150) str должен быть \"Заказ №3 на 150 ₽\" — берите значения из self"
# ─── другое решение ───
class Order:
    def __init__(self, number, total):
        self.number = number
        self.total = total

    def __str__(self):
        return "Заказ №" + str(self.number) + " на " + str(self.total) + " ₽"

    def __repr__(self):
        return f"{type(self).__name__}({self.number}, {self.total})"
# ─── ошибка ───
class Order:
    def __init__(self, number, total):
        self.number = number
        self.total = total

    def __repr__(self):
        return f"Заказ №{self.number} на {self.total} ₽"

    def __str__(self):
        return f"Order({self.number}, {self.total})"

# %% list-quiz [quiz]
print([Order(17, 640)])

# %% log [exercise]
order = Order(17, 640)
message = f"Готов: {order}"
log = f"создан {order!r}"
# ─── заготовка ───
order = Order(17, 640)
message = ...
log = ...
# ─── проверка ───
def test_message():
    "message — через __str__"
    assert message == "Готов: Заказ №17 на 640 ₽", f"message = {message!r}, а нужно \"Готов: Заказ №17 на 640 ₽\": {{order}} в f-строке"


def test_log():
    "log — через __repr__"
    assert log != "создан Заказ №17 на 640 ₽", "в log попал текст __str__ — для repr добавьте !r: {order!r}"
    assert log == "создан Order(17, 640)", f"log = {log!r}, а нужно \"создан Order(17, 640)\""
# ─── другое решение ───
order = Order(17, 640)
message = "Готов: " + str(order)
log = "создан " + repr(order)
# ─── ошибка ───
order = Order(17, 640)
message = f"Готов: {order}"
log = f"создан {order}"
