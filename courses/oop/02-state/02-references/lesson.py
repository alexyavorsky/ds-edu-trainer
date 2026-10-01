# Урок oop-references. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% alias
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


latte = Product("Латте", 220)
same = latte  # второе имя, не копия
same.price = 250
print(latte.price)

# %% is
twin = Product("Латте", 250)  # новый объект с теми же значениями
print(same is latte)
print(twin is latte)
print(twin == latte)  # пока == сравнивает тождественность
print(twin.price == latte.price)

# %% in-list
espresso = Product("Эспрессо", 150)
menu = [espresso, Product("Чай", 120)]
menu[0].price = 160
print(espresso.price)
print(menu[0] is espresso)

# %% raise-prices [exercise]
def raise_prices(products, amount):
    for p in products:
        p.price = p.price + amount
# ─── заготовка ───
def raise_prices(products, amount):
    ...
# ─── проверка ───
def test_changes():
    "цены товаров выросли на amount"
    tea, raf = Product("Чай", 120), Product("Раф", 260)
    products = [tea, raf]
    raise_prices(products, 15)
    assert tea.price != 120, "цена чая не изменилась — меняйте атрибут price у каждого товара: p.price = p.price + amount"
    assert (tea.price, raf.price) == (135, 275), f"после raise_prices(…, 15) цены {tea.price} и {raf.price}, а нужно 135 и 275"


def test_same_objects():
    "в списке остались те же объекты"
    tea = Product("Чай", 120)
    products = [tea]
    raise_prices(products, 10)
    assert len(products) == 1 and products[0] is tea, "функция заменила товары в списке другими объектами — меняйте цену у самих товаров"


def test_returns_nothing():
    "функция ничего не возвращает"
    got = raise_prices([Product("Чай", 120)], 10)
    assert got is None, f"функция вернула {got!r}, а должна только изменить товары"
# ─── другое решение ───
def raise_prices(products, amount):
    for i in range(len(products)):
        products[i].price += amount
# ─── ошибка ───
def raise_prices(products, amount):
    for p in products:
        price = p.price
        price = price + amount
# ─── ошибка ───
def raise_prices(products, amount):
    for i in range(len(products)):
        products[i] = Product(products[i].name, products[i].price + amount)

# %% find [exercise]
def find(products, name):
    for p in products:
        if p.name == name:
            return p
    return None
# ─── заготовка ───
def find(products, name):
    ...
# ─── проверка ───
def test_found():
    "возвращает сам товар из списка"
    tea, raf = Product("Чай", 120), Product("Раф", 260)
    got = find([tea, raf], "Раф")
    assert got is not None, "find(…, \"Раф\") вернула None, а раф в списке есть"
    assert not isinstance(got, (int, str)), f"find вернула {got!r}, а нужен сам товар — экземпляр Product"
    assert got is raf, "find вернула не тот объект, что лежит в списке: верните p, а не новый Product"


def test_missing():
    "нет товара — None"
    got = find([Product("Чай", 120)], "Какао")
    assert got is None, f"для товара, которого нет, find вернула {got!r}, а нужно None"
# ─── другое решение ───
def find(products, name):
    found = None
    for p in products:
        if p.name == name and found is None:
            found = p
    return found
# ─── ошибка ───
def find(products, name):
    for p in products:
        if p.name == name:
            return Product(p.name, p.price)
    return None
# ─── ошибка ───
def find(products, name):
    for p in products:
        if p.name == name:
            return p.price
    return None

# %% copy-quiz [quiz]
tea = menu[1]
tea.price = 100
print(menu[1].price)

# %% copy [exercise]
latte = Product("Латте", 220)
pumpkin = Product(latte.name, latte.price)
pumpkin.name = "Тыквенный латте"
pumpkin.price = 290
# ─── заготовка ───
latte = Product("Латте", 220)
pumpkin = ...
# ─── проверка ───
def test_separate():
    "pumpkin — отдельный объект Product"
    assert isinstance(pumpkin, Product), f"pumpkin — это {type(pumpkin).__name__}, а нужен экземпляр Product"
    assert pumpkin is not latte, "pumpkin и latte — один и тот же объект; создайте новый вызовом Product(…)"


def test_values():
    "у pumpkin новое название и цена, latte не изменился"
    assert isinstance(pumpkin, Product), "сначала создайте pumpkin"
    assert (latte.name, latte.price) == ("Латте", 220), f"исходный латте изменился: {latte.name}, {latte.price} — меняйте только pumpkin"
    assert (pumpkin.name, pumpkin.price) == ("Тыквенный латте", 290), f"у pumpkin {pumpkin.name!r}, {pumpkin.price!r}"
# ─── другое решение ───
latte = Product("Латте", 220)
pumpkin = Product("Тыквенный латте", 290)
# ─── ошибка ───
latte = Product("Латте", 220)
pumpkin = latte
pumpkin.name = "Тыквенный латте"
pumpkin.price = 290

# %% default-bug
class Ticket:
    def __init__(self, customer, items=[]):  # ошибка: один список на все вызовы
        self.customer = customer
        self.items = items


anna = Ticket("Анна")
boris = Ticket("Борис")
anna.items.append("Латте")
print(boris.items)
print(anna.items is boris.items)

# %% fix-default [exercise]
class Delivery:
    def __init__(self, address, notes=None):
        self.address = address
        if notes is None:
            self.notes = []
        else:
            self.notes = list(notes)
# ─── заготовка ───
class Delivery:
    def __init__(self, address, notes=[]):
        self.address = address
        self.notes = notes
# ─── проверка ───
def test_own_lists():
    "у доставок без notes — свои пустые списки"
    a, b = Delivery("Лесная, 5"), Delivery("Садовая, 12")
    assert a.notes == [] and b.notes == [], f"у новых доставок notes = {a.notes} и {b.notes}, а нужно []"
    a.notes.append("домофон не работает")
    assert b.notes == [], "заметка одной доставки появилась у другой — у доставок общий список; значение по умолчанию — None, список создаётся в __init__"


def test_given():
    "переданный список копируется"
    notes = ["позвонить заранее"]
    d = Delivery("Лесная, 5", notes)
    assert d.notes == ["позвонить заранее"], f"у доставки с заметками notes = {d.notes}"
    d.notes.append("оставить у двери")
    assert notes == ["позвонить заранее"], "доставка изменила чужой список — храните его копию: list(notes)"
# ─── другое решение ───
class Delivery:
    def __init__(self, address, notes=None):
        self.address = address
        self.notes = list(notes) if notes is not None else []
# ─── ошибка ───
class Delivery:
    def __init__(self, address, notes=None):
        self.address = address
        if notes is None:
            self.notes = []
        else:
            self.notes = notes
