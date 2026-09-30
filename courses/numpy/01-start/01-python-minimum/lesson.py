# Урок np-python-minimum. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% lists
scores = [72, 85, 90, 64, 88, 95]
print(scores[0], scores[-1])   # первый и последний
print(scores[1:3])             # элементы с индексами 1 и 2
print(len(scores))

# %% last-three [exercise]
last3 = scores[-3:]
# ─── заготовка ───
last3 = ...
# ─── проверка ───
def test_list():
    "last3 — список из трёх баллов"
    assert isinstance(last3, list), f"last3 — это {type(last3).__name__}, а нужен список: срез списка — тоже список"
    assert len(last3) == 3, f"в last3 {len(last3)} элементов, а нужно 3"


def test_values():
    "это три последних балла"
    assert isinstance(last3, list), "last3 пока не список — сначала исправьте то, о чём говорит проверка выше"
    assert last3 != [72, 85, 90], "это три первых балла, а нужны последние: считайте с конца"
    assert last3 == [64, 88, 95], f"в last3 {last3}, а три последних балла — [64, 88, 95]"
# ─── другое решение ───
last3 = scores[3:]
# ─── ошибка ───
last3 = scores[:3]

# %% dicts
stock = {"кофе": 12, "чай": 30, "сахар": 7}
print(stock["кофе"])
stock["молоко"] = 4
print(stock)

# %% stock [exercise]
tea = stock["чай"]
stock["какао"] = 5
# ─── заготовка ───
tea = ...
# добавьте в stock какао — 5 штук
# ─── проверка ───
def test_tea():
    "tea — остаток чая"
    assert tea == 30, f"tea = {tea!r}, а чая на складе 30 — возьмите значение по ключу \"чай\""


def test_cocoa():
    "в stock появилось какао, 5 штук"
    assert "какао" in stock, "в stock нет ключа \"какао\" — добавьте его: stock[\"какао\"] = 5"
    assert stock["какао"] == 5, f"какао в stock — {stock['какао']!r}, а нужно 5"
# ─── другое решение ───
tea = stock.get("чай")
stock.update({"какао": 5})
# ─── ошибка ───
tea = stock["чай"]

# %% loops
sales = [3, 0, 5, 2, 0, 4]
days_with_sales = 0
for s in sales:
    if s > 0:
        days_with_sales = days_with_sales + 1
print(days_with_sales)

# %% positive [exercise]
profit = [1200, -300, 450, 0, -150, 800]
positive_total = 0
for p in profit:
    if p > 0:
        positive_total = positive_total + p
# ─── заготовка ───
profit = [1200, -300, 450, 0, -150, 800]
positive_total = ...
# ─── проверка ───
def test_total():
    "сумма только положительных значений"
    assert positive_total != 2000, "2000 — сумма всех значений вместе с убытками; складывайте только те, что больше нуля"
    assert positive_total == 2450, f"positive_total = {positive_total!r}, а сумма прибыльных дней — 2450"
# ─── другое решение ───
profit = [1200, -300, 450, 0, -150, 800]
positive_total = sum(p for p in profit if p > 0)
# ─── ошибка ───
profit = [1200, -300, 450, 0, -150, 800]
positive_total = sum(profit)

# %% functions
def with_discount(price, percent):
    return price * (100 - percent) / 100


print(with_discount(200, 10))
print(with_discount(80, 25))

# %% average [exercise]
def average(numbers):
    return sum(numbers) / len(numbers)
# ─── заготовка ───
def average(numbers):
    ...  # верните среднее
# ─── проверка ───
def test_simple():
    "average([2, 4, 6]) = 4"
    got = average([2, 4, 6])
    assert got is not None, "функция ничего не возвращает — не забудьте return"
    assert got == 4, f"average([2, 4, 6]) вернула {got!r}, а среднее — 4"


def test_fraction():
    "среднее может быть дробным: average([1, 2]) = 1.5"
    got = average([1, 2])
    assert got is not None, "функция ничего не возвращает — не забудьте return"
    assert got == 1.5, f"average([1, 2]) вернула {got!r}, а нужно 1.5 — делите обычным делением /"
# ─── другое решение ───
def average(numbers):
    total = 0
    for n in numbers:
        total = total + n
    return total / len(numbers)
# ─── ошибка ───
def average(numbers):
    print(sum(numbers) / len(numbers))
# ─── ошибка ───
def average(numbers):
    return sum(numbers) // len(numbers)

# %% comprehension
prices = [120, 80, 45, 300]
print([p * 2 for p in prices])
print([p for p in prices if p < 100])

# %% squares [exercise]
squares = [x ** 2 for x in range(1, 11)]
# ─── заготовка ───
squares = ...
# ─── проверка ───
def test_squares():
    "squares — квадраты чисел от 1 до 10"
    assert isinstance(squares, list), f"squares — это {type(squares).__name__}, а нужен список: [выражение for x in ...]"
    assert squares != [x ** 2 for x in range(10)], "получились квадраты чисел от 0 до 9: начните диапазон с 1 и закончите на 11"
    assert squares == [1, 4, 9, 16, 25, 36, 49, 64, 81, 100], f"в squares {squares}"
# ─── другое решение ───
squares = [x * x for x in range(1, 11)]
# ─── ошибка ───
squares = [x ** 2 for x in range(10)]
