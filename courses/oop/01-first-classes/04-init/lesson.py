# Урок oop-init. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% init
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


latte = Product("Латте", 220)
tea = Product("Чай", 120)
print(latte.name, latte.price)
print(tea.name, tea.price)

# %% steps
class Cup:
    def __init__(self, volume):
        print(f"__init__: заполняю экземпляр, volume = {volume}")
        self.volume = volume


print("до вызова Cup")
big = Cup(400)
print("после вызова Cup:", big.volume)

# %% missing [raises=TypeError]
Product("Чай")

# %% drink-init [exercise]
class Drink:
    def __init__(self, name, price):
        self.name = name
        self.price = price
# ─── заготовка ───
class Drink:
    def __init__(self, name, price):
        ...  # запишите атрибуты name и price
# ─── проверка ───
def _make(*args):
    "создаёт Drink; если вызов не удался — None и текст ошибки"
    try:
        return Drink(*args), ""
    except TypeError as e:
        return None, str(e)


def test_create():
    "Drink(\"Раф\", 260) создаёт экземпляр"
    drink, error = _make("Раф", 260)
    assert drink is not None, f"Drink(\"Раф\", 260) не создаётся: {error}. Первый параметр __init__ — self, за ним name и price"


def test_attributes():
    "атрибуты name и price — из аргументов"
    drink, error = _make("Раф", 260)
    assert drink is not None, "сначала исправьте создание экземпляра (проверка выше)"
    assert hasattr(drink, "name") and hasattr(drink, "price"), "у экземпляра нет атрибутов name и price — внутри __init__ пишите self.name = name, а не name = name"
    assert drink.name == "Раф" and drink.price == 260, f"у Drink(\"Раф\", 260) name = {drink.name!r}, price = {drink.price!r}"


def test_independent():
    "у двух экземпляров — свои атрибуты"
    a, _ = _make("Раф", 260)
    b, _ = _make("Чай", 120)
    assert a is not None and b is not None, "сначала исправьте создание экземпляра (проверка выше)"
    assert getattr(a, "price", None) == 260 and getattr(b, "price", None) == 120, "у Drink(\"Раф\", 260) и Drink(\"Чай\", 120) должны быть разные цены — берите их из параметров"
# ─── другое решение ───
class Drink:
    def __init__(self, name, price):
        self.price = price
        self.name = name
# ─── ошибка ───
class Drink:
    def __init__(self, name, price):
        name = name
        price = price
# ─── ошибка ───
class Drink:
    def __init__(name, price):
        name.price = price
# ─── ошибка ───
class Drink:
    def __init__(self, name, price):
        self.name = "Раф"
        self.price = 260

# %% no-self [raises=AttributeError]
class Bun:
    def __init__(self, name):
        name = name  # забыли self.


bun = Bun("Круассан")
print(bun.name)

# %% init-quiz [quiz]
created = []


class Cup:
    def __init__(self):
        created.append("новая чашка")


a = Cup()
b = Cup()
c = a
print(len(created))

# %% defaults
class Product:
    def __init__(self, name, price, volume=250):
        self.name = name
        self.price = price
        self.volume = volume


print(Product("Капучино", 220).volume)
print(Product("Капучино", 260, 400).volume)

# %% size [exercise]
class Drink:
    def __init__(self, name, price, size="M"):
        self.name = name
        self.price = price
        self.size = size
# ─── заготовка ───
class Drink:
    def __init__(self, name, price):  # добавьте параметр size
        ...
# ─── проверка ───
def test_default():
    "Drink(\"Чай\", 120) — размер M"
    try:
        tea = Drink("Чай", 120)
    except TypeError:
        assert False, "Drink(\"Чай\", 120) не создаётся без размера — дайте параметру size значение по умолчанию: size=\"M\""
    assert hasattr(tea, "size"), "у экземпляра нет атрибута size — запишите его в __init__: self.size = size"
    assert tea.size == "M", f"у Drink(\"Чай\", 120) size = {tea.size!r}, а по умолчанию нужно \"M\""
    assert getattr(tea, "name", None) == "Чай" and getattr(tea, "price", None) == 120, "name и price по-прежнему берутся из аргументов"


def test_given():
    "Drink(\"Чай\", 150, \"L\") — размер L"
    try:
        tea = Drink("Чай", 150, "L")
    except TypeError:
        assert False, "Drink(\"Чай\", 150, \"L\") не создаётся — добавьте в __init__ третий параметр size"
    assert getattr(tea, "size", None) == "L", f"у Drink(\"Чай\", 150, \"L\") size = {getattr(tea, 'size', None)!r}, а нужно \"L\" — берите размер из параметра"
# ─── другое решение ───
class Drink:
    def __init__(self, name, price, size=None):
        self.name = name
        self.price = price
        if size:
            self.size = size
        else:
            self.size = "M"
# ─── ошибка ───
class Drink:
    def __init__(self, name, price, size="M"):
        self.name = name
        self.price = price
        self.size = "M"
# ─── ошибка ───
class Drink:
    def __init__(self, name, price, size):
        self.name = name
        self.price = price
        self.size = size

# %% computed
class Pastry:
    def __init__(self, name, price, weight):
        self.name = name
        self.price = price
        self.weight = weight
        self.per_100g = round(price / weight * 100)  # вычислено из аргументов
        self.sold = 0  # начальное значение, одинаковое для всех


croissant = Pastry("Круассан", 140, 70)
print(croissant.per_100g, croissant.sold)

# %% customer [exercise]
class Customer:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.points = 0
# ─── заготовка ───
class Customer:
    def __init__(self, name, phone):
        ...
# ─── проверка ───
def test_create():
    "Customer(имя, телефон) создаётся с двумя аргументами"
    try:
        Customer("Анна", "+7 900 111-22-33")
    except TypeError as e:
        assert False, f"Customer(\"Анна\", \"+7 900 111-22-33\") не создаётся: {e}. Баллы не передаются при создании — их нет среди параметров"


def test_attributes():
    "name, phone и points = 0"
    try:
        anna = Customer("Анна", "+7 900 111-22-33")
    except TypeError:
        assert False, "сначала исправьте создание экземпляра (проверка выше)"
    assert getattr(anna, "name", None) == "Анна", "name берётся из первого аргумента"
    assert getattr(anna, "phone", None) == "+7 900 111-22-33", "phone берётся из второго аргумента"
    assert hasattr(anna, "points"), "у покупателя нет атрибута points — запишите в __init__ self.points = 0"
    assert anna.points == 0, f"у нового покупателя points = {anna.points!r}, а нужно 0"
# ─── другое решение ───
class Customer:
    def __init__(self, name, phone, points=0):
        self.name = name
        self.phone = phone
        self.points = points
# ─── ошибка ───
class Customer:
    def __init__(self, name, phone, points):
        self.name = name
        self.phone = phone
        self.points = points
# ─── ошибка ───
class Customer:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

# %% menu [exercise]
data = [("Эспрессо", 150), ("Капучино", 220), ("Раф", 260)]
menu = [Drink(name, price) for name, price in data]
# ─── заготовка ───
data = [("Эспрессо", 150), ("Капучино", 220), ("Раф", 260)]
menu = ...
# ─── проверка ───
def test_menu():
    "menu — список из трёх экземпляров Drink"
    assert isinstance(menu, list), f"menu — это {type(menu).__name__}, а нужен список"
    assert len(menu) == 3, f"в menu {len(menu)} элементов, а пар в data три"
    assert all(isinstance(d, Drink) for d in menu), "в menu должны быть экземпляры Drink, а не пары из data: Drink(name, price)"


def test_values():
    "названия и цены — из data, по порядку"
    assert isinstance(menu, list) and all(isinstance(d, Drink) for d in menu), "сначала исправьте список (проверка выше)"
    names = [d.name for d in menu]
    assert names == ["Эспрессо", "Капучино", "Раф"], f"названия в menu: {names}"
    assert [d.price for d in menu] == [150, 220, 260], f"цены в menu: {[d.price for d in menu]}"
    assert len(set(map(id, menu))) == 3, "в menu один и тот же экземпляр несколько раз — создавайте новый для каждой пары"
# ─── другое решение ───
data = [("Эспрессо", 150), ("Капучино", 220), ("Раф", 260)]
menu = []
for pair in data:
    menu.append(Drink(pair[0], pair[1]))
# ─── ошибка ───
data = [("Эспрессо", 150), ("Капучино", 220), ("Раф", 260)]
menu = data
