# Урок np-broadcasting. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% row
import numpy as np

prices = np.array([
    [120, 80, 45, 300],   # магазин 1: четыре товара
    [130, 85, 50, 290],   # магазин 2
    [110, 90, 40, 310],   # магазин 3
])
delivery = np.array([20, 10, 5, 40])   # доставка каждого товара
print(prices.shape, delivery.shape)
prices + delivery

# %% discount [exercise]
discount = np.array([0.9, 1.0, 0.8, 0.95])
discounted = prices * discount
# ─── заготовка ───
discount = np.array([0.9, 1.0, 0.8, 0.95])
discounted = ...
# ─── проверка ───
def test_shape():
    "discounted — таблица 3 × 4"
    assert isinstance(discounted, np.ndarray), f"discounted — это {type(discounted).__name__}, а нужен массив: prices * discount"
    assert discounted.shape == (3, 4), f"форма discounted — {discounted.shape}, а должна остаться (3, 4)"


def test_values():
    "у каждого товара своя скидка"
    assert isinstance(discounted, np.ndarray) and discounted.shape == (3, 4), "сначала исправьте то, о чём говорит проверка выше"
    assert np.allclose(discounted, [[108, 80, 36, 285], [117, 85, 40, 275.5], [99, 90, 32, 294.5]]), f"discounted = {discounted.tolist()}: сравните с prices * discount — у каждого столбца (товара) своя скидка"
# ─── другое решение ───
discount = np.array([0.9, 1.0, 0.8, 0.95])
discounted = discount * prices
# ─── ошибка ───
discount = np.array([0.9, 1.0, 0.8, 0.95])
discounted = prices * discount.mean()

# %% rule [quiz]
print((np.zeros((3, 4)) + np.zeros(4)).shape)

# %% deviation
scores = np.loadtxt("data/scores.csv", delimiter=",", skiprows=1, usecols=(1, 2, 3, 4, 5))
subject_mean = scores.mean(axis=0)
print(subject_mean.shape)
print(np.round(scores[:3] - subject_mean, 1))

# %% above-avg [exercise]
dev = scores - scores.mean(axis=0)
above = (dev > 0).sum()
# ─── заготовка ───
dev = ...
above = ...
# ─── проверка ───
def test_dev():
    "dev — отклонения от средних по предметам"
    assert isinstance(dev, np.ndarray), f"dev — это {type(dev).__name__}, а нужна таблица"
    assert dev.shape == (30, 5), f"форма dev — {dev.shape}, а должна быть (30, 5)"
    assert np.allclose(dev.mean(axis=0), 0), "среднее отклонение по каждому предмету должно быть 0 — вычитайте scores.mean(axis=0)"


def test_above():
    "above — оценки выше среднего своего предмета"
    assert above == 74, f"above = {above}, а оценок выше среднего по предмету — 74"
# ─── другое решение ───
dev = scores - np.mean(scores, axis=0)
above = np.sum(scores > scores.mean(axis=0))
# ─── ошибка ───
dev = scores - scores.mean()
above = (dev > 0).sum()

# %% mismatch [raises=ValueError]
store_markup = np.array([1.1, 1.2, 1.05])
prices * store_markup

# %% weeks
tmax = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=2)
weeks = tmax[:364].reshape(52, 7)
print(weeks.shape, weeks.mean(axis=0).shape)

# %% weekly [exercise]
vs_weekday = weeks - weeks.mean(axis=0)
# ─── заготовка ───
vs_weekday = ...
# ─── проверка ───
def test_shape():
    "vs_weekday — таблица той же формы, что weeks"
    assert isinstance(vs_weekday, np.ndarray) and vs_weekday.shape == weeks.shape, f"vs_weekday должна быть той же формы, что weeks: {weeks.shape}"


def test_values():
    "по каждому дню недели среднее отклонение — 0"
    assert isinstance(vs_weekday, np.ndarray) and vs_weekday.shape == weeks.shape, "сначала исправьте то, о чём говорит проверка выше"
    assert np.allclose(vs_weekday.mean(axis=0), 0), "вычитайте среднее по столбцам — weeks.mean(axis=0)"
# ─── другое решение ───
vs_weekday = weeks - np.mean(weeks, axis=0)
# ─── ошибка ───
vs_weekday = weeks - weeks.mean()
