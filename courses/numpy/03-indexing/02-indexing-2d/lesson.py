# Урок np-indexing-2d. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import numpy as np

weather = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1)
print(weather.shape)

# %% cell
print(weather[0, 2])     # 1 января, максимум
print(weather[-1, 1])    # 31 декабря, минимум

# %% day10 [exercise]
day10_min = weather[9, 1]
day10_rain = weather[9, 3]
# ─── заготовка ───
day10_min = ...
day10_rain = ...
# ─── проверка ───
def test_min():
    "day10_min — минимальная температура 10 января"
    assert day10_min != weather[10, 1] or weather[10, 1] == weather[9, 1], "это 11 января: 10 января — строка с индексом 9"
    assert day10_min == weather[9, 1], f"day10_min = {day10_min}, а минимум 10 января — {weather[9, 1]}: строка 9, столбец 1"


def test_rain():
    "day10_rain — осадки 10 января"
    assert day10_rain == weather[9, 3], f"day10_rain = {day10_rain}, а осадки 10 января — {weather[9, 3]}: строка 9, столбец 3"
# ─── другое решение ───
day = weather[9]
day10_min = day[1]
day10_rain = day[3]
# ─── ошибка ───
day10_min = weather[10, 1]
day10_rain = weather[10, 3]

# %% row-col
print(weather[1])          # строка: 2 января
col = weather[:, 2]        # столбец: максимумы за год
print(col.shape, col.max())

# %% columns [exercise]
tmin = weather[:, 1]
tmax = weather[:, 2]
# ─── заготовка ───
tmin = ...
tmax = ...
# ─── проверка ───
def test_shape():
    "tmin и tmax — столбцы по 365 значений"
    for name, value in [("tmin", tmin), ("tmax", tmax)]:
        assert isinstance(value, np.ndarray), f"{name} — это {type(value).__name__}, а нужен столбец weather[:, номер]"
        assert value.shape != (4,), f"{name} — строка из 4 чисел, а нужен столбец: weather[:, номер]"
        assert value.shape == (365,), f"у {name} форма {value.shape}, а нужен столбец из 365 значений"


def test_values():
    "в tmin минимумы, в tmax максимумы"
    assert isinstance(tmin, np.ndarray) and isinstance(tmax, np.ndarray) and tmin.shape == tmax.shape == (365,), "сначала исправьте то, о чём говорит проверка выше"
    assert tmin.min() == -14.9, "tmin — не столбец минимумов: его номер 1"
    assert tmax.max() == 27.2, "tmax — не столбец максимумов: его номер 2"
# ─── другое решение ───
tmin = weather[0:365, 1]
tmax = weather[:, -2]
# ─── ошибка ───
tmin = weather[1]
tmax = weather[2]

# %% first-day [exercise]
day1 = weather[0]
# ─── заготовка ───
day1 = ...
# ─── проверка ───
def test_day1():
    "day1 — четыре показателя 1 января"
    assert isinstance(day1, np.ndarray), f"day1 — это {type(day1).__name__}, а нужна строка таблицы"
    assert day1.shape != (365,), "это столбец, а нужна строка: один индекс — weather[0]"
    assert day1.tolist() == [1.0, -9.9, -3.2, 0.0], f"day1 = {day1.tolist()}, а 1 января — [1, −9.9, −3.2, 0]"
# ─── другое решение ───
day1 = weather[0, :]
# ─── ошибка ───
day1 = weather[:, 0]
# ─── ошибка ───
day1 = weather[1]

# %% block
week = weather[0:7, 1:3]
print(week.shape)
week

# %% block-shape [quiz]
print(weather[:, 1:3].shape)

# %% spring [exercise]
march = weather[59:90, 1:3]
# ─── заготовка ───
march = ...
# ─── проверка ───
def test_shape():
    "march — 31 день × 2 столбца"
    assert isinstance(march, np.ndarray), f"march — это {type(march).__name__}, а нужен блок таблицы"
    assert march.shape != (30, 2), "в блоке 30 дней: конец среза не входит, возьмите строки 59:90"
    assert march.shape == (31, 2), f"форма march — {march.shape}, а нужно (31, 2): 31 день, два столбца температур"


def test_values():
    "это мартовские минимумы и максимумы"
    assert isinstance(march, np.ndarray) and march.shape == (31, 2), "сначала исправьте то, о чём говорит проверка выше"
    assert march.tolist()[0] == weather[59, 1:3].tolist(), "блок должен начинаться с 1 марта (строка 59) и столбца 1"
    assert march.tolist()[-1] == weather[89, 1:3].tolist(), "блок должен заканчиваться 31 марта (строка 89)"
# ─── другое решение ───
temps = weather[:, 1:3]
march = temps[59:90]
# ─── ошибка ───
march = weather[59:89, 1:3]
# ─── ошибка ───
march = weather[59:90, 1:2]
