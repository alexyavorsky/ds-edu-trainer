# Урок np-axis. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% sales
import numpy as np

sales = np.array([
    [120, 135, 150, 170],   # магазин 1: кварталы 1–4
    [ 90, 100,  95, 130],   # магазин 2
    [200, 180, 210, 250],   # магазин 3
])
print(sales.shape)
print(sales.sum())

# %% axis-sums
print(sales.sum(axis=0))   # по каждому кварталу (столбцу)
print(sales.sum(axis=1))   # по каждому магазину (строке)

# %% per-store [exercise]
store_totals = sales.sum(axis=1)
# ─── заготовка ───
store_totals = ...
# ─── проверка ───
def test_totals():
    "store_totals — годовые продажи трёх магазинов"
    assert isinstance(store_totals, np.ndarray), f"store_totals — это {type(store_totals).__name__}, а нужен массив из трёх чисел: sum с axis"
    got = store_totals.tolist()
    assert got != [410, 415, 455, 550], "получились суммы кварталов (4 числа): чтобы получить по числу на магазин, сворачивайте столбцы"
    assert got == [575, 415, 840], f"store_totals = {got} — это не годовые продажи магазинов"
# ─── другое решение ───
store_totals = np.sum(sales, axis=1)
# ─── ошибка ───
store_totals = sales.sum(axis=0)

# %% per-quarter [exercise]
quarter_avg = sales.mean(axis=0)
# ─── заготовка ───
quarter_avg = ...
# ─── проверка ───
def test_avg():
    "quarter_avg — средний магазин в каждом квартале"
    assert isinstance(quarter_avg, np.ndarray), f"quarter_avg — это {type(quarter_avg).__name__}, а нужен массив из четырёх чисел"
    got = np.asarray(quarter_avg, dtype=float)
    assert got.shape != (3,), "получилось по числу на магазин: для кварталов сворачивайте строки"
    assert np.allclose(got, [136.666667, 138.333333, 151.666667, 183.333333]), f"quarter_avg = {np.round(got, 2).tolist()}"
# ─── другое решение ───
quarter_avg = sales.sum(axis=0) / 3
# ─── ошибка ───
quarter_avg = sales.mean(axis=1)

# %% axis-shape [quiz]
print(np.zeros((3, 4)).sum(axis=0).shape)

# %% weeks
tmax = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=2)
weeks = tmax[:364].reshape(52, 7)
week_mean = weeks.mean(axis=1)
print(week_mean.shape)
print("самая холодная неделя:", week_mean.argmin() + 1, "—", round(week_mean.min(), 1), "°C")

# %% hot-week [exercise]
week_max = weeks.max(axis=1)
hottest_week = week_max.argmax() + 1
# ─── заготовка ───
week_max = ...
hottest_week = ...
# ─── проверка ───
def test_week_max():
    "week_max — максимум каждой недели"
    assert isinstance(week_max, np.ndarray), f"week_max — это {type(week_max).__name__}, а нужен массив"
    assert week_max.shape != (7,), "получилось 7 чисел — по дню недели; для недель сворачивайте столбцы"
    assert week_max.shape == (52,), f"у week_max форма {week_max.shape}, а нужно 52 числа — по одному на неделю"
    assert week_max.max() == 27.2, "это не максимумы недель"


def test_hottest():
    "hottest_week — номер самой жаркой недели"
    assert hottest_week != 28, "28 — индекс, а недели нумеруются с 1"
    assert hottest_week == 29, f"hottest_week = {hottest_week} — это не номер самой жаркой недели"
# ─── другое решение ───
week_max = np.max(weeks, axis=1)
hottest_week = np.argmax(week_max) + 1
# ─── ошибка ───
week_max = weeks.max(axis=0)
hottest_week = week_max.argmax() + 1
# ─── ошибка ───
week_max = weeks.max(axis=1)
hottest_week = week_max.argmax()

# %% weekday [exercise]
by_weekday = weeks.mean(axis=0)
# ─── заготовка ───
by_weekday = ...
# ─── проверка ───
def test_weekday():
    "by_weekday — среднее каждого дня недели"
    assert isinstance(by_weekday, np.ndarray), f"by_weekday — это {type(by_weekday).__name__}, а нужен массив из 7 чисел"
    assert by_weekday.shape != (52,), "получилось 52 числа — по неделе; для дней недели сворачивайте строки"
    assert np.allclose(by_weekday, [9.387, 9.279, 8.919, 9.096, 8.737, 9.427, 9.231], atol=1e-3), f"by_weekday = {np.round(by_weekday, 2).tolist()}"
# ─── другое решение ───
by_weekday = weeks.T.mean(axis=1)
# ─── ошибка ───
by_weekday = weeks.mean(axis=1)
