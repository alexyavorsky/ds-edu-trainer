# Урок np-indexing. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import numpy as np

tmax = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=2)
print(tmax.shape)

# %% one
print(tmax[0], tmax[-1])
print(tmax[364])

# %% out-of-range [raises=IndexError]
tmax[365]

# %% slices
print(tmax[:5])     # первые пять дней
print(tmax[-7:])    # последняя неделя
print(len(tmax[:31]))

# %% january [exercise]
jan = tmax[:31]
jan_avg = jan.mean()
# ─── заготовка ───
jan = ...
jan_avg = ...
# ─── проверка ───
def test_jan():
    "jan — 31 день января"
    assert isinstance(jan, np.ndarray), f"jan — это {type(jan).__name__}, а нужен срез массива tmax"
    assert len(jan) != 30, "в срезе 30 дней: конец среза не входит"
    assert len(jan) == 31, f"в jan {len(jan)} дней, а в январе 31"
    assert jan[0] == -3.2, "январь начинается с первого дня года — с индекса 0"


def test_avg():
    "jan_avg — средняя температура января"
    assert abs(jan_avg - (-3.829032)) < 1e-5, f"jan_avg = {jan_avg} — это не средняя температура января"
# ─── другое решение ───
jan = tmax[0:31]
jan_avg = np.mean(jan)
# ─── ошибка ───
jan = tmax[:30]
jan_avg = jan.mean()
# ─── ошибка ───
jan = tmax[1:32]
jan_avg = jan.mean()

# %% december [exercise]
last10 = tmax[-10:]
# ─── заготовка ───
last10 = ...
# ─── проверка ───
def test_last10():
    "last10 — последние десять дней"
    assert isinstance(last10, np.ndarray), f"last10 — это {type(last10).__name__}, а нужен срез массива tmax"
    assert len(last10) == 10, f"в last10 {len(last10)} значений, а нужно 10"
    assert last10.tolist() != tmax[:10].tolist(), "это первые десять дней года, а нужны последние: считайте с конца"
    assert last10[-1] == -2.0, "срез должен заканчиваться последним днём года"
# ─── другое решение ───
last10 = tmax[355:]
# ─── ошибка ───
last10 = tmax[:10]
# ─── ошибка ───
last10 = tmax[-10:-1]

# %% step
wednesdays = tmax[::7]
print(len(wednesdays))
print(wednesdays[:5])

# %% mondays [exercise]
mondays = tmax[5::7]
monday_avg = mondays.mean()
# ─── заготовка ───
mondays = ...
monday_avg = ...
# ─── проверка ───
def test_mondays():
    "mondays — 52 понедельника"
    assert isinstance(mondays, np.ndarray), f"mondays — это {type(mondays).__name__}, а нужен срез с шагом"
    assert len(mondays) == 52, f"в mondays {len(mondays)} значений, а понедельников в 2025 году 52"
    assert mondays[0] == -7.8, "первый понедельник — 6 января: с него и должен начинаться срез"


def test_avg():
    "monday_avg — средняя температура понедельников"
    assert abs(monday_avg - 9.426923) < 1e-5, f"monday_avg = {monday_avg} — это не средняя температура понедельников"
# ─── другое решение ───
mondays = tmax[5:365:7]
monday_avg = mondays.sum() / len(mondays)
# ─── ошибка ───
mondays = tmax[6::7]
monday_avg = mondays.mean()

# %% slice-step [quiz]
np.arange(10)[2:8:3]

# %% assign
hours = np.array([5.0, 7.5, 8.0, 99.0, 7.0])
hours[3] = 8.5       # одно значение
print(hours)
hours[:2] = 6.0      # сразу несколько
print(hours)

# %% sensor [exercise]
readings = np.array([20.1, 20.4, 20.9, 99.9, 21.8, 22.0, 21.7, 21.4])
readings[3] = 21.5
readings[-2:] = 0
# ─── заготовка ───
readings = np.array([20.1, 20.4, 20.9, 99.9, 21.8, 22.0, 21.7, 21.4])
# ─── проверка ───
def test_fixed():
    "четвёртое показание исправлено на 21.5"
    assert readings[3] != 99.9, "показание с ошибкой (индекс 3) всё ещё 99.9"
    assert readings[3] == 21.5, f"readings[3] = {readings[3]}, а должно быть 21.5 — индексы считают с нуля"


def test_off():
    "два последних часа — нули"
    got = readings.tolist()
    assert got[-2:] == [0, 0], f"последние два показания — {got[-2:]}, а должны быть нули"
    assert got[:3] == [20.1, 20.4, 20.9] and got[4:6] == [21.8, 22.0], f"остальные показания не должны меняться: {got}"
# ─── другое решение ───
readings = np.array([20.1, 20.4, 20.9, 99.9, 21.8, 22.0, 21.7, 21.4])
readings[3] = 21.5
readings[6] = 0
readings[7] = 0
# ─── ошибка ───
readings = np.array([20.1, 20.4, 20.9, 99.9, 21.8, 22.0, 21.7, 21.4])
readings[4] = 21.5
readings[-2:] = 0
# ─── ошибка ───
readings = np.array([20.1, 20.4, 20.9, 99.9, 21.8, 22.0, 21.7, 21.4])
readings[3] = 21.5
readings[-2] = 0
