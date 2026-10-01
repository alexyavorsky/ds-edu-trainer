# Урок oop-p4-price-list. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% product [exercise]
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
# ─── заготовка ───
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        ...

    def __eq__(self, other):
        ...

    def __hash__(self):
        ...
# ─── проверка ───
def test_repr():
    "repr — Product('Латте', 220)"
    assert "__repr__" in Product.__dict__, "в классе нет __repr__"
    got = Product.__dict__["__repr__"](Product("Латте", 220))
    assert got == "Product('Латте', 220)", f"repr товара = {got!r}, а нужно \"Product('Латте', 220)\" — название с !r"


def test_eq():
    "равны по названию и цене"
    assert "__eq__" in Product.__dict__, "в классе нет __eq__"
    assert Product("Латте", 220) == Product("Латте", 220), "товары с одинаковыми названием и ценой должны быть равны"
    assert Product("Латте", 220) != Product("Латте", 240), "у товаров разные цены — они не равны"
    assert Product("Латте", 220) != Product("Раф", 220), "у товаров разные названия — они не равны"
    try:
        got = Product.__dict__["__eq__"](Product("Латте", 220), "Латте")
    except AttributeError:
        assert False, "сравнение со строкой падает — сначала проверьте тип: isinstance(other, Product)"
    assert got is NotImplemented, f"для чужого типа __eq__ вернул {got!r}, а нужно NotImplemented"


def test_hash():
    "равные товары — один элемент set"
    try:
        group = {Product("Латте", 220), Product("Латте", 220), Product("Латте", 240)}
    except TypeError:
        assert False, "товар нельзя положить в set — объявите __hash__"
    assert len(group) == 2, f"в set из двух одинаковых латте и одного другого {len(group)} элементов, а нужно 2 — хеш из названия и цены"
# ─── другое решение ───
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return "Product(" + repr(self.name) + ", " + repr(self.price) + ")"

    def __eq__(self, other):
        if isinstance(other, Product):
            return (self.name, self.price) == (other.name, other.price)
        return NotImplemented

    def __hash__(self):
        return hash(self.name)
# ─── ошибка ───
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
# ─── ошибка ───
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"

    def __eq__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

# %% order [exercise]
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

    def __lt__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return (self.price, self.name) < (other.price, other.name)
# ─── заготовка ───
class Product:
    # скопируйте сюда __init__, __repr__, __eq__ и __hash__ из шага 1

    def __lt__(self, other):
        ...
# ─── проверка ───
def test_copied():
    "методы шага 1 на месте"
    for name in ["__init__", "__repr__", "__eq__", "__hash__"]:
        assert name in Product.__dict__ and Product.__dict__[name] is not None, f"в классе нет {name} — скопируйте класс из шага 1 целиком"


def test_lt():
    "дешевле — меньше; при равной цене — по названию"
    assert "__lt__" in Product.__dict__, "в классе нет __lt__"
    try:
        tea, raf = Product("Чай", 120), Product("Раф", 260)
    except TypeError:
        assert False, "Product(\"Чай\", 120) не создаётся — скопируйте __init__ из шага 1"
    assert tea < raf and not raf < tea, "чай за 120 ₽ должен быть меньше рафа за 260 ₽"
    assert Product("Капучино", 220) < Product("Латте", 220), "при равной цене меньше тот, чьё название раньше по алфавиту"
    assert not Product("Латте", 220) < Product("Латте", 220), "товар не меньше равного ему — сравнение строгое"
    got = Product.__dict__["__lt__"](tea, 100)
    assert got is NotImplemented, f"для чужого типа __lt__ вернул {got!r}, а нужно NotImplemented"
# ─── другое решение ───
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

    def __lt__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        if self.price != other.price:
            return self.price < other.price
        return self.name < other.name
# ─── ошибка ───
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

    def __lt__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price

# %% merge [exercise]
morning = [("Латте", 220), ("Чай", 120), ("Раф", 260), ("Какао", 190), ("Эспрессо", 150)]
evening = [("Чай", 120), ("Латте", 240), ("Эспрессо", 150), ("Капучино", 220), ("Раф", 260)]
all_items = [Product(name, price) for name, price in morning + evening]
unique = set(all_items)
n_dupes = len(all_items) - len(unique)
# ─── заготовка ───
morning = [("Латте", 220), ("Чай", 120), ("Раф", 260), ("Какао", 190), ("Эспрессо", 150)]
evening = [("Чай", 120), ("Латте", 240), ("Эспрессо", 150), ("Капучино", 220), ("Раф", 260)]
all_items = ...
unique = ...
n_dupes = ...
# ─── проверка ───
def test_all():
    "all_items — десять товаров по порядку"
    assert isinstance(all_items, list), f"all_items — это {type(all_items).__name__}, а нужен список"
    assert len(all_items) == 10, f"в all_items {len(all_items)} товаров, а в двух прайсах 10 позиций"
    assert all(isinstance(p, Product) for p in all_items), "в all_items должны быть товары Product — создайте их заново после ячейки с классом"
    assert all_items[0] == Product("Латте", 220) and all_items[5] == Product("Чай", 120), "сначала утренний прайс, потом вечерний"


def test_unique():
    "unique — set без повторов, n_dupes — сколько повторов"
    assert isinstance(unique, set), f"unique — это {type(unique).__name__}, а нужно множество: set(all_items)"
    assert len(unique) == 7, f"в unique {len(unique)} товаров, а разных — 7 (латте за 220 и за 240 — разные товары)"
    assert n_dupes == 3, f"n_dupes = {n_dupes!r}, а повторов 3: чай, эспрессо и раф"
# ─── другое решение ───
morning = [("Латте", 220), ("Чай", 120), ("Раф", 260), ("Какао", 190), ("Эспрессо", 150)]
evening = [("Чай", 120), ("Латте", 240), ("Эспрессо", 150), ("Капучино", 220), ("Раф", 260)]
all_items = []
for name, price in morning:
    all_items.append(Product(name, price))
for name, price in evening:
    all_items.append(Product(name, price))
unique = set()
n_dupes = 0
for p in all_items:
    if p in unique:
        n_dupes += 1
    unique.add(p)
# ─── ошибка ───
morning = [("Латте", 220), ("Чай", 120), ("Раф", 260), ("Какао", 190), ("Эспрессо", 150)]
evening = [("Чай", 120), ("Латте", 240), ("Эспрессо", 150), ("Капучино", 220), ("Раф", 260)]
all_items = [Product(name, price) for name, price in morning + evening]
unique = set(p.name for p in all_items)
n_dupes = len(all_items) - len(unique)

# %% price-list [exercise]
price_list = sorted(unique)
cheapest3 = [p.name for p in price_list[:3]]
# ─── заготовка ───
price_list = ...
cheapest3 = ...
# ─── проверка ───
def test_price_list():
    "price_list — по цене, при равной — по названию"
    assert isinstance(price_list, list), f"price_list — это {type(price_list).__name__}, а нужен список: sorted(unique)"
    assert len(price_list) == 7, f"в price_list {len(price_list)} товаров, а в unique 7"
    got = [(p.name, p.price) for p in price_list]
    assert got == [("Чай", 120), ("Эспрессо", 150), ("Какао", 190), ("Капучино", 220), ("Латте", 220), ("Латте", 240), ("Раф", 260)], f"порядок price_list: {got}"


def test_cheapest():
    "cheapest3 — три самых дешёвых"
    assert cheapest3 == ["Чай", "Эспрессо", "Какао"], f"cheapest3 = {cheapest3}, а самые дешёвые — чай, эспрессо и какао"
# ─── другое решение ───
price_list = list(unique)
price_list.sort()
cheapest3 = []
for p in price_list[:3]:
    cheapest3.append(p.name)
# ─── ошибка ───
price_list = sorted(unique)
cheapest3 = [p.name for p in price_list[-3:]]

# %% look
for p in price_list:
    print(p)

# %% changed [exercise]
alphabet = sorted(p.name for p in unique)
counts = {}
for name in alphabet:
    counts[name] = counts.get(name, 0) + 1
changed = [name for name, n in counts.items() if n > 1]
# ─── заготовка ───
alphabet = ...
changed = ...
# ─── проверка ───
def test_alphabet():
    "alphabet — все названия по алфавиту"
    assert isinstance(alphabet, list), f"alphabet — это {type(alphabet).__name__}, а нужен список названий"
    assert alphabet == ["Какао", "Капучино", "Латте", "Латте", "Раф", "Чай", "Эспрессо"], f"alphabet = {alphabet}"


def test_changed():
    "changed — товары с новой ценой"
    assert isinstance(changed, list), f"changed — это {type(changed).__name__}, а нужен список названий"
    assert changed != ["Латте", "Латте"], "латте попал в changed дважды — каждое название нужно один раз"
    assert changed == ["Латте"], f"changed = {changed}, а цена изменилась только у латте"
# ─── другое решение ───
alphabet = [p.name for p in sorted(unique, key=lambda p: p.name)]
changed = []
for name in alphabet:
    if alphabet.count(name) > 1 and name not in changed:
        changed.append(name)
# ─── ошибка ───
alphabet = sorted(p.name for p in unique)
changed = [name for name in alphabet if alphabet.count(name) > 1]

# %% summary
print(f"позиций в двух прайсах: {len(all_items)}, повторов: {n_dupes}")
print("сводный прайс:", price_list)
for name in changed:
    prices = sorted(p.price for p in unique if p.name == name)
    print(f"изменилась цена: {name}, цены в прайсах {prices}")
