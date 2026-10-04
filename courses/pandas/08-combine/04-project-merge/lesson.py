# Урок pd-project-merge. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import pandas as pd

orders = pd.read_csv("data/orders.csv")
products = pd.read_csv("data/products.csv")
customers = pd.read_csv("data/customers.csv")
print(orders.shape, products.shape, customers.shape)
orders.head(3)

# %% keys [exercise]
product_key_ok = products["product_id"].is_unique
customer_key_ok = customers["customer_id"].is_unique
order_key_ok = orders["order_id"].is_unique
# ─── заготовка ───
product_key_ok = ...
customer_key_ok = ...
order_key_ok = ...
# ─── проверка ───
def test_keys():
    "уникальны ли ключи трёх таблиц"
    assert product_key_ok is True or product_key_ok == True, "product_key_ok — это не ответ на вопрос, уникален ли product_id в products"
    assert customer_key_ok is True or customer_key_ok == True, "customer_key_ok — это не ответ на вопрос, уникален ли customer_id в customers"
    assert not isinstance(order_key_ok, pd.Series), "order_key_ok — Series, а нужно одно значение True или False"
    assert order_key_ok is False or order_key_ok == False, "order_key_ok — это не ответ на вопрос, уникален ли order_id в orders"
# ─── другое решение ───
product_key_ok = products["product_id"].nunique() == len(products)
customer_key_ok = not customers["customer_id"].duplicated().any()
order_key_ok = orders["order_id"].nunique() == len(orders)
# ─── ошибка ───
product_key_ok = True
customer_key_ok = True
order_key_ok = True

# %% lines [exercise]
lines = orders.merge(products, on="product_id", validate="many_to_one")
lines["revenue"] = lines["price"] * lines["quantity"]
lines["profit"] = (lines["price"] - lines["cost"]) * lines["quantity"]
# ─── заготовка ───
lines = ...
# добавьте в lines столбцы revenue и profit
# ─── проверка ───
def test_lines():
    "lines — заказы с данными товара"
    assert isinstance(lines, pd.DataFrame), f"lines — это {type(lines).__name__}, а нужна таблица"
    assert len(lines) == 2448, f"в lines {len(lines)} строк, а должно остаться 2448"
    assert "price" in lines.columns and "cost" in lines.columns and "order_id" in lines.columns, "в lines должны быть столбцы и заказов, и товаров"


def test_money():
    "revenue и profit — выручка и прибыль строки"
    assert "revenue" in lines.columns and "profit" in lines.columns, "в lines нужны столбцы revenue и profit"
    assert lines["revenue"].sum() == 3301420, "revenue не тот: выручка строки — цена × количество"
    assert lines["profit"].sum() != 3301420 - 9670, "себестоимость нужно умножить на количество"
    assert lines["profit"].sum() == 1542150, "profit не тот: проверьте формулу из условия"
# ─── другое решение ───
lines = pd.merge(orders, products, on="product_id", how="left")
lines["revenue"] = lines["price"] * lines["quantity"]
lines["profit"] = lines["revenue"] - lines["cost"] * lines["quantity"]
# ─── ошибка ───
lines = orders.merge(products, on="product_id", validate="many_to_one")
lines["revenue"] = lines["price"] * lines["quantity"]
lines["profit"] = lines["revenue"] - lines["cost"]

# %% full [exercise]
full = lines.merge(customers[["customer_id", "city", "segment"]], on="customer_id", validate="many_to_one")
# ─── заготовка ───
full = ...
# ─── проверка ───
def test_full():
    "full — к строкам заказов добавлены город и сегмент покупателя"
    assert isinstance(full, pd.DataFrame), f"full — это {type(full).__name__}, а нужна таблица"
    assert len(full) == 2448, f"в full {len(full)} строк, а должно остаться 2448"
    assert "city" in full.columns and "segment" in full.columns, "в full нужны столбцы city и segment из справочника клиентов"
    assert "name_x" not in full.columns and "name_y" not in full.columns, "задвоился столбец name: берите из customers только customer_id, city и segment"
    assert "signup_date" not in full.columns, "лишние столбцы: берите из customers только customer_id, city и segment"
    assert "name" in full.columns and "profit" in full.columns, "в full должны остаться столбцы таблицы lines"
# ─── другое решение ───
full = lines.merge(customers.drop(columns=["name", "signup_date"]), on="customer_id", how="left")
# ─── ошибка ───
full = lines.merge(customers, on="customer_id")
# ─── ошибка ───
full = lines

# %% check
shop = pd.read_csv("data/shop_orders.csv")
shop["revenue"] = shop["price"] * shop["quantity"]
ours = full.groupby("city")["revenue"].sum()
theirs = shop.groupby("city")["revenue"].sum()
print((ours == theirs).all())
print(ours.sum(), theirs.sum())

# %% cities [exercise]
city_table = full.groupby("city").agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
city_table["margin"] = (city_table["profit"] / city_table["revenue"]).round(3)
city_table = city_table.sort_values("profit", ascending=False)
# ─── заготовка ───
city_table = ...
# ─── проверка ───
def test_city_table():
    "city_table — выручка, прибыль и маржа по городам, по убыванию прибыли"
    assert isinstance(city_table, pd.DataFrame), f"city_table — это {type(city_table).__name__}, а нужна таблица"
    assert list(city_table.columns) == ["revenue", "profit", "margin"], f"столбцы сейчас {list(city_table.columns)}, а нужны revenue, profit, margin"
    assert len(city_table) == 5 and "Казань" in city_table.index, "в индексе должны быть пять городов"
    assert city_table.loc["Москва", "profit"] == 612070, "profit не тот: нужна прибыль города"
    assert abs(city_table.loc["Москва", "margin"] - 0.467) < 1e-9, "margin не тот: нужна доля прибыли в выручке с округлением до трёх знаков"
    assert city_table["profit"].tolist() == sorted(city_table["profit"].tolist(), reverse=True), "отсортируйте city_table по убыванию profit"
# ─── другое решение ───
g = full.groupby("city")
city_table = pd.DataFrame({"revenue": g["revenue"].sum(), "profit": g["profit"].sum()})
city_table["margin"] = round(city_table["profit"] / city_table["revenue"], 3)
city_table = city_table.sort_values("profit", ascending=False)
# ─── ошибка ───
city_table = full.groupby("city").agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
city_table["margin"] = (city_table["profit"] / city_table["revenue"]).round(3)
# ─── ошибка ───
city_table = full.groupby("city").agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
city_table["margin"] = (city_table["revenue"] / city_table["profit"]).round(3)
city_table = city_table.sort_values("profit", ascending=False)

# %% products [exercise]
product_table = full.groupby(["category", "name"], as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
product_table["margin"] = (product_table["profit"] / product_table["revenue"]).round(3)
top_profit = product_table.nlargest(3, "profit")
low_margin = product_table.nsmallest(3, "margin")
# ─── заготовка ───
product_table = ...
top_profit = ...
low_margin = ...
# ─── проверка ───
def test_product_table():
    "product_table — выручка, прибыль и маржа по товарам"
    assert isinstance(product_table, pd.DataFrame), f"product_table — это {type(product_table).__name__}, а нужна таблица"
    assert list(product_table.columns) == ["category", "name", "revenue", "profit", "margin"], f"столбцы сейчас {list(product_table.columns)}, а нужны category, name, revenue, profit, margin"
    assert len(product_table) == 20 and product_table["profit"].sum() == 1542150, "в product_table 20 товаров"
    assert abs(product_table["margin"].max() - 0.625) < 1e-9, "margin не тот: нужна доля прибыли в выручке с округлением до трёх знаков"


def test_tops():
    "top_profit — три самых прибыльных товара, low_margin — три товара с наименьшей маржой"
    assert isinstance(top_profit, pd.DataFrame) and len(top_profit) == 3, "top_profit — три строки"
    assert top_profit["name"].tolist() == ["Эфиопия 250 г", "Колумбия 250 г", "Кофе без кофеина 250 г"], f"в top_profit сейчас {top_profit['name'].tolist()}: нужны три товара с наибольшей прибылью"
    assert isinstance(low_margin, pd.DataFrame) and len(low_margin) == 3, "low_margin — три строки"
    assert low_margin["name"].tolist() == ["Бразилия 1 кг", "Эспрессо-смесь 1 кг", "Кофемолка ручная"], f"в low_margin сейчас {low_margin['name'].tolist()}: нужны три товара с наименьшей маржой"
# ─── другое решение ───
product_table = full.groupby(["category", "name"])[["revenue", "profit"]].sum().reset_index()
product_table["margin"] = (product_table["profit"] / product_table["revenue"]).round(3)
top_profit = product_table.sort_values("profit", ascending=False).head(3)
low_margin = product_table.sort_values("margin").head(3)
# ─── ошибка ───
product_table = full.groupby(["category", "name"], as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
product_table["margin"] = (product_table["profit"] / product_table["revenue"]).round(3)
top_profit = product_table.nlargest(3, "revenue")
low_margin = product_table.nlargest(3, "margin")

# %% delivery [exercise]
delivery = pd.concat([pd.read_csv("data/delivery_h1.csv"), pd.read_csv("data/delivery_h2.csv")], ignore_index=True)
order_table = full.groupby(["order_id", "channel"], as_index=False).agg(total=("revenue", "sum"))
order_table = order_table.merge(delivery, on="order_id", validate="one_to_one")
channel_delivery = order_table.groupby("channel").agg(days=("days", "mean"), rating=("rating", "mean")).round(2)
# ─── заготовка ───
delivery = ...
order_table = ...
channel_delivery = ...
# ─── проверка ───
def test_delivery():
    "delivery — доставка за год"
    assert isinstance(delivery, pd.DataFrame) and len(delivery) == 1576, "delivery — обе выгрузки одной таблицей"
    assert delivery.index.is_unique, "метки delivery повторяются"


def test_order_table():
    "order_table — один заказ в строке: канал, сумма, срок, оценка"
    assert isinstance(order_table, pd.DataFrame), f"order_table — это {type(order_table).__name__}, а нужна таблица"
    assert len(order_table) != 2448, "в order_table 2448 строк — это позиции, а не заказы: сначала сгруппируйте full по order_id и channel"
    assert len(order_table) == 1576, f"в order_table {len(order_table)} строк: нужна одна строка на заказ"
    assert list(order_table.columns) == ["order_id", "channel", "total", "days", "rating"], f"столбцы сейчас {list(order_table.columns)}, а нужны order_id, channel, total, days, rating"
    assert order_table["total"].sum() == 3301420, "total не тот: нужна сумма revenue заказа"


def test_channels():
    "channel_delivery — средний срок и оценка по каналам"
    assert isinstance(channel_delivery, pd.DataFrame) and list(channel_delivery.columns) == ["days", "rating"], "channel_delivery — таблица со столбцами days и rating"
    assert channel_delivery.loc["маркетплейс", "days"] == 5.25 and channel_delivery.loc["сайт", "rating"] == 3.76, "средние должны быть округлены до двух знаков"
# ─── другое решение ───
delivery = pd.concat([pd.read_csv("data/delivery_h1.csv"), pd.read_csv("data/delivery_h2.csv")]).reset_index(drop=True)
order_table = full.groupby(["order_id", "channel"])["revenue"].sum().reset_index().rename(columns={"revenue": "total"})
order_table = order_table.merge(delivery, on="order_id", how="left")
channel_delivery = order_table.groupby("channel")[["days", "rating"]].mean().round(2)
# ─── ошибка ───
delivery = pd.concat([pd.read_csv("data/delivery_h1.csv"), pd.read_csv("data/delivery_h2.csv")], ignore_index=True)
order_table = full[["order_id", "channel", "revenue"]].rename(columns={"revenue": "total"}).merge(delivery, on="order_id")
channel_delivery = order_table.groupby("channel").agg(days=("days", "mean"), rating=("rating", "mean")).round(2)

# %% summary
print("Выручка:", full["revenue"].sum(), "· прибыль:", full["profit"].sum(), "· маржа:", round(full["profit"].sum() / full["revenue"].sum(), 3))
print(city_table)
print(channel_delivery)
