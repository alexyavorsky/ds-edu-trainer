# Урок oop-objects. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% types
print(type(150))
print(type(2.5))
print(type("латте"))
print(type(["чай", "раф"]))
print(type({"чай": 120}))

# %% methods
name = "латте"
print(name.upper())
print("чай, раф, какао".split(", "))

order = ["чай", "раф"]
order.append("какао")
print(order)

# %% no-method [raises=AttributeError]
name.append("со льдом")

# %% type-name
price = 220
print(type(price).__name__)
print(f"price — это {type(price).__name__}")

# %% kinds [exercise]
values = [150, "латте", 2.5, ["чай"], {"раф": 260}, True]
kinds = [type(v).__name__ for v in values]
# ─── заготовка ───
values = [150, "латте", 2.5, ["чай"], {"раф": 260}, True]
kinds = ...
# ─── проверка ───
def test_kinds():
    "kinds — имена классов значений по порядку"
    assert isinstance(kinds, list), f"kinds — это {type(kinds).__name__}, а нужен список строк"
    assert len(kinds) == 6, f"в kinds {len(kinds)} элементов, а значений в values 6"
    assert all(isinstance(k, str) for k in kinds), "в kinds должны быть имена классов строками: type(v).__name__, а не сам type(v)"
    assert not kinds[0].startswith("<class"), f"в kinds {kinds[0]!r} — это текст всего класса; нужно только имя: type(v).__name__"
    assert kinds == ["int", "str", "float", "list", "dict", "bool"], f"в kinds {kinds}"
# ─── другое решение ───
values = [150, "латте", 2.5, ["чай"], {"раф": 260}, True]
kinds = []
for v in values:
    kinds.append(type(v).__name__)
# ─── ошибка ───
values = [150, "латте", 2.5, ["чай"], {"раф": 260}, True]
kinds = [type(v) for v in values]

# %% isinstance
print(isinstance(150, int))
print(isinstance("150", int))
print(isinstance(2.5, (int, float)))

# %% numbers-only [exercise]
raw = [150, "200", 90.5, None, 120, "нет цены", 300.0]
prices = [v for v in raw if isinstance(v, (int, float))]
# ─── заготовка ───
raw = [150, "200", 90.5, None, 120, "нет цены", 300.0]
prices = ...
# ─── проверка ───
def test_prices():
    "prices — только числа из raw"
    assert isinstance(prices, list), f"prices — это {type(prices).__name__}, а нужен список"
    assert "200" not in prices, "в prices попала строка \"200\": она похожа на число, но это str"
    assert 90.5 in prices, "в prices нет 90.5 — дробные числа (float) тоже нужны"
    assert prices == [150, 90.5, 120, 300.0], f"в prices {prices}, а чисел в raw четыре: 150, 90.5, 120, 300.0"
# ─── другое решение ───
raw = [150, "200", 90.5, None, 120, "нет цены", 300.0]
prices = []
for v in raw:
    if isinstance(v, int) or isinstance(v, float):
        prices.append(v)
# ─── ошибка ───
raw = [150, "200", 90.5, None, 120, "нет цены", 300.0]
prices = [v for v in raw if type(v) == int]

# %% bool-quiz [quiz]
print(isinstance(True, int))

# %% classes
kind = int
print(kind("42") + 1)
print(type(int))
print([c.__name__ for c in [int, str, list]])

# %% describe [exercise]
def describe(value):
    return f"{type(value).__name__}: {value}"
# ─── заготовка ───
def describe(value):
    ...  # "имя класса: значение"
# ─── проверка ───
def test_number():
    "describe(150) = \"int: 150\""
    got = describe(150)
    assert got is not None, "функция ничего не возвращает — не забудьте return"
    assert isinstance(got, str), f"функция вернула {type(got).__name__}, а нужна строка"
    assert "class" not in got, f"получилось {got!r}: нужно имя класса type(value).__name__, а не сам класс"
    assert got == "int: 150", f"describe(150) вернула {got!r}, а нужно \"int: 150\""


def test_others():
    "describe(\"латте\") и describe([1, 2])"
    assert describe("латте") == "str: латте", f"describe(\"латте\") вернула {describe('латте')!r}"
    assert describe([1, 2]) == "list: [1, 2]", f"describe([1, 2]) вернула {describe([1, 2])!r}"
# ─── другое решение ───
def describe(value):
    name = type(value).__name__
    return name + ": " + str(value)
# ─── ошибка ───
def describe(value):
    return f"{type(value)}: {value}"
# ─── ошибка ───
def describe(value):
    print(f"{type(value).__name__}: {value}")
