# Урок pd-agg. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% list
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv")
orders["revenue"] = orders["price"] * orders["quantity"]
orders.groupby("city")["revenue"].agg(["sum", "mean", "count"])

# %% list-use
stats = orders.groupby("city")["revenue"].agg(["sum", "mean", "count"])
print(stats.loc["Казань", "sum"])
print(stats["mean"].round(1).tolist())

# %% prices [exercise]
price_stats = orders.groupby("category")["price"].agg(["min", "max", "mean"])
widest = (price_stats["max"] - price_stats["min"]).idxmax()
# ─── заготовка ───
price_stats = ...
widest = ...
# ─── проверка ───
def test_stats():
    "price_stats — наименьшая, наибольшая и средняя цена по категориям"
    assert isinstance(price_stats, pd.DataFrame), f"price_stats — это {type(price_stats).__name__}, а нужна таблица: .agg([\"min\", \"max\", \"mean\"])"
    assert list(price_stats.columns) == ["min", "max", "mean"], f"столбцы сейчас {list(price_stats.columns)}, а нужны min, max, mean — в этом порядке"
    assert len(price_stats) == 5 and "Чай" in price_stats.index, "в индексе должны быть пять категорий: groupby(\"category\")"
    assert price_stats.loc["Чай", "min"] == 260 and price_stats.loc["Чай", "max"] == 540, "числа не те: считать нужно по столбцу price"
    assert abs(price_stats.loc["Чай", "mean"] - 381.114370) < 1e-5, "среднее не то: столбец price, функция mean"


def test_widest():
    "widest — категория с наибольшим размахом цен"
    assert isinstance(widest, str), f"widest — это {type(widest).__name__}, а нужно название категории: idxmax() разности столбцов max и min"
    assert widest == "Аксессуары", f"widest = {widest!r}, а наибольшая разность между max и min — у другой категории"
# ─── другое решение ───
groups = orders.groupby("category")["price"]
price_stats = pd.DataFrame({"min": groups.min(), "max": groups.max(), "mean": groups.mean()})
widest = (groups.max() - groups.min()).sort_values().index[-1]
# ─── ошибка ───
price_stats = orders.groupby("category")["revenue"].agg(["min", "max", "mean"])
widest = (price_stats["max"] - price_stats["min"]).idxmax()
# ─── ошибка ───
price_stats = orders.groupby("category")["price"].agg(["min", "max", "mean"])
widest = price_stats["max"].max()

# %% named
orders.groupby("city").agg(
    total=("revenue", "sum"),
    orders=("order_id", "nunique"),
    avg_price=("price", "mean"),
)

# %% named-calc
cities = orders.groupby("city").agg(total=("revenue", "sum"), orders=("order_id", "nunique"))
cities["check"] = (cities["total"] / cities["orders"]).round(1)
cities.sort_values("check", ascending=False)

# %% shape-quiz [quiz]
print(orders.groupby("channel")["revenue"].agg(["sum", "mean"]).shape)

# %% channels [exercise]
channels = orders.groupby("channel").agg(
    total=("revenue", "sum"),
    orders=("order_id", "nunique"),
    buyers=("customer_id", "nunique"),
)
channels["per_buyer"] = (channels["total"] / channels["buyers"]).round()
# ─── заготовка ───
channels = ...
# добавьте в channels столбец per_buyer
# ─── проверка ───
def test_channels():
    "channels — выручка, заказы и покупатели по каналам"
    assert isinstance(channels, pd.DataFrame), f"channels — это {type(channels).__name__}, а нужна таблица: orders.groupby(\"channel\").agg(...)"
    assert list(channels.columns)[:3] == ["total", "orders", "buyers"], f"столбцы сейчас {list(channels.columns)}, а первые три должны быть total, orders, buyers"
    assert sorted(channels.index) == ["маркетплейс", "приложение", "сайт"], "в индексе должны быть три канала: groupby(\"channel\")"
    assert channels.loc["сайт", "total"] == 1522920, "total — сумма revenue: total=(\"revenue\", \"sum\")"
    assert channels.loc["сайт", "orders"] != 1137, "orders — число разных заказов, а не строк: orders=(\"order_id\", \"nunique\")"
    assert channels.loc["сайт", "orders"] == 715, "orders — число разных заказов: orders=(\"order_id\", \"nunique\")"
    assert channels.loc["сайт", "buyers"] == 193, "buyers — число разных покупателей: buyers=(\"customer_id\", \"nunique\")"


def test_per_buyer():
    "per_buyer — выручка на одного покупателя, до рублей"
    assert "per_buyer" in channels.columns, "в channels нет столбца per_buyer"
    assert abs(channels.loc["сайт", "per_buyer"] - 7890.777) > 1e-2, "значения не округлены: добавьте .round()"
    assert channels.loc["сайт", "per_buyer"] == 7891 and channels.loc["маркетплейс", "per_buyer"] == 5764, "per_buyer — total, делённый на buyers, с округлением до рублей"
# ─── другое решение ───
groups = orders.groupby("channel")
channels = pd.DataFrame({
    "total": groups["revenue"].sum(),
    "orders": groups["order_id"].nunique(),
    "buyers": groups["customer_id"].nunique(),
})
channels["per_buyer"] = round(channels["total"] / channels["buyers"])
# ─── ошибка ───
channels = orders.groupby("channel").agg(
    total=("revenue", "sum"),
    orders=("order_id", "count"),
    buyers=("customer_id", "nunique"),
)
channels["per_buyer"] = (channels["total"] / channels["buyers"]).round()
# ─── ошибка ───
channels = orders.groupby("channel").agg(
    total=("revenue", "sum"),
    orders=("order_id", "nunique"),
    buyers=("customer_id", "nunique"),
)
channels["per_buyer"] = channels["total"] / channels["buyers"]

# %% two-keys
by_pair = orders.groupby(["city", "channel"])["revenue"].sum()
by_pair.head(7)

# %% two-keys-loc
print(by_pair.loc[("Казань", "сайт")])
print(by_pair.loc["Казань"])

# %% two-keys-len
print(len(by_pair))
print(by_pair.sum())
print(list(by_pair.index.names))

# %% pairs [exercise]
city_category = orders.groupby(["city", "category"])["revenue"].sum()
moscow = city_category.loc["Москва"]
moscow_tea = city_category.loc[("Москва", "Чай")]
# ─── заготовка ───
city_category = ...
moscow = ...
moscow_tea = ...
# ─── проверка ───
def test_pairs():
    "city_category — выручка по парам «город, категория»"
    assert isinstance(city_category, pd.Series), f"city_category — это {type(city_category).__name__}, а нужен Series: orders.groupby([\"city\", \"category\"])[\"revenue\"].sum()"
    assert len(city_category) != 5, "группировка только по одному столбцу: в groupby нужен список из двух — [\"city\", \"category\"]"
    assert len(city_category) == 25, f"в city_category {len(city_category)} значений, а пар «город, категория» 25"
    assert list(city_category.index.names) == ["city", "category"], f"уровни индекса сейчас {list(city_category.index.names)}, а нужны city, затем category — в таком порядке"
    assert city_category.sum() == 3301420, "суммы не те: складывать нужно столбец revenue"


def test_moscow():
    "moscow — категории в Москве, moscow_tea — чай в Москве"
    assert isinstance(moscow, pd.Series) and len(moscow) == 5, "moscow — Series из пяти категорий: city_category.loc[\"Москва\"]"
    assert "Кофе" in moscow.index and moscow["Кофе"] == 774640, "в moscow должны быть суммы по категориям для Москвы: city_category.loc[\"Москва\"]"
    assert not isinstance(moscow_tea, pd.Series), "moscow_tea — Series, а нужно одно число: city_category.loc[(\"Москва\", \"Чай\")] — пара в круглых скобках"
    assert moscow_tea == 230690, f"moscow_tea = {moscow_tea!r}, а выручка от чая в Москве — 230690"
# ─── другое решение ───
city_category = orders.groupby(["city", "category"])["revenue"].sum()
moscow = orders[orders["city"] == "Москва"].groupby("category")["revenue"].sum()
moscow_tea = moscow["Чай"]
# ─── ошибка ───
city_category = orders.groupby("city")["revenue"].sum()
moscow = orders[orders["city"] == "Москва"].groupby("category")["revenue"].sum()
moscow_tea = moscow["Чай"]
# ─── ошибка ───
city_category = orders.groupby(["category", "city"])["revenue"].sum()
moscow = city_category.loc["Чай"]
moscow_tea = city_category.loc[("Чай", "Москва")]

# %% two-keys-named
orders.groupby(["category", "channel"]).agg(total=("revenue", "sum"), lines=("revenue", "size")).head(6)

# %% climate [exercise]
weather = pd.read_csv("data/weather.csv")
climate = weather.groupby("city").agg(
    t_mean=("temp_max", "mean"),
    t_std=("temp_max", "std"),
    rain=("precip_mm", "sum"),
)
climate = climate.round(1)
# ─── заготовка ───
weather = pd.read_csv("data/weather.csv")
climate = ...
# ─── проверка ───
def test_climate():
    "climate — средний максимум, его разброс и осадки по городам"
    assert isinstance(climate, pd.DataFrame), f"climate — это {type(climate).__name__}, а нужна таблица: weather.groupby(\"city\").agg(...)"
    assert list(climate.columns) == ["t_mean", "t_std", "rain"], f"столбцы сейчас {list(climate.columns)}, а нужны t_mean, t_std, rain"
    assert len(climate) == 5 and "Сочи" in climate.index, "в индексе должны быть пять городов"
    assert abs(climate.loc["Сочи", "t_mean"] - 17.724932) > 1e-5, "значения не округлены: climate.round(1)"
    assert climate.loc["Сочи", "t_mean"] == 17.7, "t_mean — среднее temp_max: t_mean=(\"temp_max\", \"mean\")"
    assert climate.loc["Сочи", "t_std"] == 6.3, "t_std — стандартное отклонение temp_max: t_std=(\"temp_max\", \"std\")"
    assert climate.loc["Сочи", "rain"] == 795.0 and climate.loc["Новосибирск", "rain"] == 520.5, "rain — сумма precip_mm: rain=(\"precip_mm\", \"sum\")"
# ─── другое решение ───
weather = pd.read_csv("data/weather.csv")
groups = weather.groupby("city")
climate = pd.DataFrame({
    "t_mean": groups["temp_max"].mean(),
    "t_std": groups["temp_max"].std(),
    "rain": groups["precip_mm"].sum(),
}).round(1)
# ─── ошибка ───
weather = pd.read_csv("data/weather.csv")
climate = weather.groupby("city").agg(
    t_mean=("temp_max", "mean"),
    t_std=("temp_max", "std"),
    rain=("precip_mm", "sum"),
)
# ─── ошибка ───
weather = pd.read_csv("data/weather.csv")
climate = weather.groupby("city").agg(
    t_mean=("temp_max", "mean"),
    t_std=("temp_max", "std"),
    rain=("precip_mm", "mean"),
).round(1)
