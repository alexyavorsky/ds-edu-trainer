# Урок pd-isin-query. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% long
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv")
hot = orders[(orders["category"] == "Кофе") | (orders["category"] == "Чай")]
len(hot)

# %% isin
hot = orders[orders["category"].isin(["Кофе", "Чай"])]
len(hot)

# %% not-isin
other = orders[~orders["category"].isin(["Кофе", "Чай"])]
other["category"].value_counts()

# %% east [exercise]
east = orders[orders["city"].isin(["Казань", "Екатеринбург", "Новосибирск"])]
n_capitals = len(orders[~orders["city"].isin(["Казань", "Екатеринбург", "Новосибирск"])])
# ─── заготовка ───
east = ...
n_capitals = ...
# ─── проверка ───
def test_east():
    "east — строки из Казани, Екатеринбурга и Новосибирска"
    assert isinstance(east, pd.DataFrame), f"east — это {type(east).__name__}, а нужна таблица: orders[маска]"
    assert sorted(east["city"].unique()) == ["Екатеринбург", "Казань", "Новосибирск"], f"в east города {sorted(east['city'].unique())}, а нужны Екатеринбург, Казань, Новосибирск"
    assert len(east) == 911, f"в east {len(east)} строк, а из трёх городов их 911"


def test_capitals():
    "n_capitals — сколько строк из остальных городов"
    assert n_capitals != 911, "911 — строки из трёх городов, а нужны все остальные: переверните маску оператором ~"
    assert n_capitals == 1537, f"n_capitals = {n_capitals!r}, а строк из остальных городов 1537"
# ─── другое решение ───
in_east = orders["city"].isin(["Казань", "Екатеринбург", "Новосибирск"])
east = orders[in_east]
n_capitals = (~in_east).sum()
# ─── ошибка ───
east = orders[orders["city"].isin(["Казань", "Екатеринбург"])]
n_capitals = len(orders[~orders["city"].isin(["Казань", "Екатеринбург"])])
# ─── ошибка ───
east = orders[orders["city"].isin(["Казань", "Екатеринбург", "Новосибирск"])]
n_capitals = len(east)

# %% between
middle = orders[orders["price"].between(320, 390)]
print(len(middle))
print(sorted(middle["price"].unique().tolist()))

# %% between-neither
strict = orders[orders["price"].between(320, 390, inclusive="neither")]
print(sorted(strict["price"].unique().tolist()))

# %% between-quiz [quiz]
print(pd.Series([1, 5, 10]).between(1, 5).sum())

# %% middle [exercise]
mid_price = orders[orders["price"].between(500, 1000)]
mid_share = orders["price"].between(500, 1000).mean()
# ─── заготовка ───
mid_price = ...
mid_share = ...
# ─── проверка ───
def test_mid():
    "mid_price — цена от 500 до 1000 включительно"
    assert isinstance(mid_price, pd.DataFrame), f"mid_price — это {type(mid_price).__name__}, а нужна таблица: orders[маска]"
    assert mid_price["price"].min() >= 500 and mid_price["price"].max() <= 1000, "в mid_price есть цены за пределами 500–1000"
    assert len(mid_price) == 858, f"в mid_price {len(mid_price)} строк, а с ценой от 500 до 1000 их 858"


def test_share():
    "mid_share — доля таких строк"
    assert mid_share != 858, "858 — число строк, а доля — среднее маски"
    assert abs(mid_share - 858 / 2448) < 1e-9, f"mid_share = {mid_share!r}, а доля ≈ 0.35"
# ─── другое решение ───
mid_price = orders[(orders["price"] >= 500) & (orders["price"] <= 1000)]
mid_share = len(mid_price) / len(orders)
# ─── ошибка ───
mid_price = orders[orders["price"].between(500, 1000)]
mid_share = orders["price"].between(500, 1000).sum()
# ─── ошибка ───
mid_price = orders[orders["price"].between(600, 1000)]
mid_share = orders["price"].between(600, 1000).mean()

# %% loc-mask
orders.loc[orders["quantity"] >= 9, ["date", "city", "product", "quantity"]]

# %% loc-series
print(orders.loc[orders["city"] == "Казань", "price"].mean())

# %% luxury [exercise]
luxury = orders.loc[(orders["city"] == "Казань") & (orders["price"] > 2000), ["date", "product", "price"]]
luxury_avg = luxury["price"].mean()
# ─── заготовка ───
luxury = ...
luxury_avg = ...
# ─── проверка ───
def test_luxury():
    "luxury — дорогие покупки в Казани, три столбца"
    assert isinstance(luxury, pd.DataFrame), f"luxury — это {type(luxury).__name__}, а нужна таблица: orders.loc[маска, список столбцов]"
    assert list(luxury.columns) == ["date", "product", "price"], f"столбцы сейчас {list(luxury.columns)}, а нужны date, product, price"
    assert luxury["price"].min() > 2000, "в luxury есть цена не выше 2000"
    assert len(luxury) == 12, f"в luxury {len(luxury)} строк, а покупок дороже 2000 в Казани 12"


def test_avg():
    "luxury_avg — средняя цена таких покупок"
    assert abs(luxury_avg - 2666.6667) < 1e-3, f"luxury_avg = {luxury_avg!r}, а средняя цена ≈ 2666.67"
# ─── другое решение ───
mask = (orders["city"] == "Казань") & (orders["price"] > 2000)
luxury = orders[mask][["date", "product", "price"]]
luxury_avg = orders.loc[mask, "price"].mean()
# ─── ошибка ───
luxury = orders.loc[(orders["city"] == "Казань") & (orders["price"] > 2000)]
luxury_avg = luxury["price"].mean()
# ─── ошибка ───
luxury = orders.loc[orders["price"] > 2000, ["date", "product", "price"]]
luxury_avg = luxury["price"].mean()

# %% query
orders.query("price > 3000 and city == 'Новосибирск'")

# %% query-var
limit = 3000
towns = ["Казань", "Новосибирск"]
len(orders.query("price > @limit and city in @towns"))

# %% query-error [raises=UndefinedVariableError]
orders.query("city == Казань")

# %% bulk [exercise]
min_price = 1000
bulk = orders.query("price > @min_price and quantity >= 3")
# ─── заготовка ───
min_price = 1000
bulk = ...
# ─── проверка ───
def test_bulk():
    "bulk — дороже min_price и не меньше 3 штук"
    assert isinstance(bulk, pd.DataFrame), f"bulk — это {type(bulk).__name__}, а нужна таблица: orders.query(\"...\")"
    assert len(bulk) > 0, "в bulk нет строк: проверьте условия"
    assert bulk["price"].min() > 1000, "в bulk есть цена не выше 1000: условие — price > @min_price"
    assert bulk["quantity"].min() >= 3, "в bulk есть строки, где меньше 3 штук: оба условия нужны сразу — and"
    assert len(bulk) == 54, f"в bulk {len(bulk)} строк, а подходящих 54"
# ─── другое решение ───
min_price = 1000
bulk = orders[(orders["price"] > min_price) & (orders["quantity"] >= 3)]
# ─── ошибка ───
min_price = 1000
bulk = orders.query("price > @min_price or quantity >= 3")
# ─── ошибка ───
min_price = 1000
bulk = orders.query("price > @min_price and quantity > 3")
