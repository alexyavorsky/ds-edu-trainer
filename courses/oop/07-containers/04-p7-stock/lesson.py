# Урок oop-p7-stock. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% stock [exercise]
class Stock:
    def __init__(self, items):
        self._items = dict(items)

    def __len__(self):
        return len([name for name in self._items if self._items[name] > 0])

    def __getitem__(self, name):
        return self._items.get(name, 0)

    def __contains__(self, name):
        return self[name] > 0

    def __iter__(self):
        for name in sorted(self._items):
            if self._items[name] > 0:
                yield name
# ─── заготовка ───
class Stock:
    def __init__(self, items):
        ...

    def __len__(self):
        ...

    def __getitem__(self, name):
        ...

    def __contains__(self, name):
        ...

    def __iter__(self):
        ...
# ─── проверка ───
def _stock():
    return Stock({"Молоко": 12, "Зёрна": 8, "Сливки": 0})


def test_copy():
    "_items — копия словаря"
    data = {"Молоко": 12}
    stock = Stock(data)
    assert getattr(stock, "_items", None) == data, "количества хранятся во внутреннем словаре _items"
    data["Молоко"] = 0
    assert stock["Молоко"] == 12, "склад изменился вместе с чужим словарём — храните копию: dict(items)"


def test_len_getitem():
    "len и квадратные скобки"
    stock = _stock()
    assert len(stock) == 2, f"len = {len(stock)}, а позиций с количеством больше нуля две — сливок 0, их не считаем"
    assert stock["Молоко"] == 12, f"stock[\"Молоко\"] = {stock['Молоко']!r}"
    try:
        got = stock["Сироп"]
    except KeyError:
        assert False, "stock[\"Сироп\"] выбросил KeyError, а для отсутствующей позиции нужно 0"
    assert got == 0, f"stock[\"Сироп\"] = {got!r}, а нужно 0"


def test_in():
    "in — есть и больше нуля"
    stock = _stock()
    assert ("Молоко" in stock) is True, "\"Молоко\" in stock должно быть True"
    assert ("Сливки" in stock) is False, "сливок 0 — \"Сливки\" in stock должно быть False"
    assert ("Сироп" in stock) is False, "сиропа нет — \"Сироп\" in stock должно быть False"


def test_iter():
    "цикл — названия по алфавиту, без нулевых"
    names = list(_stock())
    assert names == ["Зёрна", "Молоко"], f"цикл по складу дал {names}, а нужно ['Зёрна', 'Молоко'] — по алфавиту и без позиций с нулём"
# ─── другое решение ───
class Stock:
    def __init__(self, items):
        self._items = {}
        for name, amount in items.items():
            self._items[name] = amount

    def __len__(self):
        return sum(1 for name in self)

    def __getitem__(self, name):
        if name in self._items:
            return self._items[name]
        return 0

    def __contains__(self, name):
        return self._items.get(name, 0) > 0

    def __iter__(self):
        names = [name for name, amount in self._items.items() if amount > 0]
        return iter(sorted(names))
# ─── ошибка ───
class Stock:
    def __init__(self, items):
        self._items = dict(items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, name):
        return self._items.get(name, 0)

    def __contains__(self, name):
        return name in self._items

    def __iter__(self):
        for name in sorted(self._items):
            yield name
# ─── ошибка ───
class Stock:
    def __init__(self, items):
        self._items = items

    def __len__(self):
        return len([name for name in self._items if self._items[name] > 0])

    def __getitem__(self, name):
        return self._items.get(name, 0)

    def __contains__(self, name):
        return self[name] > 0

    def __iter__(self):
        for name in sorted(self._items):
            if self._items[name] > 0:
                yield name

# %% supply [exercise]
class Stock:
    def __init__(self, items):
        self._items = dict(items)

    def __len__(self):
        return len([name for name in self._items if self._items[name] > 0])

    def __getitem__(self, name):
        return self._items.get(name, 0)

    def __contains__(self, name):
        return self[name] > 0

    def __iter__(self):
        for name in sorted(self._items):
            if self._items[name] > 0:
                yield name

    def __add__(self, other):
        if not isinstance(other, Stock):
            return NotImplemented
        result = dict(self._items)
        for name, amount in other._items.items():
            result[name] = result.get(name, 0) + amount
        return Stock(result)

    def take(self, name, amount):
        if self[name] < amount:
            raise ValueError(f"на складе мало: {name}")
        self._items[name] -= amount
# ─── заготовка ───
class Stock:
    # скопируйте сюда методы из шага 1

    def __add__(self, other):
        ...

    def take(self, name, amount):
        ...
# ─── проверка ───
def _pair():
    try:
        a, b = Stock({"Молоко": 2, "Зёрна": 3}), Stock({"Молоко": 10, "Сироп": 2})
    except TypeError:
        assert False, "Stock({...}) не создаётся — скопируйте __init__ из шага 1"
    for name in ["__len__", "__getitem__", "__contains__", "__iter__"]:
        assert name in Stock.__dict__, f"в классе нет {name} — скопируйте класс из шага 1 целиком"
    assert a["Молоко"] == 2 and a["Сироп"] == 0 and list(a) == ["Зёрна", "Молоко"], "методы шага 1 работают не так, как там — в скопированном классе ошибка из шага 1"
    return a, b


def test_add():
    "сложение складов"
    a, b = _pair()
    got = a + b
    assert isinstance(got, Stock), f"a + b дал {type(got).__name__}, а нужен новый Stock"
    assert (got["Молоко"], got["Зёрна"], got["Сироп"]) == (12, 3, 2), f"после сложения молоко, зёрна, сироп = {got['Молоко']}, {got['Зёрна']}, {got['Сироп']}"
    assert a["Молоко"] == 2 and b["Молоко"] == 10, "сложение изменило слагаемые — создавайте новый склад"
    assert Stock.__dict__["__add__"](a, 5) is NotImplemented, "сложение с чужим типом должно вернуть NotImplemented"


def test_take():
    "take списывает или выбрасывает ValueError"
    a, _ = _pair()
    a.take("Зёрна", 2)
    assert a["Зёрна"] == 1, f"после take(\"Зёрна\", 2) осталось {a['Зёрна']}, а нужно 1"
    for name, amount in [("Зёрна", 5), ("Сироп", 1)]:
        try:
            a.take(name, amount)
        except ValueError as e:
            assert str(e) == f"на складе мало: {name}", f"сообщение {str(e)!r}"
        else:
            assert False, f"take({name!r}, {amount}) не выбросил ValueError — на складе меньше"
    assert a["Зёрна"] == 1 and a["Сироп"] == 0, "после неудачного списания склад не должен меняться"
# ─── другое решение ───
class Stock:
    def __init__(self, items):
        self._items = dict(items)

    def __len__(self):
        return len([name for name in self._items if self._items[name] > 0])

    def __getitem__(self, name):
        return self._items.get(name, 0)

    def __contains__(self, name):
        return self[name] > 0

    def __iter__(self):
        for name in sorted(self._items):
            if self._items[name] > 0:
                yield name

    def __add__(self, other):
        if isinstance(other, Stock):
            names = set(self._items) | set(other._items)
            return Stock({name: self[name] + other[name] for name in names})
        return NotImplemented

    def take(self, name, amount):
        left = self[name] - amount
        if left < 0:
            raise ValueError(f"на складе мало: {name}")
        self._items[name] = left
# ─── ошибка ───
class Stock:
    def __init__(self, items):
        self._items = dict(items)

    def __len__(self):
        return len([name for name in self._items if self._items[name] > 0])

    def __getitem__(self, name):
        return self._items.get(name, 0)

    def __contains__(self, name):
        return self[name] > 0

    def __iter__(self):
        for name in sorted(self._items):
            if self._items[name] > 0:
                yield name

    def __add__(self, other):
        if not isinstance(other, Stock):
            return NotImplemented
        for name, amount in other._items.items():
            self._items[name] = self._items.get(name, 0) + amount
        return self

    def take(self, name, amount):
        if self[name] < amount:
            raise ValueError(f"на складе мало: {name}")
        self._items[name] -= amount
# ─── ошибка ───
class Stock:
    def __init__(self, items):
        self._items = dict(items)

    def __len__(self):
        return len([name for name in self._items if self._items[name] > 0])

    def __getitem__(self, name):
        return self._items.get(name, 0)

    def __contains__(self, name):
        return self[name] > 0

    def __iter__(self):
        for name in sorted(self._items):
            if self._items[name] > 0:
                yield name

    def __add__(self, other):
        if not isinstance(other, Stock):
            return NotImplemented
        result = dict(self._items)
        result.update(other._items)
        return Stock(result)

    def take(self, name, amount):
        if self[name] < amount:
            raise ValueError(f"на складе мало: {name}")
        self._items[name] -= amount

# %% morning [exercise]
leftover = Stock({"Зёрна": 3, "Молоко": 2, "Сироп": 1, "Стаканы": 40, "Сливки": 0})
delivery = Stock({"Зёрна": 5, "Молоко": 10, "Сироп": 2, "Стаканы": 100})
stock = leftover + delivery
n_positions = len(stock)
milk = stock["Молоко"]
# ─── заготовка ───
leftover = Stock({"Зёрна": 3, "Молоко": 2, "Сироп": 1, "Стаканы": 40, "Сливки": 0})
delivery = Stock({"Зёрна": 5, "Молоко": 10, "Сироп": 2, "Стаканы": 100})
stock = ...
n_positions = ...
milk = ...
# ─── проверка ───
def test_stock():
    "stock — склад после поставки"
    assert isinstance(stock, Stock), f"stock — это {type(stock).__name__}, а нужен Stock: leftover + delivery"
    assert stock["Стаканы"] == 140, f"стаканов на складе {stock['Стаканы']}, а должно быть 140 — 40 с вечера и 100 из поставки"


def test_numbers():
    "n_positions и milk"
    assert n_positions != 5, "5 — вместе со сливками, а их 0: len(stock) считает только позиции больше нуля"
    assert n_positions == 4, f"n_positions = {n_positions!r}, а позиций на складе 4"
    assert milk == 12, f"milk = {milk!r}, а молока 12"
# ─── другое решение ───
leftover = Stock({"Зёрна": 3, "Молоко": 2, "Сироп": 1, "Стаканы": 40, "Сливки": 0})
delivery = Stock({"Зёрна": 5, "Молоко": 10, "Сироп": 2, "Стаканы": 100})
stock = delivery + leftover
n_positions = len(list(stock))
milk = stock["Молоко"]
# ─── ошибка ───
leftover = Stock({"Зёрна": 3, "Молоко": 2, "Сироп": 1, "Стаканы": 40, "Сливки": 0})
delivery = Stock({"Зёрна": 5, "Молоко": 10, "Сироп": 2, "Стаканы": 100})
stock = delivery
n_positions = len(stock)
milk = stock["Молоко"]

# %% day [exercise]
usage = [
    ("Молоко", 5), ("Стаканы", 60), ("Сироп", 2), ("Зёрна", 3),
    ("Стаканы", 78), ("Сироп", 2), ("Молоко", 4), ("Сироп", 1),
]
short = []
for name, amount in usage:
    try:
        stock.take(name, amount)
    except ValueError:
        short.append(name)
# ─── заготовка ───
usage = [
    ("Молоко", 5), ("Стаканы", 60), ("Сироп", 2), ("Зёрна", 3),
    ("Стаканы", 78), ("Сироп", 2), ("Молоко", 4), ("Сироп", 1),
]
short = ...
# ─── проверка ───
def test_short():
    "short — неудавшиеся списания"
    assert isinstance(short, list), f"short — это {type(short).__name__}, а нужен список названий"
    assert short == ["Сироп"], f"short = {short}, а не хватило только сиропа — один раз. Если ячейка выполнялась несколько раз, склад уже потрачен прошлыми запусками — нажмите «Выполнить все выше» и выполните её один раз"


def test_left():
    "остатки после дня"
    left = {name: stock[name] for name in ["Зёрна", "Молоко", "Сироп", "Стаканы"]}
    assert left == {"Зёрна": 5, "Молоко": 3, "Сироп": 0, "Стаканы": 2}, f"остатки после дня: {left} — спишите все списания из usage по порядку"
# ─── другое решение ───
usage = [
    ("Молоко", 5), ("Стаканы", 60), ("Сироп", 2), ("Зёрна", 3),
    ("Стаканы", 78), ("Сироп", 2), ("Молоко", 4), ("Сироп", 1),
]
short = []
for pair in usage:
    if stock[pair[0]] >= pair[1]:
        stock.take(pair[0], pair[1])
    else:
        short.append(pair[0])
# ─── ошибка ───
usage = [
    ("Молоко", 5), ("Стаканы", 60), ("Сироп", 2), ("Зёрна", 3),
    ("Стаканы", 78), ("Сироп", 2), ("Молоко", 4), ("Сироп", 1),
]
short = []
for name, amount in usage:
    try:
        stock.take(name, amount)
    except ValueError:
        short.append(name)
        break

# %% report [exercise]
low = [name for name in stock if stock[name] < 5]
out_of_syrup = "Сироп" not in stock
# ─── заготовка ───
low = ...
out_of_syrup = ...
# ─── проверка ───
def test_low():
    "low — чего мало"
    assert isinstance(low, list), f"low — это {type(low).__name__}, а нужен список названий"
    assert "Сироп" not in low, "сиропа 0 — цикл по складу его не выдаёт, а в low нужны позиции, которые ещё есть, но мало"
    assert low == ["Молоко", "Стаканы"], f"low = {low}, а меньше 5 осталось молока и стаканов"


def test_syrup():
    "out_of_syrup"
    assert out_of_syrup is True, f"out_of_syrup = {out_of_syrup!r}, а сиропа не осталось"
# ─── другое решение ───
low = []
for name in stock:
    if stock[name] < 5:
        low.append(name)
out_of_syrup = stock["Сироп"] == 0
# ─── ошибка ───
low = [name for name in ["Зёрна", "Молоко", "Сироп", "Стаканы"] if stock[name] < 5]
out_of_syrup = "Сироп" not in stock

# %% summary
print(f"позиций: {len(stock)}")
for name in stock:
    mark = " ← заказать" if name in low else ""
    print(f"{name}: {stock[name]}{mark}")
print("не хватило:", ", ".join(short), "| сироп закончился:", out_of_syrup)
