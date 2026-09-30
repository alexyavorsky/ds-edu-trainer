# Урок pd-groups-top. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% series
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv")
orders["revenue"] = orders["price"] * orders["quantity"]
by_city = orders.groupby("city")["revenue"].sum()
by_city

# %% reset
by_city.reset_index()

# %% as-index
orders.groupby("city", as_index=False)["revenue"].sum()

# %% size-name
orders.groupby("city").size().reset_index(name="lines")

# %% table [exercise]
category_table = orders.groupby("category", as_index=False)["revenue"].sum()
category_table = category_table.sort_values("revenue", ascending=False).reset_index(drop=True)
# ─── заготовка ───
category_table = ...
# ─── проверка ───
def test_table():
    "category_table — таблица со столбцами category и revenue"
    assert not isinstance(category_table, pd.Series), "category_table — Series с категориями в индексе, а нужна таблица: as_index=False в groupby или reset_index() после"
    assert isinstance(category_table, pd.DataFrame), f"category_table — это {type(category_table).__name__}, а нужна таблица"
    assert list(category_table.columns) == ["category", "revenue"], f"столбцы сейчас {list(category_table.columns)}, а нужны category и revenue"
    assert len(category_table) == 5 and category_table["revenue"].sum() == 3301420, "в таблице должны быть пять категорий с суммой выручки"


def test_order():
    "строки — по убыванию выручки, индекс с нуля"
    assert isinstance(category_table, pd.DataFrame) and "revenue" in category_table.columns, "сначала исправьте то, о чём говорит проверка выше"
    values = category_table["revenue"].tolist()
    assert values == sorted(values, reverse=True), "строки должны идти по убыванию выручки: sort_values(\"revenue\", ascending=False)"
    assert list(category_table.index) == [0, 1, 2, 3, 4], f"индекс сейчас {list(category_table.index)}, а нужен 0–4 подряд: reset_index(drop=True) после сортировки"
    assert category_table.loc[0, "category"] == "Кофе", "первой должна быть категория с наибольшей выручкой"
# ─── другое решение ───
category_table = orders.groupby("category")["revenue"].sum().sort_values(ascending=False).reset_index()
# ─── ошибка ───
category_table = orders.groupby("category")["revenue"].sum().sort_values(ascending=False)
# ─── ошибка ───
category_table = orders.groupby("category", as_index=False)["revenue"].sum()
# ─── ошибка ───
category_table = orders.groupby("category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)

# %% pairs
pairs = orders.groupby(["city", "channel"], as_index=False)["revenue"].sum()
pairs.head(4)

# %% pairs-filter
pairs[pairs["revenue"] > 300000]

# %% flat-quiz [quiz]
print(orders.groupby(["city", "channel"], as_index=False)["revenue"].sum().shape)

# %% weak [exercise]
pair_table = orders.groupby(["city", "channel"], as_index=False).agg(total=("revenue", "sum"), orders=("order_id", "nunique"))
weak = pair_table[pair_table["orders"] < 55].sort_values("orders")
# ─── заготовка ───
pair_table = ...
weak = ...
# ─── проверка ───
def test_pairs():
    "pair_table — выручка и число заказов по парам «город, канал»"
    assert isinstance(pair_table, pd.DataFrame), f"pair_table — это {type(pair_table).__name__}, а нужна таблица"
    assert "city" in pair_table.columns and "channel" in pair_table.columns, "city и channel должны быть обычными столбцами, а не индексом: as_index=False"
    assert list(pair_table.columns) == ["city", "channel", "total", "orders"], f"столбцы сейчас {list(pair_table.columns)}, а нужны city, channel, total, orders"
    assert len(pair_table) == 15 and pair_table["total"].sum() == 3301420, "в pair_table 15 строк — по одной на пару, total — сумма revenue"
    assert pair_table["orders"].sum() == 1576, "orders — число разных заказов: orders=(\"order_id\", \"nunique\")"


def test_weak():
    "weak — пары, где заказов меньше 55, от меньшего к большему"
    assert isinstance(weak, pd.DataFrame), f"weak — это {type(weak).__name__}, а нужна таблица: pair_table[маска]"
    assert "orders" in weak.columns and len(weak) > 0 and weak["orders"].max() < 55, "в weak должны быть только пары, где заказов меньше 55"
    assert len(weak) == 4, f"в weak {len(weak)} строк, а пар с числом заказов меньше 55 — {4}"
    assert weak["orders"].tolist() == sorted(weak["orders"].tolist()), "отсортируйте weak по числу заказов по возрастанию"
# ─── другое решение ───
pair_table = orders.groupby(["city", "channel"]).agg(total=("revenue", "sum"), orders=("order_id", "nunique")).reset_index()
weak = pair_table.query("orders < 55").sort_values("orders")
# ─── ошибка ───
pair_table = orders.groupby(["city", "channel"]).agg(total=("revenue", "sum"), orders=("order_id", "nunique"))
weak = pair_table[pair_table["orders"] < 55].sort_values("orders")
# ─── ошибка ───
pair_table = orders.groupby(["city", "channel"], as_index=False).agg(total=("revenue", "sum"), orders=("order_id", "nunique"))
weak = pair_table[pair_table["orders"] < 55].sort_values("orders", ascending=False)

# %% products
products = orders.groupby(["category", "product"], as_index=False)["revenue"].sum()
products = products.sort_values("revenue", ascending=False)
products.head(5)

# %% top-each
products.groupby("category").head(2)

# %% top-each-sorted
products.groupby("category").head(2).sort_values(["category", "revenue"], ascending=[True, False])

# %% worst [exercise]
worst = products.groupby("category").tail(1).sort_values("category").reset_index(drop=True)
# ─── заготовка ───
worst = ...
# ─── проверка ───
def test_worst():
    "worst — товар с наименьшей выручкой в каждой категории"
    assert isinstance(worst, pd.DataFrame), f"worst — это {type(worst).__name__}, а нужна таблица"
    assert list(worst.columns) == ["category", "product", "revenue"], f"столбцы сейчас {list(worst.columns)}, а нужны category, product, revenue"
    assert len(worst) == 5, f"в worst {len(worst)} строк, а категорий пять — по одному товару на каждую"
    assert worst["category"].tolist() == ["Аксессуары", "Кофе", "Посуда", "Сладости", "Чай"], "отсортируйте worst по категории и пронумеруйте строки заново"
    assert "Кофемолка ручная" not in worst["product"].tolist(), "в worst попали лучшие товары, а нужны худшие: products отсортирована по убыванию — худшие в конце каждой группы, tail(1)"
    assert worst["product"].tolist() == ["Фильтры бумажные", "Кофе без кофеина 250 г", "Кружка 350 мл", "Печенье овсяное", "Травяной сбор 50 г"], f"товары сейчас {worst['product'].tolist()}"
    assert list(worst.index) == [0, 1, 2, 3, 4], "индекс должен идти с нуля подряд: reset_index(drop=True)"
# ─── другое решение ───
worst = products.sort_values("revenue").groupby("category").head(1).sort_values("category").reset_index(drop=True)
# ─── ошибка ───
worst = products.groupby("category").head(1).sort_values("category").reset_index(drop=True)
# ─── ошибка ───
worst = products.groupby("category").tail(1)

# %% vip [exercise]
customers = orders.groupby(["city", "customer_id"], as_index=False)["revenue"].sum()
vip = customers.sort_values("revenue", ascending=False).groupby("city").head(2)
vip = vip.sort_values(["city", "revenue"], ascending=[True, False]).reset_index(drop=True)
# ─── заготовка ───
customers = ...
vip = ...
# ─── проверка ───
def test_customers():
    "customers — выручка по покупателям с городом"
    assert isinstance(customers, pd.DataFrame), f"customers — это {type(customers).__name__}, а нужна таблица"
    assert list(customers.columns) == ["city", "customer_id", "revenue"], f"столбцы сейчас {list(customers.columns)}, а нужны city, customer_id, revenue: groupby([\"city\", \"customer_id\"], as_index=False)"
    assert len(customers) == 213 and customers["revenue"].sum() == 3301420, "в customers 213 строк — по одной на покупателя"


def test_vip():
    "vip — два лучших покупателя каждого города"
    assert isinstance(vip, pd.DataFrame), f"vip — это {type(vip).__name__}, а нужна таблица"
    assert len(vip) != 2, "в vip два покупателя на всю таблицу, а нужно по два на каждый город: .groupby(\"city\").head(2)"
    assert len(vip) == 10, f"в vip {len(vip)} строк, а нужно 10: по два покупателя на пять городов"
    assert vip["city"].value_counts().tolist() == [2, 2, 2, 2, 2], "в vip должно быть ровно по два покупателя на город"
    assert vip["customer_id"].tolist() == ["C122", "C138", "C076", "C203", "C134", "C118", "C023", "C090", "C137", "C024"], "это не лучшие покупатели: сначала отсортируйте customers по убыванию выручки, потом groupby(\"city\").head(2); в конце — сортировка по городу и убыванию выручки"
    assert list(vip.index) == list(range(10)), "индекс должен идти с нуля подряд: reset_index(drop=True)"
# ─── другое решение ───
customers = orders.groupby(["city", "customer_id"])["revenue"].sum().reset_index()
vip = customers.sort_values(["city", "revenue"], ascending=[True, False]).groupby("city").head(2).reset_index(drop=True)
# ─── ошибка ───
customers = orders.groupby(["city", "customer_id"], as_index=False)["revenue"].sum()
vip = customers.sort_values("revenue", ascending=False).head(2)
vip = vip.sort_values(["city", "revenue"], ascending=[True, False]).reset_index(drop=True)
# ─── ошибка ───
customers = orders.groupby(["city", "customer_id"], as_index=False)["revenue"].sum()
vip = customers.groupby("city").head(2)
vip = vip.sort_values(["city", "revenue"], ascending=[True, False]).reset_index(drop=True)
