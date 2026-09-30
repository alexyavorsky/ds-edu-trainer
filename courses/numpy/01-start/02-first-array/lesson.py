# Урок np-first-array. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% list-loop
prices_list = [120, 80, 45, 300]
[p * 0.9 for p in prices_list]

# %% first
import numpy as np

prices = np.array([120, 80, 45, 300])
prices

# %% print
print(prices)
print(type(prices))

# %% temps [exercise]
temps = np.array([18, 21, 19, 25, 23, 17, 20])
# ─── заготовка ───
temps = ...
# ─── проверка ───
def test_array():
    "temps — массив NumPy"
    assert isinstance(temps, np.ndarray), f"temps — это {type(temps).__name__}, а нужен массив: передайте список в np.array(...)"


def test_values():
    "в temps семь температур по порядку"
    got = np.asarray(temps).tolist()
    assert got == [18, 21, 19, 25, 23, 17, 20], f"в temps сейчас {got}"
# ─── другое решение ───
week = [18, 21, 19, 25, 23, 17, 20]
temps = np.array(week)
# ─── ошибка ───
temps = [18, 21, 19, 25, 23, 17, 20]

# %% discount
prices * 0.9

# %% more-ops
print(prices + 50)   # доставка 50 ₽ к каждой позиции
print(prices / 2)    # половина цены
print(prices ** 2)   # квадрат каждого числа

# %% fahrenheit [exercise]
temps_f = temps * 9 / 5 + 32
# ─── заготовка ───
temps_f = ...
# ─── проверка ───
def test_array():
    "temps_f — массив той же длины, что temps"
    assert isinstance(temps_f, np.ndarray), f"temps_f — это {type(temps_f).__name__}, а нужен массив: посчитайте формулу прямо с массивом temps"
    assert len(temps_f) == 7, f"в temps_f {len(temps_f)} чисел, а температур 7"


def test_values():
    "значения переведены по формуле F = C × 9 / 5 + 32"
    got = np.asarray(temps_f, dtype=float)
    assert not np.allclose(got, [90.0, 95.4, 91.8, 102.6, 99.0, 88.2, 93.6]), "похоже, 32 прибавлено до умножения: сначала temps * 9 / 5, потом + 32"
    assert np.allclose(got, [64.4, 69.8, 66.2, 77.0, 73.4, 62.6, 68.0]), f"получилось {np.round(got, 1).tolist()}, а 18 °C — это 64.4 °F"
# ─── другое решение ───
temps_f = 32 + temps * 1.8
# ─── ошибка ───
temps_f = (temps + 32) * 9 / 5

# %% list-times
print(prices_list * 2)
print(prices * 2)

# %% list-float [raises=TypeError]
prices_list * 0.9

# %% list-plus [quiz]
[1, 2, 3] + [10, 20, 30]

# %% new-prices [exercise]
new_prices = prices * 1.1 + 20
# ─── заготовка ───
new_prices = ...
# ─── проверка ───
def test_array():
    "new_prices — массив из четырёх цен"
    assert isinstance(new_prices, np.ndarray), f"new_prices — это {type(new_prices).__name__}, а нужен массив: считайте от массива prices"
    assert len(new_prices) == 4, f"в new_prices {len(new_prices)} чисел, а цен 4"


def test_values():
    "цены подняты на 10 %, к каждой прибавлено 20 ₽"
    got = np.asarray(new_prices, dtype=float)
    assert not np.allclose(got, [154, 110, 71.5, 352]), "похоже, 20 ₽ прибавлены до повышения: сначала умножьте на 1.1, потом прибавьте 20"
    assert not np.allclose(got, [32, 28, 24.5, 50]), "умножение на 0.1 даёт 10 % от цены, а нужна цена плюс 10 % — умножьте на 1.1"
    assert np.allclose(got, [152, 108, 69.5, 350]), f"получилось {np.round(got, 2).tolist()}, а позиция за 120 ₽ должна стоить 152 ₽"


def test_prices_kept():
    "prices не изменился"
    assert np.asarray(prices).tolist() == [120, 80, 45, 300], (
        "массив prices изменился — новые цены нужно сохранить в new_prices. Чтобы вернуть prices, выполните ячейку "
        "«Массив из списка» ещё раз или нажмите «Перезапустить»"
    )
# ─── другое решение ───
new_prices = 1.1 * prices + 20
# ─── ошибка ───
new_prices = (prices + 20) * 1.1
# ─── ошибка ───
new_prices = prices * 0.1 + 20

# %% division [quiz]
np.array([10, 20]) / 4

# %% minutes [exercise]
seconds = np.array([185, 240, 210, 330, 150])
minutes = seconds / 60
# ─── заготовка ───
seconds = ...
minutes = ...
# ─── проверка ───
def test_seconds():
    "seconds — массив из пяти длительностей"
    assert isinstance(seconds, np.ndarray), f"seconds — это {type(seconds).__name__}, а нужен массив: np.array([...])"
    got = np.asarray(seconds).tolist()
    assert got == [185, 240, 210, 330, 150], f"в seconds сейчас {got}"


def test_minutes():
    "minutes — те же длительности в минутах"
    assert isinstance(minutes, np.ndarray), f"minutes — это {type(minutes).__name__}, а нужен массив: разделите массив seconds на 60"
    got = np.asarray(minutes, dtype=float)
    assert not np.allclose(got, [11100, 14400, 12600, 19800, 9000]), "вы умножили на 60, а секунды в минуты переводят делением"
    assert np.allclose(got, [185 / 60, 4, 3.5, 5.5, 2.5]), f"получилось {np.round(got, 2).tolist()}, а 240 секунд — это 4 минуты"
# ─── другое решение ───
seconds = np.array([185, 240, 210, 330, 150])
minutes = seconds / 60.0
# ─── ошибка ───
seconds = np.array([185, 240, 210, 330, 150])
minutes = seconds * 60
