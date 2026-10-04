# Урок pd-series. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% column
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv")
orders["price"]

# %% types
print(type(orders))
print(type(orders["price"]))

# %% wrong-name [raises=KeyError]
orders["Price"]

# %% cities [exercise]
cities = orders["city"]
# ─── заготовка ───
cities = ...
# ─── проверка ───
def test_series():
    "cities — столбец Series"
    assert not isinstance(cities, str), "cities — это строка с названием, а нужен сам столбец"
    assert not isinstance(cities, pd.DataFrame), "cities — целая таблица, а нужен один столбец"
    assert isinstance(cities, pd.Series), f"cities — это {type(cities).__name__}, а нужен столбец Series"


def test_city():
    "в cities — города всех 2448 строк"
    assert isinstance(cities, pd.Series), "cities пока не столбец — сначала исправьте то, о чём говорит проверка выше"
    assert cities.name == "city", f"это столбец {cities.name!r}, а нужен \"city\""
    assert len(cities) == 2448, f"в cities {len(cities)} значений, а строк в таблице 2448 — столбец нужен целиком"
# ─── другое решение ───
cities = orders.loc[:, "city"]
# ─── ошибка ───
cities = "city"
# ─── ошибка ───
cities = orders["city"].head()
# ─── ошибка ───
cities = orders["channel"]

# %% head
orders["product"].head(3)

# %% attrs
prices = orders["price"]
print(prices.name)
print(prices.dtype)
print(prices.index)

# %% totals
print(prices.sum())
print(prices.max())
print(prices.min())
print(prices.mean())

# %% items [exercise]
total_items = orders["quantity"].sum()
max_items = orders["quantity"].max()
mean_items = orders["quantity"].mean()
# ─── заготовка ───
total_items = ...
max_items = ...
mean_items = ...
# ─── проверка ───
def test_total():
    "total_items — сколько штук продано"
    assert not isinstance(total_items, pd.Series), "total_items — столбец, а нужно одно число"
    assert not callable(total_items), "total_items — сам метод: вы забыли скобки после sum"
    assert total_items != 1685990, "это сумма столбца price, а нужен столбец quantity"
    assert total_items == 5210, f"total_items = {total_items} — это не сумма столбца quantity"


def test_max():
    "max_items — больше всего штук в одной строке"
    assert not callable(max_items), "max_items — сам метод: вы забыли скобки после max"
    assert max_items == 10, f"max_items = {max_items} — это не максимум столбца quantity"


def test_mean():
    "mean_items — в среднем штук в строке"
    assert not callable(mean_items), "mean_items — сам метод: вы забыли скобки после mean"
    assert abs(mean_items - 2.128268) < 1e-5, f"mean_items = {mean_items} — это не среднее столбца quantity"
# ─── другое решение ───
quantity = orders["quantity"]
total_items = sum(quantity)
max_items = max(quantity)
mean_items = total_items / len(quantity)
# ─── ошибка ───
total_items = orders["price"].sum()
max_items = orders["price"].max()
mean_items = orders["price"].mean()
# ─── ошибка ───
total_items = orders["quantity"].sum
max_items = orders["quantity"].max
mean_items = orders["quantity"].mean

# %% number
prices * 0.9

# %% two-series
revenue = orders["price"] * orders["quantity"]
revenue

# %% double-quiz [quiz]
print(len(orders["quantity"] * 2))

# %% discount [exercise]
sale_price = orders["price"] * 0.85
sale_total = (sale_price * orders["quantity"]).sum()
# ─── заготовка ───
sale_price = ...
sale_total = ...
# ─── проверка ───
def test_price():
    "sale_price — цены со скидкой 15 %"
    assert isinstance(sale_price, pd.Series), f"sale_price — это {type(sale_price).__name__}, а нужен столбец: цена каждой строки со скидкой"
    assert len(sale_price) == 2448, f"в sale_price {len(sale_price)} значений, а строк 2448"
    assert abs(sale_price[0] - 480.0) > 1e-6, "получилось 15 % от цены — это размер скидки; цена со скидкой — 85 % от исходной"
    assert abs(sale_price[0] - 2720.0) < 1e-6, f"первая цена со скидкой — {sale_price[0]}: цена со скидкой — 85 % от исходной"
    assert abs(sale_price.sum() - 1685990 * 0.85) < 1e-3, "в sale_price должны быть цены всех строк со скидкой"


def test_total():
    "sale_total — выручка года со скидкой"
    assert not isinstance(sale_total, pd.Series), "sale_total — столбец, а нужно одно число"
    assert abs(sale_total - 1433091.5) > 1e-3, "это сумма цен со скидкой, без учёта количества: выручка строки — цена × количество"
    assert abs(sale_total - 2806207.0) < 1e-3, f"sale_total = {sale_total} — это не выручка года со скидкой"
# ─── другое решение ───
sale_price = orders["price"] - orders["price"] * 0.15
sale_total = (orders["price"] * orders["quantity"]).sum() * 0.85
# ─── ошибка ───
sale_price = orders["price"] * 0.15
sale_total = (sale_price * orders["quantity"]).sum()
# ─── ошибка ───
sale_price = orders["price"] * 0.85
sale_total = sale_price.sum()

# %% biggest [exercise]
max_revenue = revenue.max()
avg_revenue = revenue.mean()
# ─── заготовка ───
max_revenue = ...
avg_revenue = ...
# ─── проверка ───
def test_max():
    "max_revenue — самая большая выручка одной строки"
    assert not isinstance(max_revenue, pd.Series), "max_revenue — столбец, а нужно одно число"
    assert max_revenue != 3200, "3200 — наибольшая цена; нужна наибольшая выручка строки"
    assert max_revenue == 9030, f"max_revenue = {max_revenue} — это не наибольшая выручка строки"


def test_avg():
    "avg_revenue — средняя выручка строки"
    assert not isinstance(avg_revenue, pd.Series), "avg_revenue — столбец, а нужно одно число"
    assert abs(avg_revenue - 688.7214) > 1e-3, "это средняя цена; нужна средняя выручка строки"
    assert abs(avg_revenue - 1348.61928) < 1e-4, f"avg_revenue = {avg_revenue} — это не средняя выручка строки"
# ─── другое решение ───
max_revenue = max(revenue)
avg_revenue = revenue.sum() / len(revenue)
# ─── ошибка ───
max_revenue = orders["price"].max()
avg_revenue = orders["price"].mean()
