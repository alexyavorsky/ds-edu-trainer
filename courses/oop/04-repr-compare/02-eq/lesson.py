# Урок oop-eq. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% eq
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price


a = Product("Латте", 220)
b = Product("Латте", 220)
print(a == b, a is b)
print(a != Product("Латте", 250))

# %% foreign [raises=AttributeError]
a == "Латте"

# %% not-implemented
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"

    def __eq__(self, other):
        if not isinstance(other, Product):
            return NotImplemented  # «не умею» — пусть ответит другой объект
        return self.name == other.name and self.price == other.price


latte = Product("Латте", 220)
print(latte == Product("Латте", 220))
print(latte == "Латте", latte == 220)

# %% false-vs-ni
class Ticket:
    """Строка кассового чека: знает, какому товару соответствует."""

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if isinstance(other, (Product, StrictProduct)):
            return self.name == other.name
        return NotImplemented


class StrictProduct:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __eq__(self, other):
        if not isinstance(other, StrictProduct):
            return False  # ошибка: не даёт ответить Ticket
        return self.name == other.name and self.price == other.price


ticket = Ticket("Латте")
print(Product("Латте", 220) == ticket)  # Python спросил Ticket — True
print(StrictProduct("Латте", 220) == ticket)  # ответ False, Ticket не спросили

# %% drink-eq [exercise]
class Drink:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __eq__(self, other):
        if not isinstance(other, Drink):
            return NotImplemented
        return self.name.lower() == other.name.lower() and self.price == other.price
# ─── заготовка ───
class Drink:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __eq__(self, other):
        ...
# ─── проверка ───
def test_equal():
    "напитки с одинаковыми названием и ценой равны"
    assert "__eq__" in Drink.__dict__, "в классе нет __eq__ — объявите его"
    a, b = Drink("Латте", 220), Drink("Латте", 220)
    assert (a == b) is True, "Drink(\"Латте\", 220) == Drink(\"Латте\", 220) должно быть True"
    assert a is not b, "проверка создаёт два разных объекта"
    assert Drink("латте", 220) == Drink("Латте", 220), "«латте» и «Латте» по одной цене должны быть равны — сравнивайте названия без учёта регистра: lower()"


def test_different():
    "другая цена или название — не равны"
    assert "__eq__" in Drink.__dict__, "сначала объявите __eq__"
    assert Drink("Латте", 220) != Drink("Латте", 250), "у напитков разные цены, а они равны — сравнивайте и цену"
    assert Drink("Латте", 220) != Drink("Раф", 220), "у напитков разные названия, а они равны — сравнивайте и название"


def test_foreign():
    "чужой тип — NotImplemented"
    assert "__eq__" in Drink.__dict__, "сначала объявите __eq__"
    try:
        got = Drink.__dict__["__eq__"](Drink("Латте", 220), "Латте")
    except AttributeError:
        assert False, "сравнение со строкой падает с AttributeError — сначала проверьте тип: isinstance(other, Drink)"
    assert got is not False, "для чужого типа __eq__ вернул False, а нужно return NotImplemented — пусть ответит второй объект"
    assert got is NotImplemented, f"для чужого типа __eq__ вернул {got!r}, а нужно NotImplemented"
    assert (Drink("Латте", 220) == "Латте") is False, "сравнение со строкой должно давать False"
# ─── другое решение ───
class Drink:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __eq__(self, other):
        if isinstance(other, Drink):
            return (self.name.casefold(), self.price) == (other.name.casefold(), other.price)
        return NotImplemented
# ─── ошибка ───
class Drink:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __eq__(self, other):
        if not isinstance(other, Drink):
            return False
        return self.name.lower() == other.name.lower() and self.price == other.price
# ─── ошибка ───
class Drink:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __eq__(self, other):
        if not isinstance(other, Drink):
            return NotImplemented
        return self.name.lower() == other.name.lower()
# ─── ошибка ───
class Drink:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __eq__(self, other):
        if not isinstance(other, Drink):
            return NotImplemented
        return self.name == other.name and self.price == other.price

# %% unhashable [raises=TypeError]
print(Product.__hash__)  # __eq__ есть — хеш отключён
{latte}

# %% hash
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"

    def __eq__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.name == other.name and self.price == other.price

    def __hash__(self):
        return hash((self.name, self.price))


shelf = {Product("Латте", 220), Product("Латте", 220), Product("Чай", 120)}
print(len(shelf))
print(Product("Латте", 220) in shelf)
stock = {Product("Чай", 120): 30}
print(stock[Product("Чай", 120)])

# %% customer [exercise]
class Customer:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def __eq__(self, other):
        if not isinstance(other, Customer):
            return NotImplemented
        return self.phone == other.phone

    def __hash__(self):
        return hash(self.phone)
# ─── заготовка ───
class Customer:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def __eq__(self, other):
        ...

    def __hash__(self):
        ...
# ─── проверка ───
def test_eq():
    "равны по телефону, имя не важно"
    assert "__eq__" in Customer.__dict__, "в классе нет __eq__"
    anna, anya = Customer("Анна", "+7 900 111-22-33"), Customer("Аня", "+7 900 111-22-33")
    assert anna == anya, "у Анны и Ани один телефон — это один покупатель, они должны быть равны"
    assert anna != Customer("Анна", "+7 900 999-88-77"), "у покупателей разные телефоны — они не равны, даже если имя одно"


def test_foreign():
    "чужой тип — NotImplemented"
    try:
        got = Customer.__dict__["__eq__"](Customer("Анна", "1"), "1")
    except AttributeError:
        assert False, "сравнение со строкой падает — сначала проверьте тип: isinstance(other, Customer)"
    assert got is NotImplemented, f"для чужого типа __eq__ вернул {got!r}, а нужно NotImplemented"


def test_hash():
    "равные покупатели — один элемент set"
    try:
        group = {Customer("Анна", "1"), Customer("Аня", "1"), Customer("Борис", "2")}
    except TypeError:
        assert False, "покупателя нельзя положить в set — объявите __hash__"
    assert len(group) == 2, f"в set из Анны, Ани (тот же телефон) и Бориса {len(group)} элементов, а нужно 2 — хеш должен зависеть только от телефона"
    assert hash(Customer("Анна", "1")) == hash(Customer("Аня", "1")), "у равных покупателей хеши разные — считайте хеш из телефона"
# ─── другое решение ───
class Customer:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def __eq__(self, other):
        if isinstance(other, Customer):
            return self.phone == other.phone
        return NotImplemented

    def __hash__(self):
        return hash(("Customer", self.phone))
# ─── ошибка ───
class Customer:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def __eq__(self, other):
        if not isinstance(other, Customer):
            return NotImplemented
        return self.phone == other.phone

    def __hash__(self):
        return hash((self.name, self.phone))
# ─── ошибка ───
class Customer:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def __eq__(self, other):
        if not isinstance(other, Customer):
            return NotImplemented
        return self.phone == other.phone

# %% lost
latte = Product("Латте", 220)
basket = {latte}
latte.price = 250  # хеш изменился, а в set объект лежит по старому
print(latte in basket)
print(len(basket), list(basket))

# %% visits [exercise]
visits = [
    Customer("Анна", "+7 900 111-22-33"),
    Customer("Борис", "+7 900 222-33-44"),
    Customer("Аня", "+7 900 111-22-33"),
    Customer("Вера", "+7 900 333-44-55"),
    Customer("Анна", "+7 900 111-22-33"),
]
n_unique = len(set(visits))
per_customer = {}
for c in visits:
    per_customer[c] = per_customer.get(c, 0) + 1
# ─── заготовка ───
visits = [
    Customer("Анна", "+7 900 111-22-33"),
    Customer("Борис", "+7 900 222-33-44"),
    Customer("Аня", "+7 900 111-22-33"),
    Customer("Вера", "+7 900 333-44-55"),
    Customer("Анна", "+7 900 111-22-33"),
]
n_unique = ...
per_customer = ...
# ─── проверка ───
def test_unique():
    "n_unique — разных покупателей"
    assert n_unique != 5, "5 — это число визитов; Анна и Аня — один человек (телефон один): посчитайте len(set(visits))"
    assert n_unique != 4, "4 — это число разных имён, а покупатель определяется телефоном"
    assert n_unique == 3, f"n_unique = {n_unique!r}, а разных покупателей 3"


def test_counts():
    "per_customer — визиты каждого"
    assert isinstance(per_customer, dict), f"per_customer — это {type(per_customer).__name__}, а нужен словарь"
    assert len(per_customer) == 3, f"в per_customer {len(per_customer)} ключей, а разных покупателей 3 — ключи должны быть сами покупатели"
    got = per_customer.get(Customer("?", "+7 900 111-22-33"))
    assert got == 3, f"у покупателя с телефоном +7 900 111-22-33 {got!r} визитов, а он приходил трижды"
# ─── другое решение ───
visits = [
    Customer("Анна", "+7 900 111-22-33"),
    Customer("Борис", "+7 900 222-33-44"),
    Customer("Аня", "+7 900 111-22-33"),
    Customer("Вера", "+7 900 333-44-55"),
    Customer("Анна", "+7 900 111-22-33"),
]
per_customer = {}
for c in visits:
    if c in per_customer:
        per_customer[c] += 1
    else:
        per_customer[c] = 1
n_unique = len(per_customer)
# ─── ошибка ───
visits = [
    Customer("Анна", "+7 900 111-22-33"),
    Customer("Борис", "+7 900 222-33-44"),
    Customer("Аня", "+7 900 111-22-33"),
    Customer("Вера", "+7 900 333-44-55"),
    Customer("Анна", "+7 900 111-22-33"),
]
n_unique = len(set(c.name for c in visits))
per_customer = {}
for c in visits:
    per_customer[c.name] = per_customer.get(c.name, 0) + 1
