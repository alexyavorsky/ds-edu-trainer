# Урок np-project-station. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load [exercise]
import numpy as np

center = np.genfromtxt("data/station_center.csv", delimiter=",", skip_header=1)
airport = np.genfromtxt("data/station_airport.csv", delimiter=",", skip_header=1)
forest = np.genfromtxt("data/station_forest.csv", delimiter=",", skip_header=1)
temps = np.stack([center[:, 1], airport[:, 1], forest[:, 1]])
gaps = np.isnan(temps).sum(axis=1)
# ─── заготовка ───
import numpy as np

temps = ...
gaps = ...
# ─── проверка ───
def test_temps():
    "temps — 3 станции × 28 дней"
    assert isinstance(temps, np.ndarray), f"temps — это {type(temps).__name__}, а нужен массив из np.stack"
    assert temps.shape != (84,), "temps — один ряд из 84 чисел: таблицу строит np.stack, а не concatenate"
    assert temps.shape != (28, 3), "у temps форма (28, 3): станции должны быть строками"
    assert temps.shape == (3, 28), f"у temps форма {temps.shape}, а нужна (3, 28)"
    assert np.nanmax(temps) < 5, "в temps не температура: нужен столбец температуры каждого файла"
    assert np.nanmean(temps[0]) > np.nanmean(temps[2]), "станции не в том порядке: center, airport, forest"


def test_gaps():
    "gaps — пропуски каждой станции"
    assert np.shape(gaps) == (3,), f"у gaps форма {np.shape(gaps)}, а станций три"
    assert gaps.tolist() == [1, 5, 0], f"gaps = {gaps.tolist()} — это не число пропусков каждой станции"
# ─── другое решение ───
import numpy as np

names = ["center", "airport", "forest"]
temps = np.vstack([
    np.genfromtxt("data/station_" + name + ".csv", delimiter=",", skip_header=1, usecols=1) for name in names
])
gaps = np.sum(np.isnan(temps), axis=1)
# ─── ошибка ───
import numpy as np

center = np.genfromtxt("data/station_center.csv", delimiter=",", skip_header=1)
airport = np.genfromtxt("data/station_airport.csv", delimiter=",", skip_header=1)
forest = np.genfromtxt("data/station_forest.csv", delimiter=",", skip_header=1)
temps = np.stack([center[:, 1], airport[:, 1], forest[:, 1]])
gaps = np.isnan(temps).sum(axis=0)

# %% fill [exercise]
day_mean = np.nanmean(temps, axis=0)
filled = np.where(np.isnan(temps), day_mean, temps)
# ─── заготовка ───
day_mean = ...
filled = ...
# ─── проверка ───
def test_day_mean():
    "day_mean — средняя каждого дня по станциям"
    assert isinstance(day_mean, np.ndarray), f"day_mean — это {type(day_mean).__name__}, а нужен массив из 28 средних"
    assert day_mean.shape != (3,), "в day_mean три числа — это средние станций; средняя дня — по столбцу"
    assert day_mean.shape == (28,), f"у day_mean форма {day_mean.shape}, а дней 28"
    assert not np.isnan(day_mean).any(), "в day_mean есть nan: нужен np.nanmean"
    assert abs(day_mean[10] - (-5.2)) < 1e-9, f"day_mean[10] = {day_mean[10]} — это не средняя 11-го дня по известным станциям"


def test_filled():
    "filled — пропуски заменены средней дня"
    assert isinstance(filled, np.ndarray) and filled.shape == (3, 28), "filled — таблица той же формы, что temps: (3, 28)"
    assert not np.isnan(filled).any(), "в filled остались пропуски"
    assert (filled[~np.isnan(temps)] == temps[~np.isnan(temps)]).all(), "в filled изменились известные значения: заменять можно только пропуски"
    assert abs(filled[1, 11] - (-5.45)) < 1e-9, f"пропуск аэропорта в 12-й день заполнен числом {filled[1, 11]}, а там должна быть средняя этого дня"
# ─── другое решение ───
day_mean = np.nanmean(temps, axis=0)
filled = np.nan_to_num(temps) + np.isnan(temps) * day_mean   # маска × средняя: где не пропуск — ноль
# ─── ошибка ───
day_mean = np.nanmean(temps, axis=0)
filled = np.nan_to_num(temps)
# ─── ошибка ───
day_mean = np.nanmean(temps, axis=0)
filled = np.where(np.isnan(temps), np.nanmean(temps, axis=1, keepdims=True), temps)

# %% check-fill
print(np.isnan(filled).sum(), "пропусков")
print(np.round(temps.mean(axis=1), 2))
print(np.round(filled.mean(axis=1), 2))

# %% cube-weeks
sample = np.arange(1, 29).reshape(2, 14)     # 2 ряда по 14 дней — две недели
sample_weeks = sample.reshape(2, 2, 7)       # ряд → неделя → день недели
print(sample_weeks.shape)
print(sample_weeks[0])       # первый ряд: 2 строки-недели по 7 дней

# %% weekly [exercise]
weekly = filled.reshape(3, 4, 7).mean(axis=2)
coldest_week = weekly.mean(axis=0).argmin() + 1
# ─── заготовка ───
weekly = ...
coldest_week = ...
# ─── проверка ───
def test_weekly():
    "weekly — средние: 3 станции × 4 недели"
    assert isinstance(weekly, np.ndarray), f"weekly — это {type(weekly).__name__}, а нужен массив"
    assert weekly.shape != (3, 7), "у weekly форма (3, 7) — это средние по дням недели; усредняйте внутри каждой недели"
    assert weekly.shape == (3, 4), f"у weekly форма {weekly.shape}, а нужна (3, 4)"
    assert np.allclose(weekly[0], [-5.478571, -4.885714, -1.657143, -0.242857], atol=1e-5), (
        f"недели центра — {np.round(weekly[0], 2)}: берите filled, недели — по 7 дней подряд"
    )
    assert np.allclose(weekly[1], [-6.714286, -6.421429, -3.078571, -1.764286], atol=1e-5), "средние аэропорта не те: считайте по filled"


def test_coldest():
    "coldest_week — номер самой холодной недели"
    assert coldest_week != 0, "0 — индекс, а недели нумеруются с 1"
    assert coldest_week == 1, f"coldest_week = {coldest_week} — это не номер самой холодной недели"
# ─── другое решение ───
weekly = np.stack(np.split(filled, 4, axis=1), axis=1).mean(axis=2)
coldest_week = np.argmin(weekly.mean(axis=0)) + 1
# ─── ошибка ───
weekly = filled.reshape(3, 4, 7).mean(axis=2)
coldest_week = weekly.mean(axis=0).argmin()

# %% island [exercise]
station_avg = filled.mean(axis=1)
island = (filled[0] - filled[2]).mean()
thaw_days = (filled.max(axis=0) > 0).sum()
# ─── заготовка ───
station_avg = ...
island = ...
thaw_days = ...
# ─── проверка ───
def test_avg():
    "station_avg — средняя каждой станции"
    assert np.shape(station_avg) == (3,), f"у station_avg форма {np.shape(station_avg)}, а станций 3: нужна средняя по строкам"
    assert np.allclose(station_avg, [-3.066071, -4.494643, -6.075], atol=1e-5), f"station_avg = {station_avg}: считайте по filled"


def test_island():
    "island — насколько центр теплее леса"
    assert island > 0, f"island = {island}: из центра вычитайте лес"
    assert abs(island - 3.008929) < 1e-5, f"island = {island} — это не средняя разница центра и леса"


def test_thaw():
    "thaw_days — дни выше нуля хотя бы на одной станции"
    assert thaw_days != 0, "thaw_days = 0 — это дни, когда выше нуля было на всех станциях; нужна хотя бы одна"
    assert thaw_days == 4, f"thaw_days = {thaw_days} — это не число дней выше нуля хотя бы на одной станции"
# ─── другое решение ───
station_avg = np.mean(filled, axis=1)
island = station_avg[0] - station_avg[2]
thaw_days = (filled > 0).any(axis=0).sum()
# ─── ошибка ───
station_avg = filled.mean(axis=1)
island = (filled[0] - filled[2]).mean()
thaw_days = (filled.min(axis=0) > 0).sum()

# %% report [exercise]
report = np.hstack([np.arange(1, 5)[:, np.newaxis], weekly.T])
np.savetxt("data/weekly.csv", report, delimiter=",", fmt="%.1f")
# ─── заготовка ───
report = ...
# ─── проверка ───
def test_report():
    "report — таблица 4 × 4"
    assert isinstance(report, np.ndarray), f"report — это {type(report).__name__}, а нужен массив"
    assert report.shape == (4, 4), f"у report форма {report.shape}, а нужна (4, 4): номер недели и три станции"
    assert report[:, 0].tolist() == [1, 2, 3, 4], "первый столбец report — номера недель 1–4"
    assert np.allclose(report[:, 1:], weekly.T), "столбцы 2–4 — средние станций по неделям"


def test_file():
    "файл data/weekly.csv записан"
    import os
    assert os.path.exists("data/weekly.csv"), "файла data/weekly.csv нет: сохраните report через np.savetxt"
    with open("data/weekly.csv") as f:
        first = f.read().split("\n")[0]
    assert first == "1.0,-5.5,-6.7,-8.2", f"первая строка файла — «{first}»: числа через запятую, у каждого один знак после точки"
# ─── другое решение ───
weeks = np.array([1, 2, 3, 4])
report = np.concatenate([weeks.reshape(-1, 1), weekly.T], axis=1)
np.savetxt("data/weekly.csv", report, fmt="%.1f", delimiter=",")
# ─── ошибка ───
report = np.hstack([np.arange(1, 5)[:, np.newaxis], weekly.T])
np.savetxt("data/weekly.csv", report, delimiter=",")

# %% summary
with open("data/weekly.csv") as f:
    print(f.read())
print("центр теплее леса на", round(island, 1), "°C")
