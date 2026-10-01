# Урок oop-p2-cart. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% product
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


latte = Product("Латте", 220)
print(latte.name, latte.price)

# %% cart [exercise]
class Cart:
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)

    def total(self):
        return sum(p.price for p in self.items)
# ─── заготовка ───
class Cart:
    def __init__(self):
        ...

    def add(self, product):
        ...

    def total(self):
        ...
# ─── проверка ───
def _cart():
    try:
        return Cart()
    except TypeError as e:
        assert False, f"Cart() не создаётся: {e}. У __init__ корзины только параметр self"


def test_empty():
    "новая корзина пустая, сумма 0"
    cart = _cart()
    assert hasattr(cart, "items"), "у корзины нет атрибута items — создайте в __init__ self.items = []"
    assert cart.items == [], f"в новой корзине items = {cart.items}, а нужен пустой список"
    assert cart.total() == 0, f"у пустой корзины total() = {cart.total()!r}, а нужно 0"


def test_add_total():
    "add кладёт товары, total считает сумму"
    cart = _cart()
    assert hasattr(cart, "items"), "сначала создайте items в __init__"
    tea, raf = Product("Чай", 120), Product("Раф", 260)
    cart.add(tea)
    cart.add(raf)
    assert len(cart.items) == 2 and cart.items[0] is tea, "add должен класть в items сам товар"
    got = cart.total()
    assert got is not None, "total() ничего не возвращает — нужен return"
    assert got == 380, f"total() = {got!r}, а чай и раф стоят 380"


def test_independent():
    "у двух корзин — свои списки"
    a, b = _cart(), _cart()
    assert hasattr(a, "items"), "сначала создайте items в __init__"
    a.add(Product("Чай", 120))
    assert b.items == [], "товар из одной корзины появился в другой — список должен создаваться в __init__, а не в теле класса"
# ─── другое решение ───
class Cart:
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items = self.items + [product]

    def total(self):
        result = 0
        for p in self.items:
            result += p.price
        return result
# ─── ошибка ───
class Cart:
    items = []

    def add(self, product):
        self.items.append(product)

    def total(self):
        return sum(p.price for p in self.items)
# ─── ошибка ───
class Cart:
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)

    def total(self):
        return len(self.items)

# %% more [exercise]
class Cart:
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)

    def total(self):
        return sum(p.price for p in self.items)

    def remove(self, name):
        for p in self.items:
            if p.name == name:
                self.items.remove(p)
                return True
        return False

    def most_expensive(self):
        if not self.items:
            return None
        best = self.items[0]
        for p in self.items:
            if p.price > best.price:
                best = p
        return best
# ─── заготовка ───
class Cart:
    # скопируйте сюда __init__, add и total из шага 1

    def remove(self, name):
        ...

    def most_expensive(self):
        ...
# ─── проверка ───
def _filled():
    "корзина: чай, раф, чай"
    try:
        cart = Cart()
    except TypeError:
        assert False, "Cart() не создаётся — скопируйте в класс __init__ из шага 1"
    for method in ["add", "total"]:
        assert hasattr(cart, method), f"в классе нет метода {method} — скопируйте класс из шага 1 целиком"
    assert getattr(cart, "items", None) == [], "у новой корзины должен быть пустой список items — в скопированном классе ошибка из шага 1"
    tea1, raf, tea2 = Product("Чай", 120), Product("Раф", 260), Product("Чай", 120)
    for p in [tea1, raf, tea2]:
        cart.add(p)
    assert len(cart.items) == 3 and cart.total() == 500, "add и total работают не так, как в шаге 1 — в скопированном классе ошибка из шага 1"
    return cart, tea1, raf, tea2


def test_remove():
    "remove убирает первый товар с этим названием"
    cart, tea1, raf, tea2 = _filled()
    got = cart.remove("Чай")
    assert got is True, f"remove(\"Чай\") вернул {got!r}, а товар был в корзине — нужно True"
    assert len(cart.items) == 2, f"после remove(\"Чай\") в корзине {len(cart.items)} товаров, а должно остаться 2 — уберите только первый чай"
    assert cart.items[0] is raf and cart.items[1] is tea2, "убрать нужно первый чай, остальные товары — на своих местах"


def test_remove_missing():
    "нет товара — False, корзина не меняется"
    cart, *_ = _filled()
    got = cart.remove("Какао")
    assert got is False, f"remove(\"Какао\") вернул {got!r}, а какао в корзине нет — нужно False"
    assert len(cart.items) == 3, "remove несуществующего товара изменил корзину"


def test_most_expensive():
    "most_expensive — сам самый дорогой товар"
    cart, tea1, raf, tea2 = _filled()
    got = cart.most_expensive()
    assert not isinstance(got, (int, float)), f"most_expensive() вернул число {got!r}, а нужен сам товар"
    assert got is raf, "most_expensive() вернул не тот товар: самый дорогой — раф"
    assert Cart().most_expensive() is None, "у пустой корзины most_expensive() должен вернуть None"
# ─── другое решение ───
class Cart:
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)

    def total(self):
        return sum(p.price for p in self.items)

    def remove(self, name):
        for i in range(len(self.items)):
            if self.items[i].name == name:
                del self.items[i]
                return True
        return False

    def most_expensive(self):
        if len(self.items) == 0:
            return None
        return max(self.items, key=lambda p: p.price)
# ─── ошибка ───
class Cart:
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)

    def total(self):
        return sum(p.price for p in self.items)

    def remove(self, name):
        before = len(self.items)
        self.items = [p for p in self.items if p.name != name]
        return len(self.items) < before

    def most_expensive(self):
        if not self.items:
            return None
        return max(self.items, key=lambda p: p.price)
# ─── ошибка ───
class Cart:
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)

    def total(self):
        return sum(p.price for p in self.items)

    def remove(self, name):
        for p in self.items:
            if p.name == name:
                self.items.remove(p)
                return True
        return False

    def most_expensive(self):
        if not self.items:
            return None
        return max(p.price for p in self.items)

# %% two-carts [exercise]
latte = Product("Латте", 220)
croissant = Product("Круассан", 140)
tea = Product("Чай", 120)

anna = Cart()
anna.add(latte)
anna.add(croissant)
boris = Cart()
boris.add(tea)
boris.add(latte)
anna_total = anna.total()
boris_total = boris.total()
# ─── заготовка ───
latte = Product("Латте", 220)
croissant = Product("Круассан", 140)
tea = Product("Чай", 120)

anna = ...
boris = ...
anna_total = ...
boris_total = ...
# ─── проверка ───
def test_carts():
    "anna и boris — две разные корзины"
    assert isinstance(anna, Cart) and isinstance(boris, Cart), "anna и boris должны быть экземплярами Cart: anna = Cart()"
    assert anna is not boris, "anna и boris — одна и та же корзина; создайте две: два раза Cart()"


def test_contents():
    "товары в корзинах — те самые объекты"
    assert isinstance(anna, Cart) and isinstance(boris, Cart), "сначала создайте корзины"
    assert [p.name for p in anna.items] == ["Латте", "Круассан"], f"в корзине Анны {[p.name for p in anna.items]}"
    assert [p.name for p in boris.items] == ["Чай", "Латте"], f"в корзине Бориса {[p.name for p in boris.items]}"
    assert anna.items[0] is latte and boris.items[1] is latte, "в обеих корзинах должен лежать один и тот же товар latte — не создавайте новый Product(\"Латте\", …)"


def test_totals():
    "anna_total и boris_total"
    assert anna_total == 360, f"anna_total = {anna_total!r}, а латте и круассан стоят 360"
    assert boris_total == 340, f"boris_total = {boris_total!r}, а чай и латте стоят 340"
# ─── другое решение ───
latte = Product("Латте", 220)
croissant = Product("Круассан", 140)
tea = Product("Чай", 120)

anna, boris = Cart(), Cart()
for p in [latte, croissant]:
    anna.add(p)
for p in [tea, latte]:
    boris.add(p)
anna_total, boris_total = anna.total(), boris.total()
# ─── ошибка ───
latte = Product("Латте", 220)
croissant = Product("Круассан", 140)
tea = Product("Чай", 120)

anna = Cart()
anna.add(latte)
anna.add(croissant)
boris = Cart()
boris.add(tea)
boris.add(Product("Латте", 220))
anna_total = anna.total()
boris_total = boris.total()

# %% new-price [exercise]
latte.price = 250
anna_new = anna.total()
boris_new = boris.total()
# ─── заготовка ───
anna_new = ...
boris_new = ...
# ─── проверка ───
def test_price():
    "цена latte — 250"
    assert latte.price == 250, f"latte.price = {latte.price!r}, а нужно 250"
    assert anna.items and anna.items[0] is latte, "в latte теперь не тот товар, что лежит в корзинах: похоже, latte присвоили новый объект. Нажмите «Выполнить все выше» и меняйте цену у существующего товара"


def test_totals():
    "суммы обеих корзин выросли"
    assert anna_new == 390, f"anna_new = {anna_new!r}, а после подорожания латте корзина Анны стоит 390"
    assert boris_new == 370, f"boris_new = {boris_new!r}, а корзина Бориса стоит 370"
    assert anna.total() == 390, "в корзине Анны должна быть новая цена — меняйте цену у самого latte, а не создавайте новый товар"
# ─── другое решение ───
latte.price = 220 + 30
anna_new, boris_new = anna.total(), boris.total()
# ─── ошибка ───
latte = Product("Латте", 250)
anna_new = anna.total()
boris_new = boris.total()

# %% swap [exercise]
raf = Product("Раф", 260)
removed = boris.remove("Чай")
missing = boris.remove("Какао")
boris.add(raf)
boris_top = boris.most_expensive()
# ─── заготовка ───
raf = Product("Раф", 260)
removed = ...
missing = ...
boris_top = ...
# ─── проверка ───
def test_results():
    "removed — True, missing — False"
    names = [p.name for p in boris.items]
    if removed is False and names.count("Раф") > 1:
        assert False, "похоже, ячейка выполнена второй раз: чай уже убран прошлым запуском, а раф добавлен дважды. Нажмите «Выполнить все выше» и выполните ячейку один раз"
    assert removed is True, f"removed = {removed!r}: чай в корзине был, remove должен вернуть True"
    assert missing is False, f"missing = {missing!r}: какао в корзине нет, remove должен вернуть False"


def test_contents():
    "в корзине Бориса латте и раф"
    names = [p.name for p in boris.items]
    assert "Чай" not in names, "чай всё ещё в корзине Бориса — уберите его: boris.remove(\"Чай\")"
    assert names == ["Латте", "Раф"], f"в корзине Бориса {names}, а нужно латте и раф"


def test_top():
    "boris_top — раф"
    assert not isinstance(boris_top, (int, float, str)), f"boris_top = {boris_top!r}, а нужен сам товар"
    assert boris_top is raf, "самый дорогой в корзине Бориса — раф: boris.most_expensive() после добавления"
# ─── другое решение ───
raf = Product("Раф", 260)
removed = boris.remove("Чай")
missing = boris.remove("Какао")
boris.items.append(raf)
boris_top = max(boris.items, key=lambda p: p.price)
# ─── ошибка ───
raf = Product("Раф", 260)
removed = boris.remove("Чай")
missing = boris.remove("Какао")
boris_top = boris.most_expensive()
boris.add(raf)

# %% summary
for name, cart in [("Анна", anna), ("Борис", boris)]:
    names = ", ".join(p.name for p in cart.items)
    print(f"{name}: {names} — {cart.total()} ₽")
print("латте в обеих корзинах — один объект:", anna.items[0] is boris.items[0])
