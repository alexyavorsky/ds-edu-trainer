# Урок np-matmul. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% dot
import numpy as np

q = np.array([2, 1, 3])          # сколько штук
p = np.array([150, 220, 90])     # цена штуки
print(q * p)
print((q * p).sum())
print(np.dot(q, p))
print(q @ p)

# %% weighted [exercise]
marks = np.array([78, 92, 85])
weights = np.array([0.5, 0.3, 0.2])
final = marks @ weights
# ─── заготовка ───
marks = np.array([78, 92, 85])
weights = np.array([0.5, 0.3, 0.2])
final = ...
# ─── проверка ───
def test_final():
    "final — итоговая оценка"
    assert not isinstance(final, np.ndarray) or final.shape == (), "final — массив: это поэлементное произведение *, а нужна сумма — @"
    assert abs(final - 255 / 3) > 1e-6, "это простое среднее трёх оценок, а нужно взвешенное: marks @ weights"
    assert abs(final - 83.6) < 1e-9, f"final = {final}, а взвешенная оценка — 0.5·78 + 0.3·92 + 0.2·85 = 83.6"
# ─── другое решение ───
marks = np.array([78, 92, 85])
weights = np.array([0.5, 0.3, 0.2])
final = np.dot(marks, weights)
# ─── ошибка ───
marks = np.array([78, 92, 85])
weights = np.array([0.5, 0.3, 0.2])
final = marks * weights
# ─── ошибка ───
marks = np.array([78, 92, 85])
weights = np.array([0.5, 0.3, 0.2])
final = marks.mean()

# %% orders
orders = np.array([
    [2, 1, 0, 3],
    [0, 2, 1, 1],
    [1, 0, 4, 0],
    [3, 3, 0, 2],
    [0, 1, 2, 5],
])
prices = np.array([180, 250, 90, 60])
print(orders.shape, prices.shape)
print(orders @ prices)

# %% mismatch [raises=ValueError]
orders @ np.array([180, 250, 90])

# %% grades [exercise]
scores = np.array([
    [78, 85, 90],
    [62, 70, 58],
    [91, 88, 95],
    [55, 80, 72],
])
finals = scores @ weights
best = finals.argmax()
# ─── заготовка ───
scores = np.array([
    [78, 85, 90],
    [62, 70, 58],
    [91, 88, 95],
    [55, 80, 72],
])
finals = ...
best = ...
# ─── проверка ───
def test_finals():
    "finals — итоги четырёх студентов"
    assert isinstance(finals, np.ndarray), f"finals — это {type(finals).__name__}, а нужен массив из четырёх итогов"
    assert finals.shape != (4, 3), "finals — таблица (4, 3): это поэлементное *, а суммы по строкам даёт @"
    assert finals.shape == (4,), f"у finals форма {finals.shape}, а студентов 4"
    assert np.allclose(finals, [82.5, 63.6, 90.9, 65.9]), f"finals = {finals}, а итоги с весами 0.5, 0.3, 0.2 — [82.5, 63.6, 90.9, 65.9]"


def test_best():
    "best — строка лучшего студента"
    assert best == 2, f"best = {best}, а лучший итог (90.9) — у студента в строке 2"
# ─── другое решение ───
scores = np.array([
    [78, 85, 90],
    [62, 70, 58],
    [91, 88, 95],
    [55, 80, 72],
])
finals = (scores * weights).sum(axis=1)
best = np.argmax(finals)
# ─── ошибка ───
scores = np.array([
    [78, 85, 90],
    [62, 70, 58],
    [91, 88, 95],
    [55, 80, 72],
])
finals = scores * weights
best = finals.argmax()

# %% two-cols
price_cost = np.array([
    [180, 70],     # цена, себестоимость
    [250, 110],
    [90, 30],
    [60, 15],
])
print(orders.shape, price_cost.shape)
print(orders @ price_cost)

# %% shape-quiz [quiz]
print((np.ones((5, 3)) @ np.ones((3, 2))).shape)

# %% profit [exercise]
rc = orders @ price_cost
profit = rc[:, 0] - rc[:, 1]
total_profit = profit.sum()
# ─── заготовка ───
rc = ...
profit = ...
total_profit = ...
# ─── проверка ───
def test_rc():
    "rc — выручка и затраты каждого заказа"
    assert isinstance(rc, np.ndarray) and rc.shape == (5, 2), f"rc — таблица (5, 2): orders @ price_cost"
    assert rc[:, 0].tolist() == [790, 650, 540, 1410, 730], "столбец 0 rc — выручка заказов: orders @ price_cost"


def test_profit():
    "profit и total_profit — прибыль"
    assert np.shape(profit) == (5,), f"у profit форма {np.shape(profit)}, а заказов 5: выручка минус затраты по строкам"
    assert profit.tolist() == [495, 385, 350, 840, 485], f"profit = {profit.tolist()}, а прибыль заказов — [495, 385, 350, 840, 485]"
    assert total_profit == 2555, f"total_profit = {total_profit}, а общая прибыль — 2555"
# ─── другое решение ───
rc = np.dot(orders, price_cost)
profit = orders @ (price_cost[:, 0] - price_cost[:, 1])
total_profit = np.sum(profit)
# ─── ошибка ───
rc = orders @ price_cost
profit = rc[:, 1] - rc[:, 0]
total_profit = profit.sum()
