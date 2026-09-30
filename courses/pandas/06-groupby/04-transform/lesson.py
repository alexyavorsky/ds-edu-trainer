# Урок pd-transform. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% toy-agg
import pandas as pd

scores = pd.DataFrame({
    "team": ["A", "A", "B", "B", "B"],
    "score": [10, 30, 5, 5, 20],
})
scores.groupby("team")["score"].mean()

# %% toy-transform
scores.groupby("team")["score"].transform("mean")

# %% toy-column
scores["team_mean"] = scores.groupby("team")["score"].transform("mean")
scores["diff"] = scores["score"] - scores["team_mean"]
scores

# %% len-quiz [quiz]
print(len(scores.groupby("team")["score"].transform("sum")))

# %% share [exercise]
orders = pd.read_csv("data/shop_orders.csv")
orders["revenue"] = orders["price"] * orders["quantity"]
orders["city_total"] = orders.groupby("city")["revenue"].transform("sum")
orders["city_share"] = orders["revenue"] / orders["city_total"]
# ─── заготовка ───
orders = pd.read_csv("data/shop_orders.csv")
orders["revenue"] = orders["price"] * orders["quantity"]
# добавьте в orders столбцы city_total и city_share
# ─── проверка ───
def test_total():
    "city_total — выручка города в каждой строке"
    assert "city_total" in orders.columns, "в orders нет столбца city_total: orders.groupby(\"city\")[\"revenue\"].transform(\"sum\")"
    assert orders["city_total"].notna().all(), "в city_total пропуски: похоже, в столбец записан результат .sum() — в нём пять значений с городами в индексе. Нужен .transform(\"sum\")"
    assert orders["city_total"].nunique() == 5, "в city_total должно быть пять разных значений — по одному на город"
    assert orders.loc[0, "city_total"] == 1310110 and orders.loc[4, "city_total"] == 440150, "значения не те: сумма revenue по городу строки"


def test_share():
    "city_share — доля строки в выручке своего города"
    assert "city_share" in orders.columns, "в orders нет столбца city_share"
    assert abs(orders.loc[0, "city_share"] - 6400 / 3301420) > 1e-9, "это доля в выручке всего магазина, а нужна доля в выручке своего города: revenue / city_total"
    assert abs(orders.loc[0, "city_share"] - 6400 / 1310110) < 1e-12, f"city_share в первой строке — {orders.loc[0, 'city_share']}, а должно быть ≈ 0.0049"
    assert abs(orders["city_share"].sum() - 5) < 1e-9, "доли внутри каждого города должны в сумме давать 1"
# ─── другое решение ───
orders = pd.read_csv("data/shop_orders.csv")
orders["revenue"] = orders["price"] * orders["quantity"]
orders["city_total"] = orders["city"].map(orders.groupby("city")["revenue"].sum())
orders["city_share"] = orders["revenue"] / orders["city_total"]
# ─── ошибка ───
orders = pd.read_csv("data/shop_orders.csv")
orders["revenue"] = orders["price"] * orders["quantity"]
orders["city_total"] = orders.groupby("city")["revenue"].sum()
orders["city_share"] = orders["revenue"] / orders["city_total"]
# ─── ошибка ───
orders = pd.read_csv("data/shop_orders.csv")
orders["revenue"] = orders["price"] * orders["quantity"]
orders["city_total"] = orders.groupby("city")["revenue"].transform("sum")
orders["city_share"] = orders["revenue"] / orders["revenue"].sum()

# %% shares-sum
orders.groupby("city")["city_share"].sum()

# %% order-total
orders["order_total"] = orders.groupby("order_id")["revenue"].transform("sum")
orders[["order_id", "product", "revenue", "order_total"]].head(4)

# %% order-filter
big = orders[orders["order_total"] >= 10000]
print(len(big), big["order_id"].nunique())

# %% lines [exercise]
orders["lines"] = orders.groupby("order_id")["product"].transform("count")
multi = orders[orders["lines"] >= 3]
n_multi = multi["order_id"].nunique()
# ─── заготовка ───
# добавьте в orders столбец lines
multi = ...
n_multi = ...
# ─── проверка ───
def test_lines():
    "lines — сколько позиций в заказе этой строки"
    assert "lines" in orders.columns, "в orders нет столбца lines: orders.groupby(\"order_id\")[\"product\"].transform(\"count\")"
    assert orders["lines"].notna().all(), "в lines пропуски: нужен transform(\"count\"), а не count() — он возвращает по одному значению на заказ"
    assert orders["lines"].tolist()[:7] == [2, 2, 2, 2, 2, 2, 1], f"первые значения lines — {orders['lines'].tolist()[:7]}, а должны быть [2, 2, 2, 2, 2, 2, 1]: в первых трёх заказах по две позиции"
    assert orders["lines"].max() == 3 and (orders["lines"] == 1).sum() == 832, "значения не те: число строк в группе по order_id"


def test_multi():
    "multi — строки заказов из трёх и более позиций, n_multi — число таких заказов"
    assert isinstance(multi, pd.DataFrame), f"multi — это {type(multi).__name__}, а нужна таблица: orders[маска]"
    assert len(multi) == 384, f"в multi {len(multi)} строк, а строк в заказах из трёх позиций — 384"
    assert n_multi != 384, "384 — число строк, а заказов меньше: разные order_id считает nunique()"
    assert n_multi == 128, f"n_multi = {n_multi!r}, а заказов из трёх и более позиций — 128"
# ─── другое решение ───
orders["lines"] = orders.groupby("order_id")["order_id"].transform("size")
multi = orders.query("lines >= 3")
n_multi = len(multi["order_id"].unique())
# ─── ошибка ───
orders["lines"] = orders.groupby("order_id")["product"].transform("count")
multi = orders[orders["lines"] >= 3]
n_multi = len(multi)
# ─── ошибка ───
orders["lines"] = orders.groupby("order_id")["product"].transform("count")
multi = orders[orders["lines"] > 3]
n_multi = multi["order_id"].nunique()

# %% norm
weather = pd.read_csv("data/weather.csv", parse_dates=["date"])
weather["month"] = weather["date"].dt.month
weather["norm"] = weather.groupby(["city", "month"])["temp_max"].transform("mean")
weather[["date", "city", "temp_max", "norm"]].head(3)

# %% anomaly [exercise]
weather["anomaly"] = weather["temp_max"] - weather["norm"]
warmest = weather.loc[weather["anomaly"].idxmax()]
n_unusual = (weather["anomaly"].abs() > 8).sum()
# ─── заготовка ───
# добавьте в weather столбец anomaly
warmest = ...
n_unusual = ...
# ─── проверка ───
def test_anomaly():
    "anomaly — отклонение дневного максимума от нормы месяца"
    assert "anomaly" in weather.columns, "в weather нет столбца anomaly: temp_max минус norm"
    assert abs(weather.loc[0, "anomaly"] - (-0.629032)) > 1e-5, "знак перепутан: из температуры дня вычитают норму"
    assert abs(weather.loc[0, "anomaly"] - 0.629032) < 1e-5, f"anomaly в первой строке — {weather.loc[0, 'anomaly']}, а должно быть ≈ 0.63"
    assert weather["anomaly"].isna().sum() == 2, "пропусков в anomaly должно быть два — там, где неизвестен temp_max"


def test_warmest():
    "warmest — день с наибольшим отклонением вверх, n_unusual — число необычных дней"
    assert isinstance(warmest, pd.Series) and "city" in warmest.index, "warmest — строка таблицы weather: weather.loc[weather[\"anomaly\"].idxmax()]"
    assert warmest["city"] == "Сочи" and warmest["date"] == pd.to_datetime("2025-03-29"), "это не день с наибольшим отклонением: метка — weather[\"anomaly\"].idxmax()"
    assert n_unusual != 12, "посчитаны только тёплые отклонения: нужны отклонения в обе стороны — модуль, .abs()"
    assert n_unusual == 20, f"n_unusual = {n_unusual!r}, а дней с отклонением больше 8 градусов в любую сторону — 20"
# ─── другое решение ───
weather = weather.assign(anomaly=weather["temp_max"] - weather["norm"])
warmest = weather.sort_values("anomaly", ascending=False).iloc[0]
n_unusual = ((weather["anomaly"] > 8) | (weather["anomaly"] < -8)).sum()
# ─── ошибка ───
weather["anomaly"] = weather["norm"] - weather["temp_max"]
warmest = weather.loc[weather["anomaly"].idxmax()]
n_unusual = (weather["anomaly"].abs() > 8).sum()
# ─── ошибка ───
weather["anomaly"] = weather["temp_max"] - weather["norm"]
warmest = weather.loc[weather["anomaly"].idxmax()]
n_unusual = (weather["anomaly"] > 8).sum()

# %% best-in-group
orders["cat_max"] = orders.groupby("category")["revenue"].transform("max")
orders.loc[orders["revenue"] == orders["cat_max"], ["category", "product", "quantity", "revenue"]]

# %% pricey [exercise]
orders["cat_price"] = orders.groupby("category")["price"].transform("mean")
orders["above_avg"] = orders["price"] > orders["cat_price"]
above_share = orders.groupby("category")["above_avg"].mean()
# ─── заготовка ───
# добавьте в orders столбцы cat_price и above_avg
above_share = ...
# ─── проверка ───
def test_columns():
    "cat_price — средняя цена категории, above_avg — цена строки выше неё"
    assert "cat_price" in orders.columns, "в orders нет столбца cat_price: orders.groupby(\"category\")[\"price\"].transform(\"mean\")"
    assert orders["cat_price"].notna().all() and orders["cat_price"].nunique() == 5, "в cat_price должно быть пять разных значений без пропусков: transform(\"mean\")"
    assert abs(orders.loc[0, "cat_price"] - 1165.277778) < 1e-5, "cat_price — средняя цена по строкам категории: в первой строке (аксессуары) ≈ 1165.28"
    assert "above_avg" in orders.columns and orders["above_avg"].dtype == bool, "above_avg — маска: orders[\"price\"] > orders[\"cat_price\"]"
    assert orders["above_avg"].sum() == 889, "маска не та: цена строки строго больше средней цены её категории"


def test_share():
    "above_share — доля строк дороже среднего в каждой категории"
    assert isinstance(above_share, pd.Series) and len(above_share) == 5, "above_share — Series по пяти категориям: orders.groupby(\"category\")[\"above_avg\"].mean()"
    assert above_share.max() <= 1, "в above_share числа строк, а нужны доли: среднее маски — mean()"
    assert abs(above_share["Кофе"] - (orders.loc[orders["category"] == "Кофе", "above_avg"].mean())) < 1e-12 and abs((above_share * orders.groupby("category").size()).sum() - 889) < 1e-6, "доли не те: среднее столбца above_avg по категориям"
# ─── другое решение ───
orders["cat_price"] = orders["category"].map(orders.groupby("category")["price"].mean())
orders["above_avg"] = orders["price"] > orders["cat_price"]
above_share = orders.groupby("category")["above_avg"].sum() / orders.groupby("category").size()
# ─── ошибка ───
orders["cat_price"] = orders.groupby("category")["price"].transform("mean")
orders["above_avg"] = orders["price"] > orders["cat_price"]
above_share = orders.groupby("category")["above_avg"].sum()
