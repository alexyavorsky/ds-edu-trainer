# Урок np-reshape. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% basic
import numpy as np

nums = np.arange(12)
print(nums)
print(nums.reshape(3, 4))
print(nums.reshape(2, 6))

# %% grid [exercise]
grid = np.arange(1, 21).reshape(4, 5)
# ─── заготовка ───
grid = ...
# ─── проверка ───
def test_shape():
    "grid — таблица 4 × 5"
    assert isinstance(grid, np.ndarray), f"grid — это {type(grid).__name__}, а нужен массив"
    assert grid.shape != (5, 4), "получилось 5 строк и 4 столбца: в reshape сначала строки — reshape(4, 5)"
    assert grid.shape == (4, 5), f"форма grid — {grid.shape}, а нужно (4, 5)"


def test_values():
    "числа от 1 до 20 по строкам"
    assert isinstance(grid, np.ndarray) and grid.shape == (4, 5), "сначала исправьте то, о чём говорит проверка выше"
    assert grid[0, 0] != 0, "таблица начинается с 0, а нужно с 1: np.arange(1, 21)"
    assert grid.tolist() == [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20]], f"в grid {grid.tolist()}"
# ─── другое решение ───
grid = np.arange(20).reshape(4, 5) + 1
# ─── ошибка ───
grid = np.arange(20).reshape(4, 5)
# ─── ошибка ───
grid = np.arange(1, 21).reshape(5, 4)

# %% weeks
tmax = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=2)
weeks = tmax[:364].reshape(52, 7)
print(weeks.shape)
print(weeks[0])            # первая неделя
print(weeks[:, 0].shape)   # все среды

# %% bad-shape [raises=ValueError]
tmax[:364].reshape(5, 7)

# %% minus-one
print(tmax[:364].reshape(-1, 7).shape)
print(np.arange(10).reshape(-1, 2))

# %% by-week [exercise]
tmin = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=1)
tmin_weeks = tmin[:364].reshape(-1, 7)
# ─── заготовка ───
tmin = ...
tmin_weeks = ...
# ─── проверка ───
def test_tmin():
    "tmin — 365 минимальных температур"
    assert isinstance(tmin, np.ndarray) and tmin.shape == (365,), "tmin — это столбец 1 из файла: np.loadtxt(..., usecols=1)"
    assert tmin.min() == -14.9, "tmin — не столбец минимальных температур: его номер 1"


def test_weeks():
    "tmin_weeks — 52 недели по 7 дней"
    assert isinstance(tmin_weeks, np.ndarray), f"tmin_weeks — это {type(tmin_weeks).__name__}, а нужен массив"
    assert tmin_weeks.shape != (7, 52), "получилось 7 строк по 52: в строке должна быть неделя — reshape(-1, 7)"
    assert tmin_weeks.shape == (52, 7), f"форма tmin_weeks — {tmin_weeks.shape}, а нужно (52, 7)"
    assert tmin_weeks[0].tolist() == tmin[:7].tolist(), "первая строка должна быть первой неделей года"
# ─── другое решение ───
tmin = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=1)
tmin_weeks = tmin[:364].reshape(52, 7)
# ─── ошибка ───
tmin = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=1)
tmin_weeks = tmin[:364].reshape(7, -1)

# %% minus-one-shape [quiz]
print(np.arange(24).reshape(-1, 6).shape)

# %% ravel
table = np.arange(6).reshape(2, 3)
print(table)
print(table.ravel())

# %% flat [exercise]
flat_tmin = tmin_weeks.ravel()
# ─── заготовка ───
flat_tmin = ...
# ─── проверка ───
def test_flat():
    "flat_tmin — снова ряд из 364 значений"
    assert isinstance(flat_tmin, np.ndarray), f"flat_tmin — это {type(flat_tmin).__name__}, а нужен массив"
    assert flat_tmin.ndim == 1, f"у flat_tmin форма {flat_tmin.shape}, а нужен одномерный массив: ravel()"
    assert flat_tmin.tolist() == tmin[:364].tolist(), "значения должны идти в исходном порядке — первые 364 дня tmin"
# ─── другое решение ───
flat_tmin = tmin_weeks.reshape(-1)
# ─── ошибка ───
flat_tmin = tmin_weeks.T.ravel()

# %% transpose
print(weeks.T.shape)
print(weeks.T[0][:5])   # первые пять сред года

# %% days-rows [exercise]
by_day = tmin_weeks.T
thursdays = by_day[1]
# ─── заготовка ───
by_day = ...
thursdays = ...
# ─── проверка ───
def test_by_day():
    "by_day — 7 строк по 52 недели"
    assert isinstance(by_day, np.ndarray), f"by_day — это {type(by_day).__name__}, а нужен массив: tmin_weeks.T"
    assert by_day.shape == (7, 52), f"форма by_day — {by_day.shape}, а нужно (7, 52): поверните tmin_weeks через .T"


def test_thursdays():
    "thursdays — минимальные температуры всех четвергов"
    assert isinstance(thursdays, np.ndarray), f"thursdays — это {type(thursdays).__name__}, а нужна строка by_day"
    assert thursdays.shape == (52,), f"у thursdays форма {thursdays.shape}, а нужно 52 значения — одна строка by_day"
    assert thursdays.tolist() != tmin[0:364:7].tolist(), "это среды (строка 0); четверги — строка 1"
    assert thursdays.tolist() == tmin[1:364:7].tolist(), "это не четверги: год начался в среду, четверг — второй день, строка 1"
# ─── другое решение ───
by_day = tmin_weeks.T
thursdays = tmin_weeks[:, 1]
# ─── ошибка ───
by_day = tmin_weeks.T
thursdays = by_day[0]
# ─── ошибка ───
by_day = tmin_weeks.reshape(7, 52)
thursdays = by_day[1]
