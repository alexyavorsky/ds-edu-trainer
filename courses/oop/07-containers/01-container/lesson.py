# Урок oop-container. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% len
class Ticket:
    def __init__(self, number, lines):
        self.number = number
        self.lines = list(lines)

    def __len__(self):
        return len(self.lines)


full = Ticket(17, ["латте", "круассан"])
empty = Ticket(18, [])
print(len(full), len(empty))
for ticket in [full, empty]:
    if ticket:
        print(f"заказ №{ticket.number}: {len(ticket)} поз.")
    else:
        print(f"заказ №{ticket.number} пуст")

# %% cart-len [exercise]
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"


class Cart:
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)

    def __len__(self):
        return len(self.items)
# ─── заготовка ───
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"


class Cart:
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)

    def __len__(self):
        ...
# ─── проверка ───
def test_len():
    "len — число товаров"
    cart = Cart()
    assert len(cart) == 0, "у пустой корзины len должен быть 0"
    cart.add(Product("Латте", 220))
    cart.add(Product("Чай", 120))
    try:
        n = len(cart)
    except TypeError as e:
        assert False, f"len(cart) не работает: {e}. __len__ должен вернуть целое число — число товаров"
    assert n == 2, f"в корзине два товара, а len = {n}"


def test_bool():
    "пустая корзина — ложь"
    cart = Cart()
    assert not cart, "пустая корзина должна быть «ложью» — это даёт __len__, возвращающий 0"
    cart.add(Product("Чай", 120))
    assert cart, "корзина с товаром должна быть «истиной»"
# ─── другое решение ───
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"


class Cart:
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)

    def __len__(self):
        count = 0
        for _ in self.items:
            count += 1
        return count
# ─── ошибка ───
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"


class Cart:
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)

    def __len__(self):
        return sum(p.price for p in self.items)

# %% machine [exercise]
class CoffeeMachine:
    def __init__(self, water, beans):
        self.water = water
        self.beans = beans

    def __bool__(self):
        return self.water > 0 and self.beans > 0
# ─── заготовка ───
class CoffeeMachine:
    def __init__(self, water, beans):
        self.water = water
        self.beans = beans

    def __bool__(self):
        ...
# ─── проверка ───
def test_ready():
    "есть вода и зёрна — True"
    try:
        got = bool(CoffeeMachine(1500, 300))
    except TypeError as e:
        assert False, f"bool(machine) не работает: {e}. __bool__ должен вернуть True или False"
    assert got is True, "в машине есть и вода, и зёрна — bool(machine) должен быть True"


def test_not_ready():
    "нет воды или зёрен — False"
    assert not CoffeeMachine(0, 300), "без воды машина не готова"
    assert not CoffeeMachine(1500, 0), "без зёрен машина не готова — проверяйте оба условия через and"
# ─── другое решение ───
class CoffeeMachine:
    def __init__(self, water, beans):
        self.water = water
        self.beans = beans

    def __bool__(self):
        if self.water <= 0:
            return False
        return self.beans > 0
# ─── ошибка ───
class CoffeeMachine:
    def __init__(self, water, beans):
        self.water = water
        self.beans = beans

    def __bool__(self):
        return self.water > 0 or self.beans > 0

# %% getitem
class Schedule:
    def __init__(self, shifts):
        self._shifts = dict(shifts)  # день → бариста

    def __getitem__(self, day):
        if day not in self._shifts:
            raise KeyError(day)
        return self._shifts[day]


week = Schedule({"пн": "Анна", "вт": "Борис", "ср": "Анна"})
print(week["вт"])
try:
    week["вс"]
except KeyError as error:
    print("нет смены:", error)

# %% contains
class OpenDays:
    def __init__(self, days):
        self._days = list(days)

    def __contains__(self, day):
        return day in self._days


open_days = OpenDays(["пн", "вт", "ср", "чт", "пт", "сб"])
print("сб" in open_days, "вс" in open_days)

# %% menu [exercise]
class Menu:
    def __init__(self, products):
        self._items = list(products)

    def __getitem__(self, name):
        for p in self._items:
            if p.name == name:
                return p
        raise KeyError(name)

    def __contains__(self, name):
        for p in self._items:
            if p.name == name:
                return True
        return False
# ─── заготовка ───
class Menu:
    def __init__(self, products):
        self._items = list(products)

    def __getitem__(self, name):
        ...

    def __contains__(self, name):
        ...
# ─── проверка ───
def _menu():
    return Menu([Product("Латте", 220), Product("Чай", 120)])


def test_getitem():
    "menu[название] — товар"
    menu = _menu()
    got = menu["Чай"]
    assert got is not None, "menu[\"Чай\"] вернул None — верните найденный товар"
    assert isinstance(got, Product) and got.name == "Чай", f"menu[\"Чай\"] = {got!r}, а нужен товар «Чай»"


def test_missing():
    "нет товара — KeyError"
    try:
        got = _menu()["Какао"]
    except KeyError:
        return
    assert False, f"menu[\"Какао\"] вернул {got!r}, а для отсутствующего товара нужен KeyError: raise KeyError(name)"


def test_contains():
    "in — по названию"
    menu = _menu()
    assert ("Латте" in menu) is True, "\"Латте\" in menu должно быть True"
    assert ("Какао" in menu) is False, "\"Какао\" in menu должно быть False"
# ─── другое решение ───
class Menu:
    def __init__(self, products):
        self._items = list(products)

    def __getitem__(self, name):
        found = [p for p in self._items if p.name == name]
        if not found:
            raise KeyError(name)
        return found[0]

    def __contains__(self, name):
        try:
            self[name]
        except KeyError:
            return False
        return True
# ─── ошибка ───
class Menu:
    def __init__(self, products):
        self._items = list(products)

    def __getitem__(self, name):
        for p in self._items:
            if p.name == name:
                return p
        return None

    def __contains__(self, name):
        for p in self._items:
            if p.name == name:
                return True
        return False
# ─── ошибка ───
class Menu:
    def __init__(self, products):
        self._items = list(products)

    def __getitem__(self, name):
        for p in self._items:
            if p.name == name:
                return p
        raise KeyError(name)

    def __contains__(self, name):
        return name in self._items

# %% bool-quiz [quiz]
print(bool(Cart()))
