# Урок np-genfromtxt. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% peek
with open("data/station_airport.csv") as f:
    lines = f.read().splitlines()
for line in lines[9:15]:
    print(line)

# %% loadtxt-fails [raises=ValueError]
import numpy as np

np.loadtxt("data/station_airport.csv", delimiter=",", skiprows=1)

# %% load
airport = np.genfromtxt("data/station_airport.csv", delimiter=",", skip_header=1)
print(airport.shape)
print(airport[8:14])
print(np.isnan(airport[:, 1]).sum(), "дней без температуры")

# %% center [exercise]
center = np.genfromtxt("data/station_center.csv", delimiter=",", skip_header=1)
gaps_by_col = np.isnan(center).sum(axis=0)
center_avg = np.nanmean(center[:, 1])
# ─── заготовка ───
center = ...
gaps_by_col = ...
center_avg = ...
# ─── проверка ───
def test_center():
    "center — таблица 28 × 4"
    assert isinstance(center, np.ndarray), f"center — это {type(center).__name__}, а нужен массив из np.genfromtxt"
    assert center.shape != (29, 4), "в center 29 строк: заголовок стал строкой nan — добавьте skip_header=1"
    assert center.shape == (28, 4), f"у center форма {center.shape}, а в файле 28 дней по 4 числа"


def test_gaps():
    "gaps_by_col — пропуски по столбцам"
    assert isinstance(gaps_by_col, np.ndarray) and gaps_by_col.shape == (4,), "gaps_by_col — четыре числа, по столбцу: сумма маски по axis=0"
    assert gaps_by_col.tolist() == [0, 1, 0, 0], f"gaps_by_col = {gaps_by_col.tolist()}, а пропуск один — в температуре: [0, 1, 0, 0]"


def test_avg():
    "center_avg — средняя температура без пропусков"
    assert not np.isnan(center_avg), "center_avg = nan: обычный mean не пропускает пропуски — нужен np.nanmean"
    assert abs(center_avg - (-2.862963)) < 1e-5, f"center_avg = {center_avg}, а средняя температура в центре ≈ −2.86 °C (столбец 1)"
# ─── другое решение ───
center = np.genfromtxt("data/station_center.csv", delimiter=",", skip_header=1)
missing = np.isnan(center)
gaps_by_col = missing.sum(axis=0)
center_avg = np.nanmean(center, axis=0)[1]
# ─── ошибка ───
center = np.genfromtxt("data/station_center.csv", delimiter=",")
gaps_by_col = np.isnan(center).sum(axis=0)
center_avg = np.nanmean(center[:, 1])
# ─── ошибка ───
center = np.genfromtxt("data/station_center.csv", delimiter=",", skip_header=1)
gaps_by_col = np.isnan(center).sum(axis=0)
center_avg = center[:, 1].mean()

# %% no-header
raw = np.genfromtxt("data/station_center.csv", delimiter=",")
print(raw.shape)
print(raw[:3])

# %% header-quiz [quiz]
print(np.genfromtxt("data/station_forest.csv", delimiter=",").shape)

# %% filling
filled_demo = np.genfromtxt("data/station_airport.csv", delimiter=",", skip_header=1, filling_values=0)
print(filled_demo[9:14])

# %% zero-trap [exercise]
zero_temp = np.genfromtxt("data/station_airport.csv", delimiter=",", skip_header=1, usecols=1, filling_values=0)
temp = np.genfromtxt("data/station_airport.csv", delimiter=",", skip_header=1, usecols=1)
zero_avg = zero_temp.mean()
true_avg = np.nanmean(temp)
# ─── заготовка ───
zero_temp = ...
temp = ...
zero_avg = ...
true_avg = ...
# ─── проверка ───
def test_arrays():
    "zero_temp и temp — температура аэропорта"
    for name, arr in (("zero_temp", zero_temp), ("temp", temp)):
        assert isinstance(arr, np.ndarray), f"{name} — это {type(arr).__name__}, а нужен массив из np.genfromtxt"
        assert arr.shape == (28,), f"у {name} форма {arr.shape}, а нужен один столбец температуры: usecols=1, skip_header=1"
    assert np.isnan(temp).sum() == 5, "в temp должно быть 5 пропусков: загрузите его без filling_values"
    assert not np.isnan(zero_temp).any(), "в zero_temp остались пропуски: добавьте filling_values=0"
    assert (zero_temp == 0).sum() == 5, "в zero_temp должно быть 5 нулей на месте пропусков"


def test_avgs():
    "zero_avg и true_avg — средние с нулями и без пропусков"
    assert abs(zero_avg - (-3.775)) < 1e-9, f"zero_avg = {zero_avg}, а средняя по zero_temp — −3.775"
    assert not np.isnan(true_avg), "true_avg = nan: нужен np.nanmean"
    assert abs(true_avg - (-4.595652)) < 1e-5, f"true_avg = {true_avg}, а средняя без пропусков ≈ −4.60"
# ─── другое решение ───
path = "data/station_airport.csv"
temp = np.genfromtxt(path, delimiter=",", skip_header=1, usecols=1)
zero_temp = np.genfromtxt(path, delimiter=",", skip_header=1, usecols=1, filling_values=0)
zero_avg = np.mean(zero_temp)
true_avg = np.mean(temp[~np.isnan(temp)])
# ─── ошибка ───
zero_temp = np.genfromtxt("data/station_airport.csv", delimiter=",", skip_header=1, usecols=1, filling_values=0)
temp = np.genfromtxt("data/station_airport.csv", delimiter=",", skip_header=1, usecols=1)
zero_avg = zero_temp.mean()
true_avg = zero_avg

# %% nan-to-num
row = np.array([2.0, np.nan, 5.0])
print(np.nan_to_num(row))
print(np.nan_to_num(row, nan=-1.0))
print(row)

# %% humidity [exercise]
forest = np.genfromtxt("data/station_forest.csv", delimiter=",", skip_header=1)
humidity = forest[:, 2]
hum_filled = np.nan_to_num(humidity, nan=np.nanmean(humidity))
# ─── заготовка ───
forest = ...
humidity = ...
hum_filled = ...
# ─── проверка ───
def test_humidity():
    "humidity — влажность в лесу за 28 дней"
    assert isinstance(humidity, np.ndarray) and humidity.shape == (28,), "humidity — столбец из 28 значений: forest[:, 2] (и skip_header=1 при загрузке)"
    assert np.isnan(humidity).sum() == 1, "в humidity должен быть один пропуск — это столбец влажности, номер 2"


def test_filled():
    "hum_filled — пропуск заменён средней"
    assert isinstance(hum_filled, np.ndarray) and hum_filled.shape == (28,), "hum_filled — те же 28 дней, без пропуска"
    assert not np.isnan(hum_filled).any(), "в hum_filled остался пропуск"
    assert hum_filled[13] != 0, "пропуск стал нулём: передайте nan=средняя, иначе nan_to_num подставит 0"
    assert abs(hum_filled[13] - 86.481481) < 1e-5, f"на месте пропуска {hum_filled[13]}, а средняя влажность по известным дням ≈ 86.48"
# ─── другое решение ───
forest = np.genfromtxt("data/station_forest.csv", delimiter=",", skip_header=1)
humidity = forest[:, 2].copy()
hum_filled = np.where(np.isnan(humidity), np.nanmean(humidity), humidity)
# ─── ошибка ───
forest = np.genfromtxt("data/station_forest.csv", delimiter=",", skip_header=1)
humidity = forest[:, 2]
hum_filled = np.nan_to_num(humidity)
