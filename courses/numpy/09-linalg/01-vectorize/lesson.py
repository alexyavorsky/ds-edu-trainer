# Урок np-vectorize. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% ufuncs
import numpy as np

print(np.sqrt(np.array([4, 9, 2])))
print(np.abs(np.array([-3, 0, 2.5, -7])))

# %% distance [exercise]
dx = np.array([3.0, 5.0, 1.5, 8.0, 6.0])
dy = np.array([4.0, 12.0, 2.0, 6.0, 2.5])
dist = np.sqrt(dx ** 2 + dy ** 2)
# ─── заготовка ───
dx = np.array([3.0, 5.0, 1.5, 8.0, 6.0])
dy = np.array([4.0, 12.0, 2.0, 6.0, 2.5])
dist = ...
# ─── проверка ───
def test_dist():
    "dist — расстояния до пяти точек"
    assert isinstance(dist, np.ndarray) and dist.shape == (5,), "dist — пять расстояний, по одному на заказ"
    assert not np.allclose(dist, dx + dy), "dist = dx + dy — это путь по улицам; по прямой — корень из суммы квадратов"
    assert not np.allclose(dist, dx ** 2 + dy ** 2), "не хватает корня: np.sqrt(dx ** 2 + dy ** 2)"
    assert np.allclose(dist, [5.0, 13.0, 2.5, 10.0, 6.5]), f"dist = {dist}, а должно быть [5, 13, 2.5, 10, 6.5]"
# ─── другое решение ───
dx = np.array([3.0, 5.0, 1.5, 8.0, 6.0])
dy = np.array([4.0, 12.0, 2.0, 6.0, 2.5])
dist = (dx * dx + dy * dy) ** 0.5
# ─── ошибка ───
dx = np.array([3.0, 5.0, 1.5, 8.0, 6.0])
dy = np.array([4.0, 12.0, 2.0, 6.0, 2.5])
dist = np.sqrt(dx ** 2) + np.sqrt(dy ** 2)

# %% mae [exercise]
actual = np.array([120, 135, 150, 128, 142, 160, 155])
forecast = np.array([118, 140, 145, 130, 150, 152, 158])
mae = np.abs(forecast - actual).mean()
# ─── заготовка ───
actual = np.array([120, 135, 150, 128, 142, 160, 155])
forecast = np.array([118, 140, 145, 130, 150, 152, 158])
mae = ...
# ─── проверка ───
def test_mae():
    "mae — средняя ошибка без учёта знака"
    assert not isinstance(mae, np.ndarray), "mae — массив, а нужно одно число: среднее модулей"
    assert abs(mae - 0.428571) > 1e-3, "это среднее самих разностей — промахи вверх и вниз сократились; возьмите модуль np.abs"
    assert abs(mae - 4.714286) < 1e-5, f"mae = {mae}, а средняя абсолютная ошибка ≈ 4.71"
# ─── другое решение ───
actual = np.array([120, 135, 150, 128, 142, 160, 155])
forecast = np.array([118, 140, 145, 130, 150, 152, 158])
mae = np.mean(np.abs(actual - forecast))
# ─── ошибка ───
actual = np.array([120, 135, 150, 128, 142, 160, 155])
forecast = np.array([118, 140, 145, 130, 150, 152, 158])
mae = (forecast - actual).mean()

# %% log10
population = np.array([1200, 45000, 610000, 1100000, 12600000])
print(np.log10(population))
print(np.log10(population).astype(int) + 1)     # число цифр
print(np.log(np.array([1, 10, 100])))     # натуральный логарифм

# %% sigmoid
x = np.array([-4, -1, 0, 1, 4])
print(np.round(1 / (1 + np.exp(-x)), 3))

# %% maximum
a = np.array([3, -2, 7, -5])
b = np.array([1, 4, 6, 0])
print(np.maximum(a, b))
print(np.maximum(a, 0))      # отрицательные → 0
print(np.minimum(a, 5))      # больше 5 → 5

# %% max-quiz [quiz]
print(np.max(np.array([-2, 5, -1]), 0))

# %% overtime [exercise]
hours = np.array([38, 45, 40, 52, 36, 41])
overtime = np.maximum(hours - 40, 0)
total_overtime = overtime.sum()
# ─── заготовка ───
hours = np.array([38, 45, 40, 52, 36, 41])
overtime = ...
total_overtime = ...
# ─── проверка ───
def test_overtime():
    "overtime — часы переработки"
    assert isinstance(overtime, np.ndarray), "overtime — одно число: np.max(…, 0) — это axis=0; поэлементный максимум — np.maximum"
    assert overtime.shape == (6,), f"у overtime форма {overtime.shape}, а сотрудников 6"
    assert overtime.min() >= 0, "в overtime есть отрицательные: у кого нет переработки — 0, np.maximum(hours - 40, 0)"
    assert overtime.tolist() == [0, 5, 0, 12, 0, 1], f"overtime = {overtime.tolist()}, а должно быть [0, 5, 0, 12, 0, 1]"


def test_total():
    "total_overtime — сумма переработок"
    assert total_overtime == 18, f"total_overtime = {total_overtime}, а всего переработано 18 часов"
# ─── другое решение ───
hours = np.array([38, 45, 40, 52, 36, 41])
overtime = np.where(hours > 40, hours - 40, 0)
total_overtime = np.sum(overtime)
# ─── ошибка ───
hours = np.array([38, 45, 40, 52, 36, 41])
overtime = np.max(hours - 40, 0)
total_overtime = overtime.sum()
# ─── ошибка ───
hours = np.array([38, 45, 40, 52, 36, 41])
overtime = hours - 40
total_overtime = overtime.sum()

# %% rewrite-demo
prices = np.array([80, 150, 95, 240])
result = []
for p in prices:
    if p > 100:
        result.append(p * 0.9)
    else:
        result.append(p)
print(np.array(result))
print(np.where(prices > 100, prices * 0.9, prices))

# %% bonus-loop
scores = np.array([35, 50, 62, 71, 88, 95, 49, 100])
result = []
for s in scores:
    if s >= 50:
        b = (s - 50) * 2
    else:
        b = 0
    if b > 60:
        b = 60
    result.append(b)
print(np.array(result))

# %% bonus [exercise]
bonus = np.minimum(np.maximum(scores - 50, 0) * 2, 60)
# ─── заготовка ───
bonus = ...
# ─── проверка ───
def test_bonus():
    "bonus — те же бонусы, что считает цикл"
    assert isinstance(bonus, np.ndarray), f"bonus — это {type(bonus).__name__}, а нужен массив NumPy, посчитанный без цикла"
    assert bonus.shape == (8,), f"у bonus форма {bonus.shape}, а участников 8"
    assert bonus.min() >= 0, "в bonus есть отрицательные: кто набрал меньше 50, получает 0 — np.maximum(…, 0)"
    assert bonus.max() <= 60, "в bonus есть больше 60: бонус ограничен сверху — np.minimum(…, 60)"
    assert bonus.tolist() == [0, 0, 24, 42, 60, 60, 0, 60], f"bonus = {bonus.tolist()}, а цикл даёт [0, 0, 24, 42, 60, 60, 0, 60]"
# ─── другое решение ───
bonus = np.clip((scores - 50) * 2, 0, 60)
# ─── ошибка ───
bonus = np.maximum(scores - 50, 0) * 2
