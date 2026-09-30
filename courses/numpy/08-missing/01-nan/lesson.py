# Урок np-nan. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% what
import numpy as np

a = np.array([4, np.nan, 7])
print(a)
print(a.dtype)
print(a + 1)
print(a.sum(), a.mean())

# %% nan-eq
print(np.nan == np.nan)
print(a == np.nan)

# %% isnan
mask = np.isnan(a)
print(mask)
print(mask.sum())       # сколько пропусков
print(a[~mask])         # только известные
print(a[~mask].mean())

# %% gaps [exercise]
readings = np.array([-3.1, np.nan, -2.4, -4.0, np.nan, -1.8, -2.2])
gaps = np.isnan(readings).sum()
known = readings[~np.isnan(readings)]
week_avg = known.mean()
# ─── заготовка ───
readings = np.array([-3.1, np.nan, -2.4, -4.0, np.nan, -1.8, -2.2])
gaps = ...
known = ...
week_avg = ...
# ─── проверка ───
def test_gaps():
    "gaps — число пропусков"
    assert gaps != 0, "gaps = 0: сравнение с np.nan всегда False — ищите пропуски через np.isnan"
    assert gaps == 2, f"gaps = {gaps}, а пропусков в неделе два"


def test_known():
    "known — только известные значения"
    assert isinstance(known, np.ndarray), f"known — это {type(known).__name__}, а нужен массив: readings[маска]"
    assert not np.isnan(known).any(), "в known остались пропуски: отберите элементы, где np.isnan даёт False — маска ~np.isnan(readings)"
    assert known.tolist() == [-3.1, -2.4, -4.0, -1.8, -2.2], f"known = {known.tolist()}, а должны остаться пять известных дней по порядку"


def test_avg():
    "week_avg — средняя по известным дням"
    assert not np.isnan(week_avg), "week_avg = nan: среднее посчитано вместе с пропусками — берите known"
    assert abs(week_avg - (-2.7)) < 1e-9, f"week_avg = {week_avg}, а средняя по пяти известным дням — −2.7"
# ─── другое решение ───
readings = np.array([-3.1, np.nan, -2.4, -4.0, np.nan, -1.8, -2.2])
missing = np.isnan(readings)
gaps = missing.sum()
known = readings[~missing]
week_avg = np.nanmean(readings)
# ─── ошибка ───
readings = np.array([-3.1, np.nan, -2.4, -4.0, np.nan, -1.8, -2.2])
gaps = (readings == np.nan).sum()
known = readings[readings != np.nan]
week_avg = known.mean()
# ─── ошибка ───
readings = np.array([-3.1, np.nan, -2.4, -4.0, np.nan, -1.8, -2.2])
gaps = np.isnan(readings).sum()
known = readings[~np.isnan(readings)]
week_avg = readings.mean()

# %% eq-quiz [quiz]
print(np.nan == np.nan)

# %% nan-funcs
print(np.nanmean(a), np.nansum(a))
print(np.nanmax(a), np.nanmin(a))

# %% nan-axis
table = np.array([
    [1.0, np.nan, 3.0],
    [np.nan, 5.0, 7.0],
])
print(table.mean(axis=1))
print(np.nanmean(table, axis=1))

# %% stations [exercise]
week = np.array([
    [-2.1, -3.4, np.nan, -1.0, 0.5, 1.2, -0.3],
    [-3.5, np.nan, np.nan, -2.2, -0.8, 0.1, -1.9],
    [-4.0, -5.1, -4.4, -3.0, np.nan, -1.1, -2.6],
])
station_avg = np.nanmean(week, axis=1)
day_max = np.nanmax(week, axis=0)
# ─── заготовка ───
week = np.array([
    [-2.1, -3.4, np.nan, -1.0, 0.5, 1.2, -0.3],
    [-3.5, np.nan, np.nan, -2.2, -0.8, 0.1, -1.9],
    [-4.0, -5.1, -4.4, -3.0, np.nan, -1.1, -2.6],
])
station_avg = ...
day_max = ...
# ─── проверка ───
def test_avg():
    "station_avg — средняя каждой станции"
    assert isinstance(station_avg, np.ndarray), f"station_avg — это {type(station_avg).__name__}, а нужен массив из трёх средних"
    assert not np.isnan(station_avg).any(), "в station_avg есть nan: обычный mean не пропускает пропуски — нужен np.nanmean"
    assert station_avg.shape == (3,), f"у station_avg форма {station_avg.shape}, а станций 3: средняя по строкам — axis=1"
    assert np.allclose(station_avg, [-0.85, -1.66, -3.366667], atol=1e-6), f"station_avg = {station_avg}, а должно быть около [-0.85, -1.66, -3.37]"


def test_max():
    "day_max — самая высокая температура каждого дня"
    assert isinstance(day_max, np.ndarray) and day_max.shape == (7,), "day_max — семь чисел, по дню: максимум по столбцам — axis=0"
    assert not np.isnan(day_max).any(), "в day_max есть nan: нужен np.nanmax"
    assert day_max.tolist() == [-2.1, -3.4, -4.4, -1.0, 0.5, 1.2, -0.3], f"day_max = {day_max.tolist()}, а максимумы дней — [-2.1, -3.4, -4.4, -1.0, 0.5, 1.2, -0.3]"
# ─── другое решение ───
week = np.array([
    [-2.1, -3.4, np.nan, -1.0, 0.5, 1.2, -0.3],
    [-3.5, np.nan, np.nan, -2.2, -0.8, 0.1, -1.9],
    [-4.0, -5.1, -4.4, -3.0, np.nan, -1.1, -2.6],
])
station_avg = np.nansum(week, axis=1) / (~np.isnan(week)).sum(axis=1)
day_max = np.nanmax(week, axis=0)
# ─── ошибка ───
week = np.array([
    [-2.1, -3.4, np.nan, -1.0, 0.5, 1.2, -0.3],
    [-3.5, np.nan, np.nan, -2.2, -0.8, 0.1, -1.9],
    [-4.0, -5.1, -4.4, -3.0, np.nan, -1.1, -2.6],
])
station_avg = week.mean(axis=1)
day_max = week.max(axis=0)
# ─── ошибка ───
week = np.array([
    [-2.1, -3.4, np.nan, -1.0, 0.5, 1.2, -0.3],
    [-3.5, np.nan, np.nan, -2.2, -0.8, 0.1, -1.9],
    [-4.0, -5.1, -4.4, -3.0, np.nan, -1.1, -2.6],
])
station_avg = np.nanmean(week, axis=0)
day_max = np.nanmax(week, axis=1)

# %% fill [exercise]
filled = np.where(np.isnan(readings), np.nanmean(readings), readings)
# ─── заготовка ───
filled = ...
# ─── проверка ───
def test_filled():
    "filled — пропуски заменены средней"
    assert isinstance(filled, np.ndarray), f"filled — это {type(filled).__name__}, а нужен массив"
    assert len(filled) == 7, f"в filled {len(filled)} значений, а дней 7: пропуски заменяют, а не выбрасывают"
    assert not np.isnan(filled).any(), "в filled остались пропуски: условие — np.isnan(readings), а не сравнение с np.nan"
    assert np.allclose(filled, [-3.1, -2.7, -2.4, -4.0, -2.7, -1.8, -2.2]), f"filled = {filled}, а пропуски должны стать средней −2.7"


def test_readings():
    "readings не изменился"
    assert np.isnan(readings).sum() == 2, "readings изменился: np.where строит новый массив — исходный не трогайте"
# ─── другое решение ───
filled = readings.copy()
filled[np.isnan(filled)] = np.nanmean(readings)
# ─── ошибка ───
filled = np.where(readings == np.nan, np.nanmean(readings), readings)
# ─── ошибка ───
filled = np.where(np.isnan(readings), readings.mean(), readings)

# %% int-nan [raises=ValueError]
counts = np.array([3, 5, 2])
counts[1] = np.nan
