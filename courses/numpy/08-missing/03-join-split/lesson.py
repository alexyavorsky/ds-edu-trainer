# Урок np-join-split. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% concat
import numpy as np

a = np.array([1, 2, 3])
b = np.array([10, 20])
print(np.concatenate([a, b]))
print(np.concatenate([b, a, b]))

# %% months [exercise]
jan = np.array([410, 385, 402, 395, 430])
feb = np.array([398, 441, 420, 415])
all_sales = np.concatenate([jan, feb])
total = all_sales.sum()
# ─── заготовка ───
jan = np.array([410, 385, 402, 395, 430])
feb = np.array([398, 441, 420, 415])
all_sales = ...
total = ...
# ─── проверка ───
def test_all():
    "all_sales — январь, потом февраль"
    assert isinstance(all_sales, np.ndarray), f"all_sales — это {type(all_sales).__name__}, а нужен массив из np.concatenate"
    assert len(all_sales) == 9, f"в all_sales {len(all_sales)} чисел, а должно быть 5 + 4 = 9"
    assert all_sales[0] == 410, "all_sales начинается не с января: порядок в списке — [jan, feb]"
    assert all_sales.tolist() == [410, 385, 402, 395, 430, 398, 441, 420, 415], f"all_sales = {all_sales.tolist()}, а нужны все дни января, потом февраля"


def test_total():
    "total — выручка за все дни"
    assert total == 3696, f"total = {total}, а сумма всех девяти дней — 3696"
# ─── другое решение ───
jan = np.array([410, 385, 402, 395, 430])
feb = np.array([398, 441, 420, 415])
all_sales = np.hstack([jan, feb])
total = np.sum(all_sales)
# ─── ошибка ───
jan = np.array([410, 385, 402, 395, 430])
feb = np.array([398, 441, 420, 415])
all_sales = np.concatenate([feb, jan])
total = all_sales.sum()

# %% concat-2d
t1 = np.array([[1, 2], [3, 4]])
t2 = np.array([[5, 6], [7, 8]])
print(np.concatenate([t1, t2]))            # axis=0: строки добавились
print(np.concatenate([t1, t2], axis=1))    # axis=1: столбцы добавились

# %% stack
center = np.genfromtxt("data/station_center.csv", delimiter=",", skip_header=1)
airport = np.genfromtxt("data/station_airport.csv", delimiter=",", skip_header=1)
forest = np.genfromtxt("data/station_forest.csv", delimiter=",", skip_header=1)
temps_long = np.concatenate([center[:, 1], airport[:, 1], forest[:, 1]])
temps = np.stack([center[:, 1], airport[:, 1], forest[:, 1]])
print(temps_long.shape)
print(temps.shape)
print(temps[:, :4])     # три станции, первые четыре дня

# %% stack-quiz [quiz]
x = np.arange(5)
y = np.arange(5)
print(np.stack([x, y]).shape)

# %% humidity [exercise]
hum = np.stack([center[:, 2], airport[:, 2], forest[:, 2]])
hum_avg = np.nanmean(hum, axis=1)
# ─── заготовка ───
hum = ...
hum_avg = ...
# ─── проверка ───
def test_hum():
    "hum — влажность: 3 станции × 28 дней"
    assert isinstance(hum, np.ndarray), f"hum — это {type(hum).__name__}, а нужен массив из np.stack"
    assert hum.shape != (84,), "hum — один длинный ряд из 84 чисел: concatenate продолжает массив, а таблицу строит np.stack"
    assert hum.shape != (28, 3), "у hum форма (28, 3): станции должны быть строками — np.stack без axis=1"
    assert hum.shape == (3, 28), f"у hum форма {hum.shape}, а нужна (3, 28)"
    assert np.nanmax(hum) <= 100 and np.nanmin(hum) >= 40, "в hum не влажность: нужен столбец 2 каждой станции"
    assert np.isnan(hum[2]).sum() == 1, "станции не в том порядке: center, airport, forest"


def test_avg():
    "hum_avg — средняя влажность каждой станции"
    assert not np.isnan(hum_avg).any(), "в hum_avg есть nan: у леса пропуск — нужен np.nanmean"
    assert np.allclose(hum_avg, [74.821429, 81.5, 86.481481], atol=1e-5), f"hum_avg = {hum_avg}, а средние по станциям ≈ [74.8, 81.5, 86.5]"
# ─── другое решение ───
hum = np.vstack([center[:, 2], airport[:, 2], forest[:, 2]])
hum_avg = np.array([np.nanmean(hum[0]), np.nanmean(hum[1]), np.nanmean(hum[2])])
# ─── ошибка ───
hum = np.concatenate([center[:, 2], airport[:, 2], forest[:, 2]])
hum_avg = np.nanmean(hum)
# ─── ошибка ───
hum = np.stack([center[:, 2], airport[:, 2], forest[:, 2]])
hum_avg = hum.mean(axis=1)

# %% vh
x = np.array([1, 2, 3])
y = np.array([4, 5, 6])
print(np.vstack([x, y]))
print(np.hstack([x, y]))

# %% mismatch [raises=ValueError]
np.vstack([np.array([1, 2, 3]), np.array([4, 5])])

# %% add-col
scores = np.array([[70, 80], [65, 90], [88, 72]])
bonus = np.array([5, 0, 3])
print(np.hstack([scores, bonus[:, np.newaxis]]))

# %% add-column [exercise]
order = np.array([[120, 3], [80, 5], [200, 1], [45, 12]])
table = np.hstack([order, (order[:, 0] * order[:, 1])[:, np.newaxis]])
# ─── заготовка ───
order = np.array([[120, 3], [80, 5], [200, 1], [45, 12]])
table = ...
# ─── проверка ───
def test_table():
    "table — заказ с третьим столбцом суммы"
    assert isinstance(table, np.ndarray), f"table — это {type(table).__name__}, а нужен массив"
    assert table.shape != (5, 3) and table.shape != (3, 4), "суммы стали строкой: нужен столбец — np.hstack и [:, np.newaxis]"
    assert table.shape == (4, 3), f"у table форма {table.shape}, а нужна (4, 3): четыре строки, три столбца"
    assert table[:, :2].tolist() == order.tolist(), "первые два столбца table должны быть ценой и количеством из order"
    assert table[:, 2].tolist() == [360, 400, 200, 540], f"третий столбец — {table[:, 2].tolist()}, а суммы строк — [360, 400, 200, 540]"
# ─── другое решение ───
order = np.array([[120, 3], [80, 5], [200, 1], [45, 12]])
line_total = order[:, 0] * order[:, 1]
table = np.concatenate([order, line_total.reshape(-1, 1)], axis=1)
# ─── ошибка ───
order = np.array([[120, 3], [80, 5], [200, 1], [45, 12]])
table = np.hstack([order, (order[:, 0] + order[:, 1])[:, np.newaxis]])

# %% split
days = np.arange(1, 15)
first, second = np.split(days, 2)
print(first)
print(second)
print(np.split(days, [3, 10]))    # новые части начинаются с индексов 3 и 10

# %% uneven [raises=ValueError]
np.split(days, 3)

# %% weeks [exercise]
center_temp = center[:, 1]
weeks = np.stack(np.split(center_temp, 4))
week_avg = np.nanmean(weeks, axis=1)
# ─── заготовка ───
center_temp = center[:, 1]
weeks = ...
week_avg = ...
# ─── проверка ───
def test_weeks():
    "weeks — таблица 4 × 7"
    assert not isinstance(weeks, list), "weeks — список: np.split возвращает список частей, соберите их в таблицу np.stack"
    assert isinstance(weeks, np.ndarray), f"weeks — это {type(weeks).__name__}, а нужен массив"
    assert weeks.shape != (7, 4), "у weeks форма (7, 4): режьте на 4 части (недели), а не на 7"
    assert weeks.shape == (4, 7), f"у weeks форма {weeks.shape}, а нужна (4, 7): строка — неделя"
    assert weeks[1, 0] == -5.5, "в строках weeks не недели по порядку: разрежьте center_temp на 4 части"


def test_avg():
    "week_avg — средняя каждой недели"
    assert np.shape(week_avg) == (4,), f"у week_avg форма {np.shape(week_avg)}, а недель 4: средняя по строкам weeks — axis=1"
    assert not np.isnan(week_avg).any(), "в week_avg есть nan: в первой неделе пропуск — нужен np.nanmean"
    assert np.allclose(week_avg, [-4.966667, -4.885714, -1.657143, -0.242857], atol=1e-5), f"week_avg = {week_avg}, а средние недель ≈ [-4.97, -4.89, -1.66, -0.24]"
# ─── другое решение ───
center_temp = center[:, 1]
weeks = center_temp.reshape(4, 7)
week_avg = np.nanmean(weeks, axis=1)
# ─── ошибка ───
center_temp = center[:, 1]
weeks = np.stack(np.split(center_temp, 7))
week_avg = np.nanmean(weeks, axis=1)
