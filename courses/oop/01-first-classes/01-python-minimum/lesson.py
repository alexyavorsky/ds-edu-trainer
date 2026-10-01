# Урок oop-python-minimum. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% menu
menu = {"эспрессо": 150, "капучино": 220, "чай": 120, "раф": 260, "какао": 190}
for name, price in menu.items():
    print(f"{name}: {price} ₽")
print("позиций в меню:", len(menu))

# %% menu-total [exercise]
total = sum(menu.values())
# ─── заготовка ───
total = ...
# ─── проверка ───
def test_total():
    "total — стоимость всех напитков меню"
    assert total != 5, "5 — это число позиций, а нужна сумма цен: сложите значения словаря"
    assert total == 940, f"total = {total!r}, а сумма цен меню — 940 ₽"
# ─── другое решение ───
total = 0
for price in menu.values():
    total = total + price
# ─── ошибка ───
total = len(menu)

# %% comprehension
volumes = [250, 300, 400]
print([v * 2 for v in volumes])
print([v for v in volumes if v > 280])

# %% cheap [exercise]
cheap = [name for name, price in menu.items() if price < 200]
# ─── заготовка ───
cheap = ...
# ─── проверка ───
def test_cheap():
    "cheap — названия напитков дешевле 200 ₽"
    assert isinstance(cheap, list), f"cheap — это {type(cheap).__name__}, а нужен список названий"
    assert cheap != [150, 120, 190], "в списке цены, а нужны названия напитков"
    assert "какао" in cheap, "какао стоит 190 ₽ — меньше 200, его тоже нужно взять"
    assert cheap == ["эспрессо", "чай", "какао"], f"в cheap {cheap}, а дешевле 200 ₽ — эспрессо, чай и какао"
# ─── другое решение ───
cheap = []
for name in menu:
    if menu[name] < 200:
        cheap.append(name)
# ─── ошибка ───
cheap = [price for name, price in menu.items() if price < 200]
# ─── ошибка ───
cheap = [name for name, price in menu.items() if price < 190]

# %% functions
def per_cup(price, cups=1):
    return price / cups


print(per_cup(300))
print(per_cup(300, 4))

# %% with-tip [exercise]
def with_tip(amount, percent=10):
    return round(amount + amount * percent / 100)
# ─── заготовка ───
def with_tip(amount, percent=10):
    ...  # верните сумму с чаевыми
# ─── проверка ───
def test_default():
    "with_tip(500) = 550 — по умолчанию 10 %"
    try:
        got = with_tip(500)
    except TypeError:
        assert False, "with_tip(500) не вызывается с одним аргументом — дайте параметру percent значение по умолчанию 10"
    assert got is not None, "функция ничего не возвращает — не забудьте return"
    assert got != 50, "50 — это только чаевые, а нужна сумма вместе с ними"
    assert got == 550, f"with_tip(500) вернула {got!r}, а нужно 550"


def test_percent():
    "with_tip(480, 5) = 504, with_tip(333, 15) = 383"
    got = with_tip(480, 5)
    assert got == 504, f"with_tip(480, 5) вернула {got!r}, а нужно 504"
    got = with_tip(333, 15)
    assert got == 383, f"with_tip(333, 15) вернула {got!r}, а нужно 383 — округлите итог функцией round"
# ─── другое решение ───
def with_tip(amount, percent=10):
    return round(amount * (100 + percent) / 100)
# ─── ошибка ───
def with_tip(amount, percent=10):
    print(round(amount + amount * percent / 100))
# ─── ошибка ───
def with_tip(amount, percent=10):
    return amount + amount * percent / 100

# %% counter
stock = {"зёрна": 12, "молоко": 4}
print(stock.get("молоко", 0))
print(stock.get("сливки", 0))

# %% count-orders [exercise]
orders = ["капучино", "чай", "капучино", "раф", "чай", "капучино"]
counts = {}
for drink in orders:
    counts[drink] = counts.get(drink, 0) + 1
# ─── заготовка ───
orders = ["капучино", "чай", "капучино", "раф", "чай", "капучино"]
counts = ...
# ─── проверка ───
def test_counts():
    "counts — сколько раз заказали каждый напиток"
    assert isinstance(counts, dict), f"counts — это {type(counts).__name__}, а нужен словарь"
    assert counts.get("капучино") != 1, "у капучино 1, а его заказали трижды — увеличивайте счётчик, а не записывайте 1"
    assert counts == {"капучино": 3, "чай": 2, "раф": 1}, f"в counts {counts}, а нужно капучино — 3, чай — 2, раф — 1"
# ─── другое решение ───
orders = ["капучино", "чай", "капучино", "раф", "чай", "капучино"]
counts = {}
for drink in orders:
    if drink in counts:
        counts[drink] += 1
    else:
        counts[drink] = 1
# ─── ошибка ───
orders = ["капучино", "чай", "капучино", "раф", "чай", "капучино"]
counts = {}
for drink in orders:
    counts[drink] = 1

# %% try-except
for text in ["3", "три"]:
    try:
        print(int(text) * 2)
    except ValueError:
        print(f"не число: {text}")

# %% parse-price [exercise]
def parse_price(text):
    try:
        return int(text)
    except ValueError:
        return None
# ─── заготовка ───
def parse_price(text):
    ...  # число или None
# ─── проверка ───
def test_number():
    "parse_price(\"250\") = 250 — число, а не строка"
    got = parse_price("250")
    assert got != "250", "функция вернула строку \"250\", а нужно число: int(text)"
    assert got == 250, f"parse_price(\"250\") вернула {got!r}, а нужно 250"


def test_not_number():
    "parse_price(\"бесплатно\") и parse_price(\"\") — None"
    try:
        a, b = parse_price("бесплатно"), parse_price("")
    except ValueError:
        assert False, "int(\"бесплатно\") выбрасывает ValueError — перехватите его в try/except и верните None"
    assert a is None and b is None, f"для нечисловых строк функция вернула {a!r} и {b!r}, а нужно None"
# ─── другое решение ───
def parse_price(text):
    if text.isdigit():
        return int(text)
    return None
# ─── ошибка ───
def parse_price(text):
    return int(text)
# ─── ошибка ───
def parse_price(text):
    try:
        return int(text)
    except ValueError:
        return 0
