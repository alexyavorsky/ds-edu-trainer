# Урок oop-methods. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% method
class Product:
    def __init__(self, name, price, volume):
        self.name = name
        self.price = price
        self.volume = volume

    def label(self):
        return f"{self.name}, {self.volume} мл"


latte = Product("Латте", 220, 300)
tea = Product("Чай", 120, 400)
print(latte.label())
print(tea.label())

# %% same-call
print(latte.label())
print(Product.label(latte))  # то же самое: latte становится self

# %% label [exercise]
class Drink:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def label(self):
        return f"{self.name} — {self.price} ₽"
# ─── заготовка ───
class Drink:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def label(self):
        ...  # верните строку "Название — цена ₽"
# ─── проверка ───
def test_label():
    "Drink(\"Капучино\", 220).label() = \"Капучино — 220 ₽\""
    got = Drink("Капучино", 220).label()
    assert got is not None, "метод ничего не возвращает — нужен return, а не print"
    assert isinstance(got, str), f"label() вернул {type(got).__name__}, а нужна строка"
    assert got == "Капучино — 220 ₽", f"label() вернул {got!r}, а нужно \"Капучино — 220 ₽\""


def test_other():
    "у другого экземпляра — своя строка"
    got = Drink("Раф", 260).label()
    assert got == "Раф — 260 ₽", f"Drink(\"Раф\", 260).label() вернул {got!r} — берите название и цену из self, а не пишите их в строке"
# ─── другое решение ───
class Drink:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def label(self):
        return self.name + " — " + str(self.price) + " ₽"
# ─── ошибка ───
class Drink:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def label(self):
        print(f"{self.name} — {self.price} ₽")
# ─── ошибка ───
class Drink:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def label(self):
        return "Капучино — 220 ₽"

# %% state
class Pastry:
    def __init__(self, name, left):
        self.name = name
        self.left = left

    def sell(self, count):
        self.left = self.left - count

    def is_sold_out(self):
        return self.left == 0


croissant = Pastry("Круассан", 5)
croissant.sell(2)
print(croissant.left, croissant.is_sold_out())
croissant.sell(3)
print(croissant.left, croissant.is_sold_out())

# %% machine [exercise]
class CoffeeMachine:
    def __init__(self):
        self.cups = 0

    def brew(self, count=1):
        self.cups = self.cups + count

    def needs_cleaning(self):
        return self.cups >= 50
# ─── заготовка ───
class CoffeeMachine:
    def __init__(self):
        ...

    def brew(self, count=1):
        ...

    def needs_cleaning(self):
        ...
# ─── проверка ───
def _machine():
    try:
        return CoffeeMachine()
    except TypeError as e:
        assert False, f"CoffeeMachine() не создаётся: {e}. У __init__ только параметр self"


def test_new():
    "у новой машины cups = 0"
    m = _machine()
    assert hasattr(m, "cups"), "у новой машины нет атрибута cups — запишите в __init__ self.cups = 0"
    assert m.cups == 0, f"у новой машины cups = {m.cups!r}, а нужно 0"


def test_brew():
    "brew() и brew(3) увеличивают счётчик"
    m = _machine()
    assert hasattr(m, "cups"), "сначала задайте cups в __init__"
    try:
        result = m.brew()
        m.brew(3)
    except TypeError as e:
        assert False, f"brew не вызывается: {e}. Объявите def brew(self, count=1):"
    assert result is None, f"brew() вернул {result!r}, а должен только изменить счётчик и ничего не возвращать"
    assert m.cups == 4, f"после brew() и brew(3) cups = {m.cups!r}, а нужно 4 — прибавляйте count к self.cups"


def test_cleaning():
    "needs_cleaning() — True с 50 чашек"
    m = _machine()
    assert hasattr(m, "cups"), "сначала задайте cups в __init__"
    m.cups = 49
    assert m.needs_cleaning() is False, "при 49 чашках чистка ещё не нужна — needs_cleaning() должен вернуть False"
    m.cups = 50
    assert m.needs_cleaning() is True, "при 50 чашках needs_cleaning() должен вернуть True: сравнение >= 50"
# ─── другое решение ───
class CoffeeMachine:
    def __init__(self):
        self.cups = 0

    def brew(self, count=1):
        self.cups += count

    def needs_cleaning(self):
        if self.cups < 50:
            return False
        return True
# ─── ошибка ───
class CoffeeMachine:
    def __init__(self):
        self.cups = 0

    def brew(self, count=1):
        self.cups = self.cups + count
        return self.cups

    def needs_cleaning(self):
        return self.cups >= 50
# ─── ошибка ───
class CoffeeMachine:
    def __init__(self):
        self.cups = 0

    def brew(self, count=1):
        self.cups = self.cups + 1

    def needs_cleaning(self):
        return self.cups >= 50
# ─── ошибка ───
class CoffeeMachine:
    def __init__(self):
        self.cups = 0

    def brew(self, count=1):
        self.cups = self.cups + count

    def needs_cleaning(self):
        return self.cups > 50

# %% bill [exercise]
class Bill:
    def __init__(self, amount):
        self.amount = amount

    def with_tip(self, percent=10):
        return round(self.amount * (100 + percent) / 100)
# ─── заготовка ───
class Bill:
    def __init__(self, amount):
        self.amount = amount

    def with_tip(self, percent=10):
        ...
# ─── проверка ───
def test_default():
    "Bill(500).with_tip() = 550"
    try:
        got = Bill(500).with_tip()
    except TypeError:
        assert False, "with_tip() не вызывается без аргумента — дайте percent значение по умолчанию 10"
    assert got is not None, "метод ничего не возвращает — нужен return"
    assert got == 550, f"Bill(500).with_tip() = {got!r}, а нужно 550"


def test_percent():
    "Bill(480).with_tip(5) = 504, округление до целых"
    assert Bill(480).with_tip(5) == 504, f"Bill(480).with_tip(5) = {Bill(480).with_tip(5)!r}, а нужно 504"
    got = Bill(333).with_tip(15)
    assert got == 383, f"Bill(333).with_tip(15) = {got!r}, а нужно 383 — округлите функцией round"


def test_unchanged():
    "amount не меняется"
    bill = Bill(500)
    bill.with_tip()
    assert bill.amount == 500, f"после with_tip() amount = {bill.amount!r}: метод должен вернуть сумму с чаевыми, а не записать её в self.amount"
# ─── другое решение ───
class Bill:
    def __init__(self, amount):
        self.amount = amount

    def with_tip(self, percent=10):
        tip = self.amount * percent / 100
        return round(self.amount + tip)
# ─── ошибка ───
class Bill:
    def __init__(self, amount):
        self.amount = amount

    def with_tip(self, percent=10):
        self.amount = round(self.amount * (100 + percent) / 100)
        return self.amount
# ─── ошибка ───
class Bill:
    def __init__(self, amount):
        self.amount = amount

    def with_tip(self, percent=10):
        return self.amount * (100 + percent) / 100

# %% no-self [raises=TypeError]
class Cookie:
    def __init__(self, name):
        self.name = name

    def label():  # забыли self
        return "печенье"


Cookie("Овсяное").label()

# %% no-parens
text = latte.label  # без скобок: сам метод
print(type(text).__name__)
print(text())

# %% no-parens-error [raises=AttributeError]
latte.label.upper()

# %% parens-quiz [quiz]
print(type(latte.label()).__name__)

# %% labels [exercise]
menu = [Drink("Эспрессо", 150), Drink("Капучино", 220), Drink("Раф", 260)]
labels = [d.label() for d in menu]
# ─── заготовка ───
menu = [Drink("Эспрессо", 150), Drink("Капучино", 220), Drink("Раф", 260)]
labels = ...
# ─── проверка ───
def test_labels():
    "labels — строки меню по порядку"
    assert isinstance(labels, list), f"labels — это {type(labels).__name__}, а нужен список"
    assert len(labels) == 3, f"в labels {len(labels)} элементов, а напитков 3"
    assert all(isinstance(x, str) for x in labels), "в labels не строки, а сами методы — вызовите метод со скобками: d.label()"
    assert labels == ["Эспрессо — 150 ₽", "Капучино — 220 ₽", "Раф — 260 ₽"], f"в labels {labels}"
# ─── другое решение ───
menu = [Drink("Эспрессо", 150), Drink("Капучино", 220), Drink("Раф", 260)]
labels = []
for drink in menu:
    labels.append(drink.label())
# ─── ошибка ───
menu = [Drink("Эспрессо", 150), Drink("Капучино", 220), Drink("Раф", 260)]
labels = [d.label for d in menu]
