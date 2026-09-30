# Урок pd-project-channels. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv")
orders["revenue"] = orders["price"] * orders["quantity"]
orders.head(3)

# %% summary [exercise]
channels = orders.groupby("channel").agg(
    total=("revenue", "sum"),
    orders=("order_id", "nunique"),
    buyers=("customer_id", "nunique"),
)
# ─── заготовка ───
channels = ...
# ─── проверка ───
def test_channels():
    "channels — выручка, заказы и покупатели по каналам"
    assert isinstance(channels, pd.DataFrame), f"channels — это {type(channels).__name__}, а нужна таблица: orders.groupby(\"channel\").agg(...)"
    assert sorted(channels.index) == ["маркетплейс", "приложение", "сайт"], "в индексе должны быть три канала: groupby(\"channel\") без as_index=False"
    assert list(channels.columns)[:3] == ["total", "orders", "buyers"], f"столбцы сейчас {list(channels.columns)}, а нужны total, orders, buyers"
    assert channels.loc["сайт", "total"] == 1522920, "total — сумма revenue"
    assert channels.loc["сайт", "orders"] != 1137, "orders — число разных заказов, а не строк: (\"order_id\", \"nunique\")"
    assert channels.loc["сайт", "orders"] == 715 and channels.loc["сайт", "buyers"] == 193, "orders и buyers — число разных order_id и customer_id: функция nunique"
# ─── другое решение ───
g = orders.groupby("channel")
channels = pd.DataFrame({"total": g["revenue"].sum(), "orders": g["order_id"].nunique(), "buyers": g["customer_id"].nunique()})
# ─── ошибка ───
channels = orders.groupby("channel").agg(
    total=("revenue", "sum"),
    orders=("order_id", "count"),
    buyers=("customer_id", "count"),
)
# ─── ошибка ───
channels = orders.groupby("channel")["revenue"].sum()

# %% metrics [exercise]
channels["share"] = channels["total"] / channels["total"].sum()
channels["check"] = channels["total"] / channels["orders"]
channels["orders_per_buyer"] = channels["orders"] / channels["buyers"]
# ─── заготовка ───
# добавьте в channels столбцы share, check и orders_per_buyer
# ─── проверка ───
def test_share():
    "share — доля канала в выручке"
    assert "share" in channels.columns, "в channels нет столбца share"
    assert abs(channels["share"].sum() - 1) < 1e-9, "доли каналов должны в сумме давать 1: total, делённый на сумму столбца total"
    assert abs(channels.loc["сайт", "share"] - 1522920 / 3301420) < 1e-9, "доля сайта должна быть ≈ 0.461"


def test_check():
    "check — средний чек, orders_per_buyer — заказов на покупателя"
    assert "check" in channels.columns and "orders_per_buyer" in channels.columns, "в channels нужны столбцы check и orders_per_buyer"
    assert abs(channels.loc["сайт", "check"] - 1522920 / 715) < 1e-6, "check — total, делённый на orders"
    assert abs(channels.loc["сайт", "orders_per_buyer"] - 193 / 715) > 1e-9, "дробь перевёрнута: заказов на покупателя — orders / buyers"
    assert abs(channels.loc["сайт", "orders_per_buyer"] - 715 / 193) < 1e-9, "orders_per_buyer — orders, делённый на buyers"
# ─── другое решение ───
channels = channels.assign(
    share=channels["total"] / orders["revenue"].sum(),
    check=channels["total"] / channels["orders"],
    orders_per_buyer=channels["orders"] / channels["buyers"],
)
# ─── ошибка ───
channels["share"] = channels["total"]
channels["check"] = channels["total"] / channels["orders"]
channels["orders_per_buyer"] = channels["orders"] / channels["buyers"]
# ─── ошибка ───
channels["share"] = channels["total"] / channels["total"].sum()
channels["check"] = channels["total"] / channels["orders"]
channels["orders_per_buyer"] = channels["buyers"] / channels["orders"]

# %% metrics-view
channels.round(3)

# %% cities [exercise]
city_channel = orders.groupby(["city", "channel"], as_index=False)["revenue"].sum()
city_channel["share"] = city_channel["revenue"] / city_channel.groupby("city")["revenue"].transform("sum")
# ─── заготовка ───
city_channel = ...
# добавьте в city_channel столбец share
# ─── проверка ───
def test_table():
    "city_channel — выручка по парам «город, канал», плоская таблица"
    assert isinstance(city_channel, pd.DataFrame), f"city_channel — это {type(city_channel).__name__}, а нужна таблица: as_index=False"
    assert list(city_channel.columns)[:3] == ["city", "channel", "revenue"], f"столбцы сейчас {list(city_channel.columns)}, а первые три должны быть city, channel, revenue"
    assert len(city_channel) == 15 and city_channel["revenue"].sum() == 3301420, "в city_channel 15 строк — по одной на пару"


def test_share():
    "share — доля канала в выручке своего города"
    assert "share" in city_channel.columns, "в city_channel нет столбца share"
    assert city_channel["share"].notna().all(), "в share пропуски: сумму города нужно раздать по строкам — transform(\"sum\"), а не sum()"
    assert abs(city_channel["share"].sum() - 1) > 1e-6, "доли считаются от выручки всего магазина, а нужны от выручки своего города: делите на city_channel.groupby(\"city\")[\"revenue\"].transform(\"sum\")"
    assert abs(city_channel["share"].sum() - 5) < 1e-9, "доли внутри каждого города должны давать в сумме 1"
    kazan_site = city_channel[(city_channel["city"] == "Казань") & (city_channel["channel"] == "сайт")]["share"].iloc[0]
    assert abs(kazan_site - 219510 / 440150) < 1e-9, "доля сайта в Казани должна быть ≈ 0.499"
# ─── другое решение ───
city_channel = orders.groupby(["city", "channel"])["revenue"].sum().reset_index()
city_channel["share"] = city_channel["revenue"] / city_channel["city"].map(orders.groupby("city")["revenue"].sum())
# ─── ошибка ───
city_channel = orders.groupby(["city", "channel"], as_index=False)["revenue"].sum()
city_channel["share"] = city_channel["revenue"] / city_channel["revenue"].sum()
# ─── ошибка ───
city_channel = orders.groupby(["city", "channel"], as_index=False)["revenue"].sum()
city_channel["share"] = city_channel["revenue"] / city_channel.groupby("city")["revenue"].sum()

# %% strong [exercise]
app = city_channel[city_channel["channel"] == "приложение"].sort_values("share", ascending=False)
app_city = app.iloc[0]["city"]
market = city_channel[city_channel["channel"] == "маркетплейс"].sort_values("share", ascending=False)
market_city = market.iloc[0]["city"]
# ─── заготовка ───
app = ...
app_city = ...
market = ...
market_city = ...
# ─── проверка ───
def test_app():
    "app — строки приложения по убыванию доли, app_city — где приложение сильнее всего"
    assert isinstance(app, pd.DataFrame) and len(app) == 5 and (app["channel"] == "приложение").all(), "app — пять строк таблицы city_channel с каналом «приложение»"
    shares = app["share"].tolist()
    assert shares == sorted(shares, reverse=True), "отсортируйте app по убыванию share"
    assert isinstance(app_city, str), f"app_city — это {type(app_city).__name__}, а нужно название города: app.iloc[0][\"city\"]"
    assert app_city == "Екатеринбург", f"app_city = {app_city!r}, а доля приложения выше всего в другом городе"


def test_market():
    "market и market_city — то же для маркетплейса"
    assert isinstance(market, pd.DataFrame) and len(market) == 5 and (market["channel"] == "маркетплейс").all(), "market — пять строк таблицы city_channel с каналом «маркетплейс»"
    shares = market["share"].tolist()
    assert shares == sorted(shares, reverse=True), "отсортируйте market по убыванию share"
    assert market_city == "Санкт-Петербург", f"market_city = {market_city!r}, а доля маркетплейса выше всего в другом городе"
# ─── другое решение ───
app = city_channel.query("channel == 'приложение'").sort_values("share", ascending=False)
app_city = app["city"].iloc[0]
market = city_channel.query("channel == 'маркетплейс'").sort_values("share", ascending=False)
market_city = market.loc[market["share"].idxmax(), "city"]
# ─── ошибка ───
app = city_channel[city_channel["channel"] == "приложение"].sort_values("revenue", ascending=False)
app_city = app.iloc[0]["city"]
market = city_channel[city_channel["channel"] == "маркетплейс"].sort_values("revenue", ascending=False)
market_city = market.iloc[0]["city"]

# %% mix [exercise]
mix = orders.groupby(["channel", "category"], as_index=False)["revenue"].sum()
mix["share"] = (mix["revenue"] / mix.groupby("channel")["revenue"].transform("sum")).round(3)
dishes = mix[mix["category"] == "Посуда"]
# ─── заготовка ───
mix = ...
# добавьте в mix столбец share
dishes = ...
# ─── проверка ───
def test_mix():
    "mix — выручка по парам «канал, категория» и доля категории в канале"
    assert isinstance(mix, pd.DataFrame), f"mix — это {type(mix).__name__}, а нужна таблица"
    assert list(mix.columns)[:3] == ["channel", "category", "revenue"], f"столбцы сейчас {list(mix.columns)}, а первые три должны быть channel, category, revenue — группировка по [\"channel\", \"category\"]"
    assert len(mix) == 15, f"в mix {len(mix)} строк, а пар «канал, категория» 15"
    assert "share" in mix.columns and mix["share"].notna().all(), "в mix нужен столбец share без пропусков: revenue, делённая на transform(\"sum\") по каналу"
    assert abs(mix["share"].sum() - 3) < 0.01, "доли внутри каждого канала должны давать в сумме 1: группировать для transform нужно по channel"
    assert mix["share"].tolist()[1] == 0.526, "доли нужно округлить до трёх знаков: у кофе на маркетплейсе — 0.526"


def test_dishes():
    "dishes — строки посуды"
    assert isinstance(dishes, pd.DataFrame) and len(dishes) == 3 and (dishes["category"] == "Посуда").all(), "dishes — три строки таблицы mix с категорией «Посуда»"
    assert sorted(dishes["share"].tolist()) == [0.085, 0.102, 0.188], f"доли посуды сейчас {sorted(dishes['share'].tolist())}, а должны быть 0.085, 0.102 и 0.188"
# ─── другое решение ───
mix = orders.groupby(["channel", "category"])["revenue"].sum().reset_index()
mix["share"] = (mix["revenue"] / mix["channel"].map(orders.groupby("channel")["revenue"].sum())).round(3)
dishes = mix.query("category == 'Посуда'")
# ─── ошибка ───
mix = orders.groupby(["channel", "category"], as_index=False)["revenue"].sum()
mix["share"] = (mix["revenue"] / mix.groupby("category")["revenue"].transform("sum")).round(3)
dishes = mix[mix["category"] == "Посуда"]
# ─── ошибка ───
mix = orders.groupby(["channel", "category"], as_index=False)["revenue"].sum()
mix["share"] = mix["revenue"] / mix.groupby("channel")["revenue"].transform("sum")
dishes = mix[mix["category"] == "Посуда"]

# %% typical [exercise]
order_totals = orders.groupby(["channel", "order_id"], as_index=False)["revenue"].sum()
typical = order_totals.groupby("channel")["revenue"].agg(["mean", "median"])
# ─── заготовка ───
order_totals = ...
typical = ...
# ─── проверка ───
def test_totals():
    "order_totals — сумма каждого заказа с его каналом"
    assert isinstance(order_totals, pd.DataFrame), f"order_totals — это {type(order_totals).__name__}, а нужна таблица"
    assert list(order_totals.columns) == ["channel", "order_id", "revenue"], f"столбцы сейчас {list(order_totals.columns)}, а нужны channel, order_id, revenue"
    assert len(order_totals) == 1576 and order_totals["revenue"].sum() == 3301420, "в order_totals 1576 строк — по одной на заказ"


def test_typical():
    "typical — средний и медианный чек по каналам"
    assert isinstance(typical, pd.DataFrame), f"typical — это {type(typical).__name__}, а нужна таблица: .agg([\"mean\", \"median\"])"
    assert list(typical.columns) == ["mean", "median"], f"столбцы сейчас {list(typical.columns)}, а нужны mean и median"
    assert abs(typical.loc["сайт", "mean"] - 1339.4195) > 1e-3, "это средняя выручка строки, а не заказа: считать нужно по таблице order_totals"
    assert abs(typical.loc["сайт", "mean"] - 1522920 / 715) < 1e-6, "средний чек сайта должен быть ≈ 2130"
    assert typical.loc["сайт", "median"] == 1610 and typical.loc["приложение", "median"] == 1450, "медианный чек: сайт — 1610, приложение — 1450"
# ─── другое решение ───
order_totals = orders.groupby(["channel", "order_id"])["revenue"].sum().reset_index()
g = order_totals.groupby("channel")["revenue"]
typical = pd.DataFrame({"mean": g.mean(), "median": g.median()})
# ─── ошибка ───
order_totals = orders.groupby(["channel", "order_id"], as_index=False)["revenue"].sum()
typical = orders.groupby("channel")["revenue"].agg(["mean", "median"])

# %% report
report = channels[["total", "share", "orders", "check", "orders_per_buyer"]].copy()
report["median_check"] = typical["median"]
report.round(2).sort_values("total", ascending=False)
