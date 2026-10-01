# Урок oop-property. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% property
class Order:
    def __init__(self, number):
        self._number = number
        self._status = "новый"

    @property
    def number(self):
        return self._number

    @property
    def status(self):
        return self._status

    def pay(self):
        if self._status == "оплачен":
            return False  # дважды не оплачивают
        self._status = "оплачен"
        return True


order = Order(17)
print(order.number, order.status)  # без скобок
print(order.pay(), order.status)
print(order.pay(), order.status)

# %% read-only [raises=AttributeError]
order.status = "отменён"

# %% balance [exercise]
class GiftCard:
    def __init__(self, amount):
        self._balance = amount

    @property
    def balance(self):
        return self._balance

    def pay(self, amount):
        if amount > self._balance:
            return False
        self._balance -= amount
        return True

    def top_up(self, amount):
        if amount <= 0:
            return False
        self._balance += amount
        return True
# ─── заготовка ───
class GiftCard:
    def __init__(self, amount):
        self._balance = amount

    def balance(self):
        ...

    def pay(self, amount):
        if amount > self._balance:
            return False
        self._balance -= amount
        return True

    def top_up(self, amount):
        if amount <= 0:
            return False
        self._balance += amount
        return True
# ─── проверка ───
def test_is_property():
    "balance — свойство"
    assert "balance" in GiftCard.__dict__, "в классе нет balance — объявите его"
    assert isinstance(GiftCard.__dict__["balance"], property), "balance — обычный метод; поставьте над ним декоратор @property"


def test_value():
    "card.balance — текущий баланс"
    assert isinstance(GiftCard.__dict__.get("balance"), property), "сначала сделайте balance свойством"
    card = GiftCard(500)
    assert card.balance == 500, f"у GiftCard(500) balance = {card.balance!r}, а нужно 500 — верните self._balance"
    card.pay(200)
    assert card.balance == 300, f"после pay(200) balance = {card.balance!r}, а нужно 300"


def test_read_only():
    "записать в balance нельзя"
    assert isinstance(GiftCard.__dict__.get("balance"), property), "сначала сделайте balance свойством"
    card = GiftCard(500)
    try:
        card.balance = 10 ** 6
    except AttributeError:
        return
    assert False, "в balance удалось записать значение — у свойства не должно быть сеттера"
# ─── другое решение ───
class GiftCard:
    def __init__(self, amount):
        self._balance = amount

    def _get_balance(self):
        return self._balance

    balance = property(_get_balance)

    def pay(self, amount):
        if amount > self._balance:
            return False
        self._balance -= amount
        return True

    def top_up(self, amount):
        if amount <= 0:
            return False
        self._balance += amount
        return True
# ─── ошибка ───
class GiftCard:
    def __init__(self, amount):
        self._balance = amount
        self.balance = amount

    def pay(self, amount):
        if amount > self._balance:
            return False
        self._balance -= amount
        return True

    def top_up(self, amount):
        if amount <= 0:
            return False
        self._balance += amount
        return True

# %% call-property [raises=TypeError]
order.number()

# %% cart [exercise]
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Cart:
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)

    @property
    def total(self):
        return sum(p.price for p in self.items)

    @property
    def count(self):
        return len(self.items)
# ─── заготовка ───
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Cart:
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)

    # свойства total и count
# ─── проверка ───
def test_properties():
    "total и count — свойства"
    for name in ["total", "count"]:
        assert name in Cart.__dict__, f"в классе Cart нет {name} — объявите его с декоратором @property"
        assert isinstance(Cart.__dict__[name], property), f"{name} — обычный метод; поставьте над ним @property"


def test_values():
    "сумма и число товаров"
    assert all(isinstance(Cart.__dict__.get(n), property) for n in ["total", "count"]), "сначала объявите свойства total и count"
    cart = Cart()
    assert cart.total == 0 and cart.count == 0, f"у пустой корзины total = {cart.total!r}, count = {cart.count!r}, а нужно 0 и 0"
    cart.add(Product("Чай", 120))
    cart.add(Product("Раф", 260))
    assert cart.count == 2, f"в корзине 2 товара, а count = {cart.count!r}"
    assert cart.total == 380, f"чай и раф стоят 380, а total = {cart.total!r}"
# ─── другое решение ───
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Cart:
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)

    @property
    def count(self):
        return len(self.items)

    @property
    def total(self):
        result = 0
        for p in self.items:
            result += p.price
        return result
# ─── ошибка ───
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Cart:
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)

    def total(self):
        return sum(p.price for p in self.items)

    def count(self):
        return len(self.items)
# ─── ошибка ───
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Cart:
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)

    @property
    def total(self):
        return sum(p.price for p in self.items)

    @property
    def count(self):
        return sum(p.price for p in self.items)

# %% size [exercise]
class Drink:
    def __init__(self, name, volume):
        self.name = name
        self.volume = volume

    @property
    def size(self):
        if self.volume <= 250:
            return "S"
        if self.volume <= 350:
            return "M"
        return "L"
# ─── заготовка ───
class Drink:
    def __init__(self, name, volume):
        self.name = name
        self.volume = volume

    @property
    def size(self):
        ...
# ─── проверка ───
def test_sizes():
    "S, M и L по объёму, границы включительно"
    assert isinstance(Drink.__dict__.get("size"), property), "size должен оставаться свойством — с декоратором @property"
    cases = [(200, "S"), (250, "S"), (300, "M"), (350, "M"), (400, "L")]
    for volume, expected in cases:
        got = Drink("Латте", volume).size
        assert got == expected, f"при объёме {volume} мл size = {got!r}, а нужно {expected!r}"


def test_follows_volume():
    "размер меняется вместе с объёмом"
    cup = Drink("Латте", 250)
    cup.volume = 400
    assert cup.size == "L", f"объём стал 400 мл, а size всё ещё {cup.size!r} — вычисляйте размер в свойстве при каждом чтении, а не один раз в __init__"
# ─── другое решение ───
class Drink:
    LIMITS = [(250, "S"), (350, "M")]

    def __init__(self, name, volume):
        self.name = name
        self.volume = volume

    @property
    def size(self):
        for limit, label in self.LIMITS:
            if self.volume <= limit:
                return label
        return "L"
# ─── ошибка ───
class Drink:
    def __init__(self, name, volume):
        self.name = name
        self.volume = volume
        if volume <= 250:
            self._size = "S"
        elif volume <= 350:
            self._size = "M"
        else:
            self._size = "L"

    @property
    def size(self):
        return self._size
# ─── ошибка ───
class Drink:
    def __init__(self, name, volume):
        self.name = name
        self.volume = volume

    @property
    def size(self):
        if self.volume < 250:
            return "S"
        if self.volume < 350:
            return "M"
        return "L"
