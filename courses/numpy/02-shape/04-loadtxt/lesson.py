# Урок np-loadtxt. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% peek
with open("data/moscow_2025.csv") as f:
    print(f.read()[:120])

# %% load
import numpy as np

weather = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1)
print(weather.shape)
weather

# %% load-shape [quiz]
print(weather.size)

# %% no-skip [raises=ValueError]
np.loadtxt("data/moscow_2025.csv", delimiter=",")

# %% usecols
hot = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=2)
print(hot.shape)
print(hot.min(), hot.max())

# %% tmax [exercise]
tmax = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=2)
warm_avg = tmax.mean()
# ─── заготовка ───
tmax = ...
warm_avg = ...
# ─── проверка ───
def test_tmax():
    "tmax — 365 максимальных температур"
    assert isinstance(tmax, np.ndarray), f"tmax — это {type(tmax).__name__}, а нужен массив из np.loadtxt"
    assert tmax.ndim == 1, f"у tmax форма {tmax.shape}, а нужен один столбец: вспомните, как выбрать столбец при чтении"
    assert len(tmax) == 365, f"в tmax {len(tmax)} значений, а дней в году 365"
    assert tmax.max() == 27.2, "это не столбец temp_max — номера столбцов считают с нуля"


def test_avg():
    "warm_avg — средняя максимальная температура"
    assert abs(warm_avg - 9.123014) < 1e-5, f"warm_avg = {warm_avg} — это не средняя максимальная температура за год"
# ─── другое решение ───
path = "data/moscow_2025.csv"
tmax = np.loadtxt(path, delimiter=",", skiprows=1, usecols=2)
warm_avg = np.mean(tmax)
# ─── ошибка ───
tmax = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=1)
warm_avg = tmax.mean()

# %% rain [exercise]
precip = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=3)
rain_total = precip.sum()
# ─── заготовка ───
precip = ...
rain_total = ...
# ─── проверка ───
def test_precip():
    "precip — осадки за 365 дней"
    assert isinstance(precip, np.ndarray), f"precip — это {type(precip).__name__}, а нужен массив из np.loadtxt"
    assert precip.shape == (365,), f"у precip форма {precip.shape}, а нужен один столбец: вспомните, как выбрать столбец при чтении"
    assert precip.min() >= 0 and precip.max() == 24.4, "это не столбец precip_mm — номера столбцов считают с нуля"


def test_total():
    "rain_total — сумма осадков за год"
    assert abs(rain_total - 711.3) < 1e-6, f"rain_total = {rain_total} — это не сумма осадков за год"
# ─── другое решение ───
precip = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=3)
rain_total = np.sum(precip)
# ─── ошибка ───
precip = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=2)
rain_total = precip.sum()

# %% save
np.savetxt("data/fahrenheit.txt", hot * 9 / 5 + 32, fmt="%.1f")
with open("data/fahrenheit.txt") as f:
    print(f.read()[:30])

# %% save-tmin [exercise]
tmin = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=1)
np.savetxt("data/tmin.txt", tmin, fmt="%.1f")
# ─── заготовка ───
tmin = ...
# сохраните tmin в файл data/tmin.txt
# ─── проверка ───
def test_tmin():
    "tmin — столбец минимальных температур"
    assert isinstance(tmin, np.ndarray) and tmin.shape == (365,), "tmin — это должен быть один столбец из файла — вспомните, как выбрать столбец при чтении"
    assert tmin.min() == -14.9, "это не столбец temp_min — номера столбцов считают с нуля"


def test_file():
    "в data/tmin.txt 365 строк с одним знаком после точки"
    import os

    assert os.path.exists("data/tmin.txt"), "файла data/tmin.txt нет — сохраните массив через np.savetxt"
    with open("data/tmin.txt") as f:
        lines = f.read().split()
    assert len(lines) == 365, f"в файле {len(lines)} чисел, а нужно 365"
    assert lines[0] == "-9.9", f"первая строка файла — {lines[0]!r}, а нужно -9.9: задайте формат чисел с одним знаком после точки"
# ─── другое решение ───
tmin = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=1)
np.savetxt("data/tmin.txt", tmin, fmt="%.1f", delimiter=",")
# ─── ошибка ───
tmin = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=1)
np.savetxt("data/tmin.txt", tmin)
