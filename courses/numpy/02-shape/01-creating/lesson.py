# Урок np-creating. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% zeros-ones
import numpy as np

print(np.zeros(5))
print(np.ones(3))
print(np.full(4, 7))

# %% savings [exercise]
plan = np.full(12, 5000)
year_total = plan.sum()
# ─── заготовка ───
plan = ...
year_total = ...
# ─── проверка ───
def test_plan():
    "plan — 12 взносов по 5000"
    assert isinstance(plan, np.ndarray), f"plan — это {type(plan).__name__}, а нужен массив"
    assert len(plan) == 12, f"в plan {len(plan)} взносов, а месяцев в году 12"
    assert np.asarray(plan).tolist() == [5000] * 12, f"в plan {np.asarray(plan).tolist()}, а каждый взнос — 5000"


def test_total():
    "year_total — сумма за год"
    assert year_total == 60000, f"year_total = {year_total} — это не сумма взносов за год"
# ─── другое решение ───
plan = np.ones(12) * 5000
year_total = np.sum(plan)
# ─── ошибка ───
plan = np.full(5000, 12)
year_total = plan.sum()

# %% arange
print(np.arange(5))
print(np.arange(1, 10))
print(np.arange(0, 50, 10))

# %% hours [exercise]
hours = np.arange(24)
# ─── заготовка ───
hours = ...
# ─── проверка ───
def test_hours():
    "hours — числа от 0 до 23"
    assert isinstance(hours, np.ndarray), f"hours — это {type(hours).__name__}, а нужен массив"
    got = np.asarray(hours).tolist()
    assert got != list(range(23)), "не хватает часа 23: конец в arange не входит"
    assert got != list(range(1, 25)), "часы суток начинаются с 0 и заканчиваются на 23"
    assert got == list(range(24)), f"в hours {got}"
# ─── другое решение ───
hours = np.arange(0, 24)
# ─── ошибка ───
hours = np.arange(23)
# ─── ошибка ───
hours = np.arange(1, 25)

# %% even [exercise]
even = np.arange(2, 21, 2)
# ─── заготовка ───
even = ...
# ─── проверка ───
def test_even():
    "even — чётные числа от 2 до 20 включительно"
    assert isinstance(even, np.ndarray), f"even — это {type(even).__name__}, а нужен массив с шагом 2"
    got = np.asarray(even).tolist()
    assert got != [2, 4, 6, 8, 10, 12, 14, 16, 18], "не хватает 20: конец в arange не входит"
    assert got == [2, 4, 6, 8, 10, 12, 14, 16, 18, 20], f"в even {got}"
# ─── другое решение ───
even = np.arange(1, 11) * 2
# ─── ошибка ───
even = np.arange(2, 20, 2)

# %% arange-step [quiz]
np.arange(1, 10, 3)

# %% linspace
print(np.linspace(0, 1, 5))
print(np.linspace(10, 20, 3))

# %% price-steps [exercise]
levels = np.linspace(100, 300, 5)
# ─── заготовка ───
levels = ...
# ─── проверка ───
def test_levels():
    "levels — пять ступеней от 100 до 300"
    assert isinstance(levels, np.ndarray), f"levels — это {type(levels).__name__}, а нужен массив"
    got = np.asarray(levels, dtype=float)
    assert len(got) == 5, f"в levels {len(got)} значений, а нужно 5: вспомните, какой аргумент linspace задаёт число значений"
    assert np.allclose(got, [100, 150, 200, 250, 300]), f"в levels {got.tolist()}: ступени должны идти от 100 до 300 через равные промежутки"
# ─── другое решение ───
levels = np.arange(100, 301, 50)
# ─── ошибка ───
levels = np.linspace(100, 300, 50)
