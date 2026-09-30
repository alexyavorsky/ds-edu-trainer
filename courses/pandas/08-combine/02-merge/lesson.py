# Урок pd-merge. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% tables
import pandas as pd

orders = pd.read_csv("data/orders.csv")
products = pd.read_csv("data/products.csv")
print(orders.head(3))
print(products.head(3))

# %% toy
left = pd.DataFrame({"id": [1, 2, 3], "name": ["Аня", "Борис", "Вика"]})
right = pd.DataFrame({"id": [2, 3, 4], "city": ["Тула", "Сочи", "Омск"]})
left.merge(right, on="id")

# %% toy-left
left.merge(right, on="id", how="left")

# %% toy-outer
left.merge(right, on="id", how="outer")

# %% how-quiz [quiz]
print(len(left.merge(right, on="id", how="right")))

# %% real
named = orders.merge(products[["product_id", "name"]], on="product_id")
print(len(orders), len(named))
named.head(3)

# %% priced [exercise]
priced = orders.merge(products, on="product_id")
priced["revenue"] = priced["price"] * priced["quantity"]
total = priced["revenue"].sum()
# ─── заготовка ───
priced = ...
# добавьте в priced столбец revenue
total = ...
# ─── проверка ───
def test_priced():
    "priced — заказы с данными о товаре"
    assert isinstance(priced, pd.DataFrame), f"priced — это {type(priced).__name__}, а нужна таблица: orders.merge(products, on=\"product_id\")"
    assert len(priced) == 2448, f"в priced {len(priced)} строк, а должно остаться 2448 — столько же, сколько в orders"
    assert "price" in priced.columns and "category" in priced.columns, "в priced должны появиться столбцы товаров — price, category и другие"
    assert "order_id" in priced.columns and "quantity" in priced.columns, "в priced должны остаться столбцы заказов: слева — orders, справа — products"


def test_revenue():
    "revenue и total — выручка строки и за год"
    assert "revenue" in priced.columns, "в priced нет столбца revenue: цена × количество"
    assert priced["revenue"].sum() == 3301420, "сумма revenue должна быть 3 301 420: priced[\"price\"] * priced[\"quantity\"]"
    assert total == 3301420, f"total = {total!r}, а выручка за год — 3 301 420"
# ─── другое решение ───
priced = pd.merge(orders, products[["product_id", "name", "category", "price", "cost"]], on="product_id", how="left")
priced["revenue"] = priced["quantity"] * priced["price"]
total = sum(priced["revenue"])
# ─── ошибка ───
priced = orders.merge(products, on="product_id")
priced["revenue"] = priced["cost"] * priced["quantity"]
total = priced["revenue"].sum()
# ─── ошибка ───
priced = products
priced["revenue"] = priced["price"]
total = priced["revenue"].sum()

# %% profit [exercise]
priced["profit"] = (priced["price"] - priced["cost"]) * priced["quantity"]
category_profit = priced.groupby("category")["profit"].sum().sort_values(ascending=False)
total_profit = priced["profit"].sum()
# ─── заготовка ───
# добавьте в priced столбец profit
category_profit = ...
total_profit = ...
# ─── проверка ───
def test_profit():
    "profit — прибыль строки: (цена − себестоимость) × количество"
    assert "profit" in priced.columns, "в priced нет столбца profit"
    assert priced.loc[0, "profit"] != 4500, "скобки: сначала разность цены и себестоимости, потом умножение на количество — (price − cost) × quantity"
    assert priced["profit"].sum() == 1542150, "прибыль не та: (priced[\"price\"] - priced[\"cost\"]) * priced[\"quantity\"]"
    assert total_profit == 1542150, f"total_profit = {total_profit!r}, а прибыль за год — 1 542 150"


def test_category():
    "category_profit — прибыль по категориям, по убыванию"
    assert isinstance(category_profit, pd.Series) and len(category_profit) == 5, "category_profit — Series по пяти категориям: priced.groupby(\"category\")[\"profit\"].sum()"
    assert category_profit["Чай"] == 340440, "суммы не те: сумма столбца profit по категориям"
    assert category_profit.tolist() == sorted(category_profit.tolist(), reverse=True), "отсортируйте category_profit по убыванию"
# ─── другое решение ───
priced["profit"] = priced["price"] * priced["quantity"] - priced["cost"] * priced["quantity"]
category_profit = priced.groupby("category")["profit"].sum().sort_values(ascending=False)
total_profit = category_profit.sum()
# ─── ошибка ───
priced["profit"] = priced["price"] - priced["cost"] * priced["quantity"]
category_profit = priced.groupby("category")["profit"].sum().sort_values(ascending=False)
total_profit = priced["profit"].sum()
# ─── ошибка ───
priced["profit"] = (priced["price"] - priced["cost"]) * priced["quantity"]
category_profit = priced.groupby("category")["profit"].sum()
total_profit = priced["profit"].sum()

# %% customers
customers = pd.read_csv("data/customers.csv")
order_counts = orders.groupby("customer_id", as_index=False).agg(n_orders=("order_id", "nunique"))
print(len(customers), len(order_counts))
order_counts.head(3)

# %% inner-loss
print(len(customers.merge(order_counts, on="customer_id")))
print(len(customers.merge(order_counts, on="customer_id", how="left")))

# %% left-nan
activity = customers.merge(order_counts, on="customer_id", how="left")
activity.head(4)

# %% sleepers [exercise]
activity["n_orders"] = activity["n_orders"].fillna(0).astype("int64")
sleepers = activity[activity["n_orders"] == 0]
n_sleepers = len(sleepers)
# ─── заготовка ───
# замените пропуски в activity["n_orders"] нулями и сделайте столбец целым
sleepers = ...
n_sleepers = ...
# ─── проверка ───
def test_orders():
    "n_orders — число заказов целым числом, без пропусков"
    assert activity["n_orders"].isna().sum() == 0, "в activity[\"n_orders\"] остались пропуски: клиент без пары в таблице заказов — это ноль заказов, fillna(0). Результат запишите обратно в столбец"
    assert str(activity["n_orders"].dtype) in ("int64", "int32"), f"тип столбца n_orders — {activity['n_orders'].dtype}, а нужен целый: astype(\"int64\")"
    assert activity["n_orders"].sum() == 1576 and len(activity) == 240, "в activity должны быть все 240 клиентов, а сумма заказов — 1576"


def test_sleepers():
    "sleepers — клиенты без заказов"
    assert isinstance(sleepers, pd.DataFrame), f"sleepers — это {type(sleepers).__name__}, а нужна таблица: activity[маска]"
    assert len(sleepers) == 27 and n_sleepers == 27, f"в sleepers {len(sleepers)} строк, n_sleepers = {n_sleepers!r}, а клиентов без заказов 27"
    assert (sleepers["n_orders"] == 0).all(), "в sleepers должны быть только клиенты с нулём заказов"
# ─── другое решение ───
activity["n_orders"] = activity["n_orders"].fillna(0).astype("int64")
sleepers = customers[~customers["customer_id"].isin(orders["customer_id"])]
sleepers = activity[activity["customer_id"].isin(sleepers["customer_id"])]
n_sleepers = (activity["n_orders"] == 0).sum()
# ─── ошибка ───
sleepers = activity[activity["n_orders"] == 0]
n_sleepers = len(sleepers)
# ─── ошибка ───
activity["n_orders"] = activity["n_orders"].fillna(0).astype("int64")
sleepers = activity[activity["n_orders"] > 0]
n_sleepers = len(sleepers)

# %% narrow
segments = customers[["customer_id", "segment"]]
with_segment = priced.merge(segments, on="customer_id")
print(with_segment.shape)
with_segment[["order_id", "name", "revenue", "segment"]].head(3)

# %% segments [exercise]
segment_stats = with_segment.groupby("segment").agg(revenue=("revenue", "sum"), buyers=("customer_id", "nunique"))
segment_stats["per_buyer"] = (segment_stats["revenue"] / segment_stats["buyers"]).round()
best_segment = segment_stats["per_buyer"].idxmax()
# ─── заготовка ───
segment_stats = ...
# добавьте в segment_stats столбец per_buyer
best_segment = ...
# ─── проверка ───
def test_stats():
    "segment_stats — выручка и число покупателей по сегментам"
    assert isinstance(segment_stats, pd.DataFrame), f"segment_stats — это {type(segment_stats).__name__}, а нужна таблица: with_segment.groupby(\"segment\").agg(...)"
    assert sorted(segment_stats.index) == ["новый", "оптовый", "постоянный"], "в индексе должны быть три сегмента"
    assert list(segment_stats.columns)[:2] == ["revenue", "buyers"], f"столбцы сейчас {list(segment_stats.columns)}, а первые два должны быть revenue и buyers"
    assert segment_stats.loc["оптовый", "revenue"] == 756240, "revenue — сумма столбца revenue"
    assert segment_stats.loc["оптовый", "buyers"] == 25, "buyers — число разных покупателей: (\"customer_id\", \"nunique\")"


def test_per_buyer():
    "per_buyer — выручка на покупателя, best_segment — самый ценный сегмент"
    assert "per_buyer" in segment_stats.columns, "в segment_stats нет столбца per_buyer"
    assert segment_stats.loc["оптовый", "per_buyer"] == 30250 and segment_stats.loc["новый", "per_buyer"] == 13621, "per_buyer — revenue, делённая на buyers, с округлением до рублей"
    assert best_segment == "оптовый", f"best_segment = {best_segment!r}, а больше всего выручки на покупателя у другого сегмента"
# ─── другое решение ───
g = with_segment.groupby("segment")
segment_stats = pd.DataFrame({"revenue": g["revenue"].sum(), "buyers": g["customer_id"].nunique()})
segment_stats["per_buyer"] = round(segment_stats["revenue"] / segment_stats["buyers"])
best_segment = segment_stats.sort_values("per_buyer").index[-1]
# ─── ошибка ───
segment_stats = with_segment.groupby("segment").agg(revenue=("revenue", "sum"), buyers=("customer_id", "count"))
segment_stats["per_buyer"] = (segment_stats["revenue"] / segment_stats["buyers"]).round()
best_segment = segment_stats["per_buyer"].idxmax()
# ─── ошибка ───
segment_stats = with_segment.groupby("segment").agg(revenue=("revenue", "sum"), buyers=("customer_id", "nunique"))
segment_stats["per_buyer"] = (segment_stats["revenue"] / segment_stats["buyers"]).round()
best_segment = segment_stats["revenue"].idxmax()
