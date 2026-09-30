# Урок np-project-moscow. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% peek
import numpy as np

with open("data/moscow_2025.csv") as f:
    print(f.read()[:80])

# %% load [exercise]
tmin = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=1)
tmax = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=2)
precip = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=3)
# ─── заготовка ───
tmin = ...
tmax = ...
precip = ...
# ─── проверка ───
def test_shapes():
    "три массива по 365 значений"
    for name, value in [("tmin", tmin), ("tmax", tmax), ("precip", precip)]:
        assert isinstance(value, np.ndarray), f"{name} — это {type(value).__name__}, а нужен массив из np.loadtxt"
        assert value.shape == (365,), f"у {name} форма {value.shape}, а нужен один столбец из 365 значений — задайте usecols="


def test_columns():
    "в каждом массиве — свой столбец"
    assert isinstance(tmin, np.ndarray) and isinstance(tmax, np.ndarray) and isinstance(precip, np.ndarray), "сначала исправьте то, о чём говорит проверка выше"
    assert tmin.min() == -14.9, "tmin — не столбец temp_min: его номер 1"
    assert tmax.max() == 27.2, "tmax — не столбец temp_max: его номер 2"
    assert precip.min() == 0 and precip.max() == 24.4, "precip — не столбец precip_mm: его номер 3"
# ─── другое решение ───
path = "data/moscow_2025.csv"
tmin = np.loadtxt(path, delimiter=",", skiprows=1, usecols=1)
tmax = np.loadtxt(path, delimiter=",", skiprows=1, usecols=2)
precip = np.loadtxt(path, delimiter=",", skiprows=1, usecols=3)
# ─── ошибка ───
tmin = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=0)
tmax = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=1)
precip = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=2)

# %% warmest [exercise]
warm_day = tmax.argmax() + 1
warm_temp = tmax.max()
# ─── заготовка ───
warm_day = ...
warm_temp = ...
# ─── проверка ───
def test_day():
    "warm_day — номер самого тёплого дня (с 1)"
    assert warm_day != 196, "196 — это индекс; номер дня на единицу больше"
    assert warm_day == 197, f"warm_day = {warm_day}, а самый тёплый — 197-й день"


def test_temp():
    "warm_temp — его температура"
    assert warm_temp == 27.2, f"warm_temp = {warm_temp}, а самый тёплый день — 27.2 °C"
# ─── другое решение ───
i = np.argmax(tmax)
warm_day = i + 1
warm_temp = np.max(tmax)
# ─── ошибка ───
warm_day = tmax.argmax()
warm_temp = tmax.max()

# %% coldest [exercise]
cold_day = tmin.argmin() + 1
cold_temp = tmin.min()
# ─── заготовка ───
cold_day = ...
cold_temp = ...
# ─── проверка ───
def test_day():
    "cold_day — номер самой холодной ночи (с 1)"
    assert cold_day != 44, "44 — это индекс; номер дня на единицу больше"
    assert cold_day == 45, f"cold_day = {cold_day}, а самая холодная ночь — в 45-й день"


def test_temp():
    "cold_temp — её температура"
    assert cold_temp == -14.9, f"cold_temp = {cold_temp}, а самый холодный минимум — −14.9 °C"
# ─── другое решение ───
cold_temp = tmin.min()
cold_day = np.argmin(tmin) + 1
# ─── ошибка ───
cold_day = tmin.argmax() + 1
cold_temp = tmin.max()

# %% amplitude [exercise]
amp = (tmax - tmin).mean()
# ─── заготовка ───
amp = ...
# ─── проверка ───
def test_amp():
    "amp — средний суточный перепад"
    assert not isinstance(amp, np.ndarray), "amp — массив, а нужно одно число: среднее от tmax - tmin"
    assert abs(amp + 5.519726) > 1e-4, "перепад получился отрицательным: из максимума вычитайте минимум"
    assert abs(amp - 5.519726) < 1e-4, f"amp = {amp}, а средний перепад ≈ 5.52 °C"
# ─── другое решение ───
amp = tmax.mean() - tmin.mean()
# ─── ошибка ───
amp = (tmin - tmax).mean()

# %% fahrenheit [exercise]
tmax_f = (tmax * 9 / 5 + 32).astype(int)
# ─── заготовка ───
tmax_f = ...
# ─── проверка ───
def test_int():
    "tmax_f — массив целых чисел"
    assert isinstance(tmax_f, np.ndarray), f"tmax_f — это {type(tmax_f).__name__}, а нужен массив"
    assert tmax_f.dtype.kind == "i", f"тип tmax_f — {tmax_f.dtype}, а нужны целые: .astype(int) к результату формулы"
    assert tmax_f.shape == (365,), f"у tmax_f форма {tmax_f.shape}, а нужно 365 значений"


def test_values():
    "температуры переведены в °F"
    assert isinstance(tmax_f, np.ndarray) and tmax_f.shape == (365,), "сначала исправьте то, о чём говорит проверка выше"
    first = tmax_f.tolist()[:5]
    assert first != [26, 26, 26, 25, 25], "похоже, astype(int) применён к tmax до формулы: скобки вокруг формулы, потом astype"
    assert first == [26, 26, 25, 19, 19], f"первые значения — {first}, а −3.2 °C — это 26.2 °F, целая часть 26"
# ─── другое решение ───
tmax_f = np.array(tmax * 1.8 + 32, dtype=int)
# ─── ошибка ───
tmax_f = tmax.astype(int) * 9 / 5 + 32

# %% rain [exercise]
wet_day = precip.argmax() + 1
rain_avg = precip.mean()
# ─── заготовка ───
wet_day = ...
rain_avg = ...
# ─── проверка ───
def test_day():
    "wet_day — номер самого дождливого дня"
    assert wet_day != 222, "222 — это индекс; номер дня на единицу больше"
    assert wet_day == 223, f"wet_day = {wet_day}, а больше всего осадков выпало в 223-й день"


def test_avg():
    "rain_avg — осадки в среднем за день"
    assert abs(rain_avg - 1.948767) < 1e-5, f"rain_avg = {rain_avg}, а в среднем выпадало ≈ 1.95 мм в день"
# ─── другое решение ───
wet_day = np.argmax(precip) + 1
rain_avg = precip.sum() / 365
# ─── ошибка ───
wet_day = precip.argmax()
rain_avg = precip.mean()

# %% summary
print("самый тёплый день:", warm_day, "—", warm_temp, "°C")
print("самая холодная ночь:", cold_day, "—", cold_temp, "°C")
print("средний перепад за сутки:", round(amp, 1), "°C")
print("осадков за год:", round(precip.sum()), "мм, больше всего — в день", wet_day)
