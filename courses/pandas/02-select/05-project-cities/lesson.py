# Урок pd-project-cities. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv")
orders.head(3)

# %% kazan [exercise]
revenue = orders["price"] * orders["quantity"]
kazan_big = orders[(orders["city"] == "Казань") & (revenue >= 5000)]
# ─── заготовка ───
revenue = ...
kazan_big = ...
# ─── проверка ───
def test_revenue():
    "revenue — выручка каждой строки"
    assert isinstance(revenue, pd.Series), f"revenue — это {type(revenue).__name__}, а нужен Series: цена × количество"
    assert len(revenue) == 2448 and revenue.sum() == 3301420, "revenue — это orders[\"price\"] * orders[\"quantity\"] по всем строкам"


def test_kazan():
    "kazan_big — покупки в Казани на 5000 ₽ и больше"
    assert isinstance(kazan_big, pd.DataFrame), f"kazan_big — это {type(kazan_big).__name__}, а нужна таблица: orders[(условие) & (условие)]"
    assert len(kazan_big) > 0, "в kazan_big нет строк: сравнивать с 5000 нужно выручку строки, а не цену"
    assert (kazan_big["city"] == "Казань").all(), "в kazan_big есть другие города"
    assert (kazan_big["price"] * kazan_big["quantity"]).min() >= 5000, "в kazan_big есть строки с выручкой меньше 5000"
    assert len(kazan_big) == 5, f"в kazan_big {len(kazan_big)} строк, а подходящих 5"
# ─── другое решение ───
revenue = orders["quantity"] * orders["price"]
kazan_big = orders.loc[(orders["city"] == "Казань") & (revenue >= 5000)]
# ─── ошибка ───
revenue = orders["price"] * orders["quantity"]
kazan_big = orders[(orders["city"] == "Казань") & (orders["price"] >= 5000)]
# ─── ошибка ───
revenue = orders["price"] * orders["quantity"]
kazan_big = orders[revenue >= 5000]

# %% dates
print(orders["date"].min(), orders["date"].max())
print("2025-02-28" < "2025-03-01")
print((orders["date"] >= "2025-12-01").sum())

# %% winter [exercise]
is_winter = (orders["date"] < "2025-03-01") | (orders["date"] >= "2025-12-01")
is_tea = orders["category"] == "Чай"
tea_winter = is_tea[is_winter].mean()
tea_rest = is_tea[~is_winter].mean()
# ─── заготовка ───
is_winter = ...
is_tea = ...
tea_winter = ...
tea_rest = ...
# ─── проверка ───
def test_masks():
    "is_winter и is_tea — маски"
    assert isinstance(is_winter, pd.Series) and is_winter.dtype == bool, "is_winter должна быть маской — Series из True и False"
    assert is_winter.sum() != 0, "в is_winter нет ни одного True: январь–февраль ИЛИ декабрь — оператор |, а не &"
    assert is_winter.sum() != 329, "в is_winter только декабрь: добавьте январь и февраль — даты раньше \"2025-03-01\""
    assert is_winter.sum() == 764, f"в is_winter {is_winter.sum()} зимних строк, а их 764: даты до 1 марта или с 1 декабря"
    assert isinstance(is_tea, pd.Series) and is_tea.dtype == bool and is_tea.sum() == 682, "is_tea — маска: категория равна \"Чай\""


def test_shares():
    "tea_winter и tea_rest — доля чая зимой и в остальное время"
    assert abs(tea_winter - 268) > 1e-9, "268 — число строк с чаем зимой; доля — среднее маски is_tea по зимним строкам"
    assert abs(tea_winter - 268 / 682) > 1e-9, "это доля зимы среди чая; нужна доля чая среди зимних строк: is_tea[is_winter].mean()"
    assert abs(tea_winter - 268 / 764) < 1e-9, f"tea_winter = {tea_winter!r}, а доля чая зимой ≈ 0.351"
    assert abs(tea_rest - 414 / 1684) < 1e-9, f"tea_rest = {tea_rest!r}, а доля чая в остальное время ≈ 0.246: маска ~is_winter"
# ─── другое решение ───
is_winter = ~orders["date"].between("2025-03-01", "2025-11-30")
is_tea = orders["category"] == "Чай"
tea_winter = (is_tea & is_winter).sum() / is_winter.sum()
tea_rest = (is_tea & ~is_winter).sum() / (~is_winter).sum()
# ─── ошибка ───
is_winter = (orders["date"] < "2025-03-01") | (orders["date"] >= "2025-12-01")
is_tea = orders["category"] == "Чай"
tea_winter = is_winter[is_tea].mean()
tea_rest = is_tea[~is_winter].mean()
# ─── ошибка ───
is_winter = orders["date"] >= "2025-12-01"
is_tea = orders["category"] == "Чай"
tea_winter = is_tea[is_winter].mean()
tea_rest = is_tea[~is_winter].mean()

# %% channels [exercise]
site_price = orders.loc[orders["channel"] == "сайт", "price"].mean()
market_price = orders.loc[orders["channel"] == "маркетплейс", "price"].mean()
market_costly = (orders.loc[orders["channel"] == "маркетплейс", "price"] >= 1000).mean()
# ─── заготовка ───
site_price = ...
market_price = ...
market_costly = ...
# ─── проверка ───
def test_prices():
    "site_price и market_price — средняя цена строки на сайте и маркетплейсе"
    assert abs(site_price - 688.7214) > 1e-3, "это средняя цена по всей таблице; нужны только строки с каналом \"сайт\""
    assert abs(site_price - 677.02726) < 1e-4, f"site_price = {site_price!r}, а средняя цена на сайте ≈ 677.03"
    assert abs(market_price - 728.19777) < 1e-4, f"market_price = {market_price!r}, а средняя цена на маркетплейсе ≈ 728.20"


def test_costly():
    "market_costly — доля строк от 1000 ₽ на маркетплейсе"
    assert abs(market_costly - 144) > 1e-9, "144 — число строк; доля — среднее маски"
    assert abs(market_costly - 144 / 2448) > 1e-9, "это доля среди всех строк таблицы; нужна доля среди строк маркетплейса"
    assert abs(market_costly - 144 / 627) < 1e-9, f"market_costly = {market_costly!r}, а доля ≈ 0.23"
# ─── другое решение ───
site = orders[orders["channel"] == "сайт"]
market = orders.query("channel == 'маркетплейс'")
site_price = site["price"].mean()
market_price = market["price"].mean()
market_costly = len(market[market["price"] >= 1000]) / len(market)
# ─── ошибка ───
site_price = orders["price"].mean()
market_price = orders["price"].mean()
market_costly = (orders["price"] >= 1000).mean()
# ─── ошибка ───
site_price = orders.loc[orders["channel"] == "сайт", "price"].mean()
market_price = orders.loc[orders["channel"] == "маркетплейс", "price"].mean()
market_costly = ((orders["channel"] == "маркетплейс") & (orders["price"] >= 1000)).mean()

# %% pricey [exercise]
pricey_cities = orders.loc[orders["price"] > 2000, "city"].value_counts()
pricey_moscow = pricey_cities["Москва"]
# ─── заготовка ───
pricey_cities = ...
pricey_moscow = ...
# ─── проверка ───
def test_cities():
    "pricey_cities — сколько дорогих покупок в каждом городе"
    assert isinstance(pricey_cities, pd.Series), f"pricey_cities — это {type(pricey_cities).__name__}, а нужен результат value_counts()"
    assert "Москва" in pricey_cities.index, "в индексе pricey_cities нет городов: value_counts нужен у столбца city"
    assert pricey_cities.sum() != 2448, "посчитаны все строки, а нужны только с ценой выше 2000: сначала фильтр, потом value_counts"
    assert pricey_cities.sum() == 66, f"в pricey_cities всего {pricey_cities.sum()} строк, а покупок дороже 2000 — 66"


def test_moscow():
    "pricey_moscow — дорогих покупок в Москве"
    assert pricey_moscow == 26, f"pricey_moscow = {pricey_moscow!r}, а дорогих покупок в Москве 26"
# ─── другое решение ───
pricey_cities = orders[orders["price"] > 2000]["city"].value_counts()
pricey_moscow = len(orders.query("price > 2000 and city == 'Москва'"))
# ─── ошибка ───
pricey_cities = orders["city"].value_counts()
pricey_moscow = pricey_cities["Москва"]

# %% record [exercise]
record = orders[orders["quantity"] == orders["quantity"].max()]
record_city = record["city"].iloc[0]
# ─── заготовка ───
record = ...
record_city = ...
# ─── проверка ───
def test_record():
    "record — строка с наибольшим количеством"
    assert isinstance(record, pd.DataFrame), f"record — это {type(record).__name__}, а нужна таблица: orders[маска]"
    assert len(record) == 1, f"в record {len(record)} строк, а покупка с наибольшим количеством одна: сравните quantity с его максимумом"
    assert record["quantity"].iloc[0] == 10, "в record не та строка: количество должно быть равно orders[\"quantity\"].max()"


def test_city():
    "record_city — город рекордной покупки"
    assert isinstance(record_city, str), f"record_city — это {type(record_city).__name__}, а нужно название города: одно значение, а не Series"
    assert record_city == "Новосибирск", f"record_city = {record_city!r}, а рекордная покупка сделана в другом городе"
# ─── другое решение ───
record = orders.query("quantity == quantity.max()")
record_city = record.iloc[0, 3]
# ─── ошибка ───
record = orders[orders["quantity"] == orders["quantity"].max()]
record_city = record["city"]
# ─── ошибка ───
record = orders[orders["quantity"] >= 9]
record_city = record["city"].iloc[0]

# %% summary
print("крупных покупок в Казани:", len(kazan_big))
print("доля чая зимой:", round(tea_winter * 100, 1), "% · в остальное время:", round(tea_rest * 100, 1), "%")
print("средняя цена: сайт", round(site_price), "₽ · маркетплейс", round(market_price), "₽")
print("покупок дороже 2000 ₽ в Москве:", pricey_moscow, "из", pricey_cities.sum())
print("рекорд:", record["quantity"].iloc[0], "шт. —", record["product"].iloc[0], "·", record_city)
