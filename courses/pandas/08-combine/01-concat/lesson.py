# Урок pd-concat. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% two-files
import pandas as pd

h1 = pd.read_csv("data/delivery_h1.csv")
h2 = pd.read_csv("data/delivery_h2.csv")
print(h1.shape, h2.shape)
h2.head(3)

# %% concat
both = pd.concat([h1, h2])
print(both.shape)
both.tail(3)

# %% index-trap
both.loc[5]

# %% ignore
delivery = pd.concat([h1, h2], ignore_index=True)
delivery.tail(3)

# %% index-quiz [quiz]
a = pd.DataFrame({"x": [1, 2]})
b = pd.DataFrame({"x": [3, 4]})
print(pd.concat([a, b]).index.tolist())

# %% year [exercise]
year = pd.concat([h1, h2], ignore_index=True)
n_orders = len(year)
avg_rating = year["rating"].mean()
# ─── заготовка ───
year = ...
n_orders = ...
avg_rating = ...
# ─── проверка ───
def test_year():
    "year — доставка за весь год, индекс подряд"
    assert isinstance(year, pd.DataFrame), f"year — это {type(year).__name__}, а нужна таблица: pd.concat([h1, h2], ...)"
    assert len(year) == 1576, f"в year {len(year)} строк, а за год заказов 1576: обе таблицы в списке, в квадратных скобках"
    assert list(year.columns) == ["order_id", "days", "rating"], f"столбцы сейчас {list(year.columns)}, а должны остаться order_id, days, rating"
    assert year["order_id"].iloc[0] == 10001, "сначала должно идти первое полугодие: pd.concat([h1, h2], ...)"
    assert year.index.is_unique, "метки индекса повторяются: добавьте ignore_index=True"
    assert list(year.index[-2:]) == [1574, 1575], "индекс должен идти от 0 до 1575 подряд: ignore_index=True"


def test_numbers():
    "n_orders и avg_rating — число заказов и средняя оценка за год"
    assert n_orders == 1576, f"n_orders = {n_orders!r}, а заказов за год 1576"
    assert abs(avg_rating - 3.650390625) < 1e-9, f"avg_rating = {avg_rating!r}, а средняя оценка за год ≈ 3.65"
# ─── другое решение ───
year = pd.concat([h1, h2]).reset_index(drop=True)
n_orders = year.shape[0]
avg_rating = year["rating"].sum() / year["rating"].count()
# ─── ошибка ───
year = pd.concat([h1, h2])
n_orders = len(year)
avg_rating = year["rating"].mean()
# ─── ошибка ───
year = pd.concat([h2, h1], ignore_index=True)
n_orders = len(year)
avg_rating = year["rating"].mean()

# %% source
marked = pd.concat([h1.assign(half=1), h2.assign(half=2)], ignore_index=True)
print(both.index.is_unique, marked.index.is_unique)
marked.groupby("half")["rating"].mean()

# %% different
jan = pd.DataFrame({"city": ["Омск", "Тула"], "cups": [120, 95]})
feb = pd.DataFrame({"city": ["Омск", "Пермь"], "cups": [130, 60], "tips": [400, 150]})
pd.concat([jan, feb], ignore_index=True)

# %% halves [exercise]
by_half = marked.groupby("half").agg(orders=("order_id", "size"), days=("days", "mean"), no_rating=("rating", "count"))
by_half["no_rating"] = by_half["orders"] - by_half["no_rating"]
slower_half = by_half["days"].idxmax()
# ─── заготовка ───
by_half = ...
slower_half = ...
# ─── проверка ───
def test_by_half():
    "by_half — заказы, средний срок и число заказов без оценки по полугодиям"
    assert isinstance(by_half, pd.DataFrame), f"by_half — это {type(by_half).__name__}, а нужна таблица: marked.groupby(\"half\").agg(...)"
    assert list(by_half.index) == [1, 2], f"в индексе сейчас {list(by_half.index)}, а должны быть полугодия 1 и 2"
    assert list(by_half.columns) == ["orders", "days", "no_rating"], f"столбцы сейчас {list(by_half.columns)}, а нужны orders, days, no_rating"
    assert by_half["orders"].tolist() == [816, 760], "orders — число строк в полугодии: (\"order_id\", \"size\")"
    assert abs(by_half.loc[1, "days"] - 4.175641) < 1e-5 and abs(by_half.loc[2, "days"] - 4.419973) < 1e-5, "days — средний срок доставки: (\"days\", \"mean\")"
    assert by_half["no_rating"].tolist() != [529, 495], "в no_rating — число заказов С оценкой; без оценки — число строк минус число оценок"
    assert by_half["no_rating"].tolist() == [287, 265], "no_rating — сколько заказов без оценки: orders минус число непустых rating"


def test_slower():
    "slower_half — полугодие с более долгой доставкой"
    assert slower_half == 2, f"slower_half = {slower_half!r}, а дольше везли во втором полугодии: by_half[\"days\"].idxmax()"
# ─── другое решение ───
g = marked.groupby("half")
by_half = pd.DataFrame({"orders": g.size(), "days": g["days"].mean(), "no_rating": g.size() - g["rating"].count()})
slower_half = by_half.sort_values("days").index[-1]
# ─── ошибка ───
by_half = marked.groupby("half").agg(orders=("order_id", "size"), days=("days", "mean"), no_rating=("rating", "count"))
slower_half = by_half["days"].idxmax()

# %% loop
parts = []
for name in ["center", "airport", "forest"]:
    part = pd.read_csv("data/station_" + name + ".csv")
    part["station"] = name
    parts.append(part)
print(len(parts), parts[0].shape)

# %% stations [exercise]
stations = pd.concat(parts, ignore_index=True)
station_temp = stations.groupby("station")["temp"].mean().round(2)
# ─── заготовка ───
stations = ...
station_temp = ...
# ─── проверка ───
def test_stations():
    "stations — три станции одной таблицей"
    assert isinstance(stations, pd.DataFrame), f"stations — это {type(stations).__name__}, а нужна таблица: pd.concat(parts, ...)"
    assert stations.shape == (84, 5), f"у stations размер {stations.shape}, а нужно 84 строки (3 станции × 28 дней) и 5 столбцов"
    assert stations["station"].value_counts().to_dict() == {"center": 28, "airport": 28, "forest": 28}, "в stations должно быть по 28 строк каждой станции"
    assert stations.index.is_unique and list(stations.index[-1:]) == [83], "индекс должен идти от 0 до 83 подряд: ignore_index=True"


def test_temp():
    "station_temp — средняя температура по станциям, два знака"
    assert isinstance(station_temp, pd.Series) and len(station_temp) == 3, "station_temp — Series по трём станциям: stations.groupby(\"station\")[\"temp\"].mean()"
    assert station_temp["center"] == -2.86 and station_temp["forest"] == -6.08, "средние должны быть округлены до двух знаков: в центре −2.86, в лесу −6.08"
# ─── другое решение ───
stations = pd.concat([parts[0], parts[1], parts[2]]).reset_index(drop=True)
station_temp = stations.pivot_table(values="temp", index="station", aggfunc="mean")["temp"].round(2)
# ─── ошибка ───
stations = pd.concat(parts)
station_temp = stations.groupby("station")["temp"].mean().round(2)
# ─── ошибка ───
stations = parts[0]
station_temp = stations.groupby("station")["temp"].mean().round(2)

# %% side
left = pd.DataFrame({"city": ["Омск", "Тула"], "cups": [120, 95]})
right = pd.DataFrame({"manager": ["Анна", "Олег"]})
pd.concat([left, right], axis=1)

# %% side-trap
shuffled = right.sort_values("manager", ascending=False)
print(shuffled)
pd.concat([left, shuffled], axis=1)
