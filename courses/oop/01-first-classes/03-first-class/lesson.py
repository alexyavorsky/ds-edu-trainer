# Урок oop-first-class. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% declare
class Product:
    pass


print(Product.__name__)
print(type(Product).__name__)

# %% instances
first = Product()
second = Product()
print(type(first).__name__)
print(isinstance(first, Product))
print(first == second)  # два разных объекта

# %% declare-drink [exercise]
class Drink:
    pass


espresso = Drink()
# ─── заготовка ───
# объявите класс Drink

espresso = ...
# ─── проверка ───
def test_class():
    "Drink — класс"
    assert "Drink" in globals(), "класса Drink нет — объявите его: class Drink:"
    assert isinstance(Drink, type), f"Drink — это {type(Drink).__name__}, а нужен класс: class Drink:"


def test_instance():
    "espresso — экземпляр Drink"
    assert isinstance(Drink, type), "сначала объявите класс Drink"
    assert espresso is not Drink, "espresso — это сам класс; экземпляр создаётся вызовом: Drink()"
    assert isinstance(espresso, Drink), f"espresso — это {type(espresso).__name__}, а нужен экземпляр Drink: Drink()"
# ─── другое решение ───
class Drink:
    """Напиток из меню."""


espresso = Drink()
# ─── ошибка ───
class Drink:
    pass


espresso = Drink

# %% attributes
cup = Product()
cup.name = "Латте"
cup.price = 220

other = Product()
other.name = "Чай"
other.price = 120

print(cup.name, cup.price)
print(other.name, other.price)
print(cup.price + other.price)

# %% latte [exercise]
latte = Drink()
latte.name = "Латте"
latte.price = 220
latte.volume = 300
# ─── заготовка ───
latte = ...
# ─── проверка ───
def test_instance():
    "latte — экземпляр Drink"
    assert isinstance(latte, Drink), f"latte — это {type(latte).__name__}, а нужен экземпляр: latte = Drink()"


def test_attributes():
    "у latte атрибуты name, price и volume"
    assert isinstance(latte, Drink), "сначала создайте экземпляр: latte = Drink()"
    for attr in ["name", "price", "volume"]:
        assert hasattr(latte, attr), f"у latte нет атрибута {attr} — запишите его: latte.{attr} = …"
    assert latte.name == "Латте", f"latte.name = {latte.name!r}, а нужно \"Латте\""
    assert latte.price == 220, f"latte.price = {latte.price!r}, а нужно число 220 (без кавычек)"
    assert latte.volume == 300, f"latte.volume = {latte.volume!r}, а нужно число 300"
# ─── другое решение ───
latte = Drink()
latte.volume = 300
latte.price = 200 + 20
latte.name = "Латте"
# ─── ошибка ───
latte = Drink()
latte.name = "Латте"
latte.price = "220"
latte.volume = 300
# ─── ошибка ───
latte = Drink()
latte.name = "Латте"
latte.price = 220

# %% two-sizes [exercise]
small = Drink()
small.name = "Капучино"
small.price = 180
large = Drink()
large.name = "Капучино"
large.price = 240
diff = large.price - small.price
# ─── заготовка ───
small = ...
large = ...
diff = ...
# ─── проверка ───
def test_two():
    "small и large — два разных экземпляра Drink"
    assert isinstance(small, Drink) and isinstance(large, Drink), "small и large должны быть экземплярами Drink: small = Drink()"
    assert small is not large, "small и large — один и тот же объект; создайте два: два раза вызовите Drink()"
    assert getattr(small, "price", None) == 180, "у small должна быть цена small.price = 180"
    assert getattr(large, "price", None) == 240, "у large должна быть цена large.price = 240"
    assert getattr(small, "name", None) == "Капучино" and getattr(large, "name", None) == "Капучино", "у обоих напитков name = \"Капучино\""


def test_diff():
    "diff — на сколько большой дороже"
    assert diff != -60, "получилось -60: вычитайте из цены большого цену маленького"
    assert diff == 60, f"diff = {diff!r}, а большой дороже на 60 ₽"
# ─── другое решение ───
small, large = Drink(), Drink()
small.name = large.name = "Капучино"
small.price, large.price = 180, 240
diff = 240 - 180
# ─── ошибка ───
small = Drink()
small.name = "Капучино"
small.price = 180
large = Drink()
large.name = "Капучино"
large.price = 240
diff = small.price - large.price
# ─── ошибка ───
small = Drink()
small.name = "Капучино"
small.price = 180
large = small
large.price = 240
diff = large.price - small.price

# %% forgot [raises=AttributeError]
tea = Drink()
tea.name = "Чай"
print(tea.price)

# %% typo
tea.price = 120
tea.prise = 130  # опечатка
print(tea.price)
print(tea.prise)

# %% make-drink [exercise]
def make_drink(name, price):
    drink = Drink()
    drink.name = name
    drink.price = price
    return drink
# ─── заготовка ───
def make_drink(name, price):
    ...  # создайте Drink, запишите атрибуты и верните его
# ─── проверка ───
def test_returns():
    "make_drink возвращает экземпляр Drink"
    got = make_drink("Раф", 260)
    assert got is not None, "функция ничего не возвращает — в конце нужен return"
    assert isinstance(got, Drink), f"функция вернула {type(got).__name__}, а нужен экземпляр Drink"


def test_attributes():
    "атрибуты name и price — из аргументов"
    got = make_drink("Раф", 260)
    assert isinstance(got, Drink), "функция должна вернуть экземпляр Drink"
    assert getattr(got, "name", None) == "Раф", "у результата make_drink(\"Раф\", 260) должно быть name = \"Раф\""
    assert getattr(got, "price", None) == 260, "у результата make_drink(\"Раф\", 260) должно быть price = 260"
    other = make_drink("Чай", 120)
    assert getattr(other, "price", None) == 120, "атрибуты берутся из аргументов: у make_drink(\"Чай\", 120) цена 120"
    assert other is not got, "каждый вызов должен создавать новый экземпляр — Drink() внутри функции"
# ─── другое решение ───
def make_drink(name, price):
    result = Drink()
    result.price = price
    result.name = name
    return result
# ─── ошибка ───
def make_drink(name, price):
    drink = Drink()
    drink.name = name
    drink.price = price
# ─── ошибка ───
SHARED = Drink()


def make_drink(name, price):
    SHARED.name = name
    SHARED.price = price
    return SHARED
