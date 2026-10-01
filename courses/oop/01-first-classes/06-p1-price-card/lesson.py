# Урок oop-p1-price-card. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% product [exercise]
class Product:
    def __init__(self, name, price, volume):
        self.name = name
        self.price = price
        self.volume = volume

    def per_100ml(self):
        return round(self.price / self.volume * 100, 1)

    def discounted(self, percent):
        return round(self.price * (100 - percent) / 100)
# ─── заготовка ───
class Product:
    def __init__(self, name, price, volume):
        ...

    def per_100ml(self):
        ...

    def discounted(self, percent):
        ...
# ─── проверка ───
def _cappuccino():
    try:
        return Product("Капучино", 220, 300)
    except TypeError as e:
        assert False, f"Product(\"Капучино\", 220, 300) не создаётся: {e}"


def test_attributes():
    "name, price и volume из аргументов"
    p = _cappuccino()
    for attr, value in [("name", "Капучино"), ("price", 220), ("volume", 300)]:
        assert hasattr(p, attr), f"у товара нет атрибута {attr} — запишите его в __init__: self.{attr} = {attr}"
        assert getattr(p, attr) == value, f"у Product(\"Капучино\", 220, 300) {attr} = {getattr(p, attr)!r}, а нужно {value!r}"


def test_per_100ml():
    "per_100ml() — цена за 100 мл с одним знаком"
    p = _cappuccino()
    assert hasattr(p, "price") and hasattr(p, "volume"), "сначала задайте атрибуты в __init__"
    got = p.per_100ml()
    assert got is not None, "per_100ml() ничего не возвращает — нужен return"
    assert got != round(300 / 220 * 100, 1), "дробь перевёрнута: цена за 100 мл — цена, делённая на объём, умноженная на 100"
    assert got == 73.3, f"per_100ml() у капучино = {got!r}, а нужно 73.3 — округлите до одного знака: round(…, 1)"
    assert Product("Латте", 240, 400).per_100ml() == 60.0, "у Product(\"Латте\", 240, 400) цена за 100 мл — 60.0"


def test_discounted():
    "discounted(20) = 176 и price не меняется"
    p = _cappuccino()
    assert hasattr(p, "price"), "сначала задайте атрибуты в __init__"
    got = p.discounted(20)
    assert got is not None, "discounted() ничего не возвращает — нужен return"
    assert p.price == 220, f"после discounted(20) price = {p.price!r}: метод должен вернуть новую цену, а не менять атрибут"
    assert got != 44, "44 — это размер скидки, а нужна цена после скидки"
    assert got == 176, f"discounted(20) у капучино = {got!r}, а нужно 176"
    assert Product("Чай", 133, 400).discounted(10) == 120, "Product(\"Чай\", 133, 400).discounted(10) — 120 (119.7 после скидки): округлите до целых рублей"
# ─── другое решение ───
class Product:
    def __init__(self, name, price, volume):
        self.name, self.price, self.volume = name, price, volume

    def per_100ml(self):
        return round(100 * self.price / self.volume, 1)

    def discounted(self, percent):
        return round(self.price - self.price * percent / 100)
# ─── ошибка ───
class Product:
    def __init__(self, name, price, volume):
        self.name = name
        self.price = price
        self.volume = volume

    def per_100ml(self):
        return round(self.price / self.volume * 100, 1)

    def discounted(self, percent):
        self.price = round(self.price * (100 - percent) / 100)
        return self.price
# ─── ошибка ───
class Product:
    def __init__(self, name, price, volume):
        self.name = name
        self.price = price
        self.volume = volume

    def per_100ml(self):
        return round(self.volume / self.price * 100, 1)

    def discounted(self, percent):
        return round(self.price * (100 - percent) / 100)

# %% card [exercise]
class Product:
    def __init__(self, name, price, volume):
        self.name = name
        self.price = price
        self.volume = volume

    def per_100ml(self):
        return round(self.price / self.volume * 100, 1)

    def discounted(self, percent):
        return round(self.price * (100 - percent) / 100)

    def card(self, percent=0):
        if percent == 0:
            return f"{self.name}, {self.volume} мл — {self.price} ₽"
        return f"{self.name}, {self.volume} мл — {self.discounted(percent)} ₽ (скидка {percent} %)"
# ─── заготовка ───
class Product:
    # скопируйте сюда __init__, per_100ml и discounted из шага 1

    def card(self, percent=0):
        ...
# ─── проверка ───
def _cappuccino():
    try:
        return Product("Капучино", 220, 300)
    except TypeError:
        assert False, "Product(\"Капучино\", 220, 300) не создаётся — скопируйте в класс __init__ из шага 1"


def test_copied():
    "методы шага 1 скопированы и работают"
    p = _cappuccino()
    for method in ["per_100ml", "discounted"]:
        assert hasattr(p, method), f"в классе нет метода {method} — скопируйте класс из шага 1 целиком"
    assert p.per_100ml() == 73.3, f"per_100ml() у капучино вернул {p.per_100ml()!r}, а нужно 73.3 — в скопированном классе ошибка из шага 1"
    assert p.discounted(20) == 176, f"discounted(20) у капучино вернул {p.discounted(20)!r}, а нужно 176 — в скопированном классе ошибка из шага 1"


def test_plain():
    "card() без скидки"
    p = _cappuccino()
    got = p.card()
    assert got is not None, "card() ничего не возвращает — нужен return"
    assert got == "Капучино, 300 мл — 220 ₽", f"card() вернул {got!r}, а нужно \"Капучино, 300 мл — 220 ₽\""


def test_sale():
    "card(20) — цена со скидкой и пометка"
    p = _cappuccino()
    assert hasattr(p, "discounted"), "сначала верните в класс метод discounted"
    got = p.card(20)
    assert got != "Капучино, 300 мл — 220 ₽ (скидка 20 %)", "на ценнике старая цена — возьмите цену со скидкой: self.discounted(percent)"
    assert got == "Капучино, 300 мл — 176 ₽ (скидка 20 %)", f"card(20) вернул {got!r}, а нужно \"Капучино, 300 мл — 176 ₽ (скидка 20 %)\""
    assert p.price == 220, "card() не должен менять price"
# ─── другое решение ───
class Product:
    def __init__(self, name, price, volume):
        self.name = name
        self.price = price
        self.volume = volume

    def per_100ml(self):
        return round(self.price / self.volume * 100, 1)

    def discounted(self, percent):
        return round(self.price * (100 - percent) / 100)

    def card(self, percent=0):
        text = f"{self.name}, {self.volume} мл — {self.discounted(percent)} ₽"
        if percent:
            text += f" (скидка {percent} %)"
        return text
# ─── ошибка ───
class Product:
    def __init__(self, name, price, volume):
        self.name = name
        self.price = price
        self.volume = volume

    def per_100ml(self):
        return round(self.price / self.volume * 100, 1)

    def discounted(self, percent):
        return round(self.price * (100 - percent) / 100)

    def card(self, percent=0):
        if percent == 0:
            return f"{self.name}, {self.volume} мл — {self.price} ₽"
        return f"{self.name}, {self.volume} мл — {self.price} ₽ (скидка {percent} %)"
# ─── ошибка ───
class Product:
    def __init__(self, name, price, volume):
        self.name = name
        self.price = price
        self.volume = volume

    def card(self, percent=0):
        price = round(self.price * (100 - percent) / 100)
        if percent == 0:
            return f"{self.name}, {self.volume} мл — {price} ₽"
        return f"{self.name}, {self.volume} мл — {price} ₽ (скидка {percent} %)"

# %% catalog [exercise]
data = [
    ("Эспрессо", 150, 60),
    ("Капучино", 220, 300),
    ("Латте", 240, 400),
    ("Раф", 260, 300),
    ("Американо", 170, 250),
    ("Какао", 190, 300),
]
catalog = [Product(name, price, volume) for name, price, volume in data]
# ─── заготовка ───
data = [
    ("Эспрессо", 150, 60),
    ("Капучино", 220, 300),
    ("Латте", 240, 400),
    ("Раф", 260, 300),
    ("Американо", 170, 250),
    ("Какао", 190, 300),
]
catalog = ...
# ─── проверка ───
def test_catalog():
    "catalog — шесть экземпляров Product по порядку"
    assert isinstance(catalog, list), f"catalog — это {type(catalog).__name__}, а нужен список"
    assert len(catalog) == 6, f"в catalog {len(catalog)} элементов, а в data шесть троек"
    assert all(isinstance(p, Product) for p in catalog), "в catalog должны быть экземпляры текущего класса Product — создайте их заново после ячейки с классом"
    assert [p.name for p in catalog] == [d[0] for d in data], f"названия в catalog: {[p.name for p in catalog]}"
    assert [(p.price, p.volume) for p in catalog] == [d[1:] for d in data], "цены и объёмы берутся из data: Product(name, price, volume)"
# ─── другое решение ───
data = [
    ("Эспрессо", 150, 60),
    ("Капучино", 220, 300),
    ("Латте", 240, 400),
    ("Раф", 260, 300),
    ("Американо", 170, 250),
    ("Какао", 190, 300),
]
catalog = []
for row in data:
    catalog.append(Product(row[0], row[1], row[2]))
# ─── ошибка ───
data = [
    ("Эспрессо", 150, 60),
    ("Капучино", 220, 300),
    ("Латте", 240, 400),
    ("Раф", 260, 300),
    ("Американо", 170, 250),
    ("Какао", 190, 300),
]
catalog = [Product(name, volume, price) for name, price, volume in data]

# %% look
for p in catalog:
    print(p.card())

# %% cards [exercise]
cards = [p.card(20) for p in catalog]
sale_total = sum(p.discounted(20) for p in catalog)
# ─── заготовка ───
cards = ...
sale_total = ...
# ─── проверка ───
def test_cards():
    "cards — шесть ценников со скидкой 20 %"
    assert isinstance(cards, list), f"cards — это {type(cards).__name__}, а нужен список"
    assert len(cards) == 6, f"в cards {len(cards)} элементов, а товаров в каталоге 6"
    assert all(isinstance(c, str) for c in cards), "в cards должны быть строки — результаты вызова p.card(20) со скобками"
    assert cards[1] != "Капучино, 300 мл — 220 ₽", "ценники без скидки — передайте в card процент: p.card(20)"
    assert cards[1] == "Капучино, 300 мл — 176 ₽ (скидка 20 %)", f"второй ценник: {cards[1]!r}"


def test_total():
    "sale_total — сумма цен распродажи"
    assert sale_total != 1230, "1230 — сумма цен без скидки; сложите p.discounted(20)"
    assert sale_total == 984, f"sale_total = {sale_total!r}, а по ценам распродажи — 984 ₽"
# ─── другое решение ───
cards = []
sale_total = 0
for p in catalog:
    cards.append(p.card(20))
    sale_total += p.discounted(20)
# ─── ошибка ───
cards = [p.card() for p in catalog]
sale_total = sum(p.discounted(20) for p in catalog)
# ─── ошибка ───
cards = [p.card(20) for p in catalog]
sale_total = sum(p.price for p in catalog)

# %% best [exercise]
best = catalog[0]
for p in catalog:
    if p.per_100ml() < best.per_100ml():
        best = p
# ─── заготовка ───
best = ...
# ─── проверка ───
def test_best():
    "best — товар с самой низкой ценой за 100 мл"
    assert not isinstance(best, (int, float)), f"best = {best!r} — это число, а нужен сам товар, экземпляр Product"
    assert not isinstance(best, str), f"best = {best!r} — это строка, а нужен сам товар, экземпляр Product"
    assert isinstance(best, Product), f"best — это {type(best).__name__}, а нужен экземпляр Product из catalog"
    assert best.name != "Эспрессо", "эспрессо — самый дешёвый за чашку, но самый дорогой за 100 мл: сравнивайте per_100ml()"
    assert best.name == "Латте", f"best — {best.name}, а дешевле всех за 100 мл латте"
# ─── другое решение ───
best = min(catalog, key=lambda p: p.per_100ml())
# ─── ошибка ───
best = catalog[0]
for p in catalog:
    if p.price < best.price:
        best = p
# ─── ошибка ───
best = min(p.per_100ml() for p in catalog)

# %% summary
print("Осенняя распродажа — скидка 20 %")
for text in cards:
    print(" ", text)
print(f"Всё меню по одной чашке: {sale_total} ₽")
print(f"Выгоднее всего: {best.name} — {best.per_100ml()} ₽ за 100 мл")
