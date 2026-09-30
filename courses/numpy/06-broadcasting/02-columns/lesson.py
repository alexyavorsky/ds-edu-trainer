# Урок np-columns. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% newaxis
import numpy as np

prices = np.array([
    [120, 80, 45, 300],
    [130, 85, 50, 290],
    [110, 90, 40, 310],
])
markup = np.array([1.1, 1.2, 1.05])
print(markup.shape, markup[:, np.newaxis].shape)
prices * markup[:, np.newaxis]

# %% store-markup [exercise]
store_markup = np.array([1.25, 1.0, 1.1])
final = prices * store_markup[:, np.newaxis]
# ─── заготовка ───
store_markup = np.array([1.25, 1.0, 1.1])
final = ...
# ─── проверка ───
def test_shape():
    "final — таблица 3 × 4"
    assert isinstance(final, np.ndarray), f"final — это {type(final).__name__}, а нужен массив"
    assert final.shape == (3, 4), f"форма final — {final.shape}, а должна остаться (3, 4)"


def test_values():
    "каждая строка умножена на наценку своего магазина"
    assert isinstance(final, np.ndarray) and final.shape == (3, 4), "сначала исправьте то, о чём говорит проверка выше"
    assert np.allclose(final, [[150, 100, 56.25, 375], [130, 85, 50, 290], [121, 99, 44, 341]]), f"final = {final.tolist()}"
# ─── другое решение ───
store_markup = np.array([1.25, 1.0, 1.1])
final = prices * store_markup.reshape(3, 1)
# ─── ошибка ───
store_markup = np.array([1.25, 1.0, 1.1])
final = prices * store_markup
# ─── ошибка ───
store_markup = np.array([1.25, 1.0, 1.1])
final = prices * store_markup.mean()

# %% keepdims
monthly = np.array([
    [40, 42, 45, 50, 48, 52, 55, 58, 50, 47, 60, 75],
    [30, 28, 33, 35, 40, 38, 36, 35, 39, 58, 45, 55],
    [70, 72, 68, 75, 80, 85, 90, 125, 82, 79, 95, 120],
])
year = monthly.sum(axis=1, keepdims=True)
print(year.shape)
shares = monthly / year
print(shares.sum(axis=1))
print(np.round(shares[:, -1] * 100, 1))   # доля декабря, %

# %% personal [exercise]
scores = np.loadtxt("data/scores.csv", delimiter=",", skiprows=1, usecols=(1, 2, 3, 4, 5))
personal = scores - scores.mean(axis=1, keepdims=True)
# ─── заготовка ───
scores = np.loadtxt("data/scores.csv", delimiter=",", skiprows=1, usecols=(1, 2, 3, 4, 5))
personal = ...
# ─── проверка ───
def test_shape():
    "personal — таблица 30 × 5"
    assert isinstance(personal, np.ndarray), f"personal — это {type(personal).__name__}, а нужна таблица"
    assert personal.shape == (30, 5), f"форма personal — {personal.shape}, а должна быть (30, 5)"


def test_rows():
    "в каждой строке среднее отклонение — 0"
    assert isinstance(personal, np.ndarray) and personal.shape == (30, 5), "сначала исправьте то, о чём говорит проверка выше"
    assert not np.allclose(personal.mean(axis=0), 0), "вычтено среднее по предметам (axis=0), а нужно среднее каждого студента — axis=1"
    assert np.allclose(personal.mean(axis=1), 0), "в каждой строке среднее должно стать 0: вычитайте scores.mean(axis=1, keepdims=True)"
    assert np.allclose(personal[0], [-1.6, -20.6, -1.6, 12.4, 11.4]), f"у первого студента получилось {np.round(personal[0], 1).tolist()}"
# ─── другое решение ───
scores = np.loadtxt("data/scores.csv", delimiter=",", skiprows=1, usecols=(1, 2, 3, 4, 5))
personal = scores - scores.mean(axis=1)[:, np.newaxis]
# ─── ошибка ───
scores = np.loadtxt("data/scores.csv", delimiter=",", skiprows=1, usecols=(1, 2, 3, 4, 5))
personal = scores - scores.mean(axis=0)

# %% newaxis-shape [quiz]
print((np.arange(3)[:, np.newaxis] * np.arange(4)).shape)

# %% outer
n = np.arange(1, 10)
n[:, np.newaxis] * n

# %% combos [exercise]
unit_price = np.array([120, 80, 45, 300, 15])
amounts = np.array([1, 2, 5, 10])
cost = unit_price[:, np.newaxis] * amounts
# ─── заготовка ───
unit_price = np.array([120, 80, 45, 300, 15])
amounts = np.array([1, 2, 5, 10])
cost = ...
# ─── проверка ───
def test_cost():
    "cost — таблица 5 товаров × 4 количества"
    assert isinstance(cost, np.ndarray), f"cost — это {type(cost).__name__}, а нужна таблица"
    assert cost.shape != (4, 5), "товары оказались в столбцах: цены должны быть столбцом — unit_price[:, np.newaxis]"
    assert cost.shape == (5, 4), f"форма cost — {cost.shape}, а нужно (5, 4)"
    assert cost[3].tolist() == [300, 600, 1500, 3000], f"строка товара за 300 ₽ — {cost[3].tolist()}, а должна быть [300, 600, 1500, 3000]"
# ─── другое решение ───
unit_price = np.array([120, 80, 45, 300, 15])
amounts = np.array([1, 2, 5, 10])
cost = unit_price.reshape(-1, 1) * amounts
# ─── ошибка ───
unit_price = np.array([120, 80, 45, 300, 15])
amounts = np.array([1, 2, 5, 10])
cost = unit_price * amounts[:, np.newaxis]

# %% square
sq = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(sq.mean(axis=1))
print(sq - sq.mean(axis=1))                  # неверно: вычли как строку
print(sq - sq.mean(axis=1, keepdims=True))   # верно: каждая строка минус своё среднее

# %% row-center [exercise]
centered = sq - sq.mean(axis=1, keepdims=True)
# ─── заготовка ───
centered = ...
# ─── проверка ───
def test_centered():
    "в каждой строке среднее стало 0"
    assert isinstance(centered, np.ndarray) and centered.shape == (3, 3), "centered — таблица 3 × 3"
    assert centered.tolist() != [[-1, -3, -5], [2, 0, -2], [5, 3, 1]], "среднее приложилось как строка: добавьте keepdims=True"
    assert centered.tolist() == [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], f"centered = {centered.tolist()}"
# ─── другое решение ───
centered = sq - sq.mean(axis=1)[:, np.newaxis]
# ─── ошибка ───
centered = sq - sq.mean(axis=1)
