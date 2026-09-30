# Урок pd-new-columns. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% products
import pandas as pd

products = pd.read_csv("data/products.csv")
products.head()

# %% add
products["margin"] = products["price"] - products["cost"]
products.head()

# %% constant
products["currency"] = "RUB"
products["is_costly"] = products["price"] > 1000
products.head(3)

# %% revenue [exercise]
orders = pd.read_csv("data/shop_orders.csv")
orders["revenue"] = orders["price"] * orders["quantity"]
# ─── заготовка ───
orders = pd.read_csv("data/shop_orders.csv")
# добавьте в таблицу orders столбец revenue
# ─── проверка ───
def test_column():
    "в orders появился столбец revenue"
    assert "revenue" in orders.columns, "в таблице orders нет столбца revenue: orders[\"revenue\"] = ..."
    assert orders.shape[1] == 10, f"в orders {orders.shape[1]} столбцов, а должно стать 10: девять исходных и revenue"
    assert list(orders.columns)[-1] == "revenue", "новый столбец должен оказаться последним"


def test_values():
    "revenue — цена × количество"
    assert "revenue" in orders.columns, "сначала добавьте столбец revenue"
    assert orders["revenue"].dtype != object, "в столбце revenue не числа: справа от = должно стоять произведение двух столбцов"
    assert orders["revenue"].sum() != 1685990 + 5210, "цену и количество нужно перемножить, а не сложить"
    assert orders["revenue"].sum() == 3301420, f"сумма revenue — {orders['revenue'].sum()}, а выручка за год — 3 301 420: цена × количество"
# ─── другое решение ───
orders = pd.read_csv("data/shop_orders.csv")
orders = orders.assign(revenue=orders["quantity"] * orders["price"])
# ─── ошибка ───
orders = pd.read_csv("data/shop_orders.csv")
revenue = orders["price"] * orders["quantity"]
# ─── ошибка ───
orders = pd.read_csv("data/shop_orders.csv")
orders["revenue"] = orders["price"] + orders["quantity"]

# %% overwrite
products["margin"] = products["margin"] / products["price"]
products[["name", "price", "cost", "margin"]].head(3)

# %% round
products["margin"] = products["margin"].round(2)
products[["name", "price", "cost", "margin"]].head(3)

# %% markup [exercise]
products["markup"] = (products["price"] / products["cost"]).round(1)
# ─── заготовка ───
# добавьте в таблицу products столбец markup
# ─── проверка ───
def test_markup():
    "в products появился столбец markup"
    assert "markup" in products.columns, "в таблице products нет столбца markup: products[\"markup\"] = ..."
    assert products["markup"].dtype != object, "в столбце markup не числа"
    assert abs(products.loc[0, "markup"] - 0.6) > 1e-9, "дробь перевёрнута: наценка — это цена, делённая на себестоимость"
    assert abs(products.loc[0, "markup"] - 1.6666667) > 1e-4, "значения не округлены: добавьте .round(1) — выражение перед точкой возьмите в скобки"
    assert abs(products.loc[0, "markup"] - 1.7) < 1e-9, f"в первой строке markup = {products.loc[0, 'markup']}, а должно быть 1.7 (1450 / 870)"
    assert abs(products["markup"].sum() - 41.0) < 1e-6, "не все значения верны: цена / себестоимость, округлённая до одного знака"
# ─── другое решение ───
ratio = products["price"] / products["cost"]
products["markup"] = ratio.round(1)
# ─── ошибка ───
products["markup"] = products["price"] / products["cost"]
# ─── ошибка ───
products["markup"] = (products["cost"] / products["price"]).round(1)

# %% assign
with_vat = products.assign(price_vat=products["price"] * 1.2)
with_vat[["name", "price", "price_vat"]].head(3)

# %% assign-kept
print("price_vat" in products.columns)
print("price_vat" in with_vat.columns)

# %% rename
products.rename(columns={"category": "group", "cost": "cost_rub"}).head(2)

# %% drop
products.drop(columns=["margin", "cost"]).head(2)

# %% drop-kept
products.columns

# %% drop-quiz [quiz]
t = pd.DataFrame({"a": [1, 2], "b": [3, 4], "c": [5, 6]})
t.drop(columns=["c"])
print(t.shape[1])

# %% tidy [exercise]
catalog = products.rename(columns={"name": "product"}).drop(columns=["currency", "is_costly"])
# ─── заготовка ───
catalog = ...
# ─── проверка ───
def test_catalog():
    "catalog — без currency и is_costly, name переименован в product"
    assert isinstance(catalog, pd.DataFrame), f"catalog — это {type(catalog).__name__}, а нужна таблица"
    assert "currency" not in catalog.columns and "is_costly" not in catalog.columns, "в catalog остались столбцы currency или is_costly: drop(columns=[...])"
    assert "name" not in catalog.columns, "в catalog остался столбец name: rename(columns={\"name\": \"product\"})"
    assert "product" in catalog.columns, "в catalog нет столбца product: rename(columns={\"name\": \"product\"})"
    assert catalog.shape[1] == products.shape[1] - 2, f"в catalog {catalog.shape[1]} столбцов, а должно быть на два меньше, чем в products: удалить нужно только currency и is_costly"
    assert len(catalog) == 20, f"в catalog {len(catalog)} строк, а товаров 20"


def test_products_kept():
    "таблица products не изменилась"
    assert "name" in products.columns and "currency" in products.columns, (
        "таблица products изменилась: результат rename и drop нужно сохранить в catalog, а не в products. "
        "Чтобы вернуть products, нажмите «Выполнить все выше»"
    )
# ─── другое решение ───
catalog = products.drop(columns=["currency", "is_costly"])
catalog = catalog.rename(columns={"name": "product"})
# ─── другое решение ───
catalog = products[["product_id", "name", "category", "price", "cost", "margin", "markup"]].rename(columns={"name": "product"})
# ─── ошибка ───
catalog = products.rename(columns={"name": "product"})
# ─── ошибка ───
catalog = products.drop(columns=["currency", "is_costly"])

# %% profit [exercise]
orders["discount"] = orders["revenue"] * 0.05
orders["to_pay"] = orders["revenue"] - orders["discount"]
total_to_pay = orders["to_pay"].sum()
# ─── заготовка ───
# добавьте в orders столбцы discount и to_pay
total_to_pay = ...
# ─── проверка ───
def test_columns():
    "в orders есть столбцы discount и to_pay"
    assert "discount" in orders.columns, "в orders нет столбца discount"
    assert "to_pay" in orders.columns, "в orders нет столбца to_pay"
    assert abs(orders.loc[0, "discount"] - 320.0) < 1e-9, f"скидка в первой строке — {orders.loc[0, 'discount']}, а должна быть 320.0: 5 % от выручки 6400"
    assert abs(orders.loc[0, "to_pay"] - 320.0) > 1e-9, "в to_pay попала сама скидка: к оплате — выручка минус скидка"
    assert abs(orders.loc[0, "to_pay"] - 6080.0) < 1e-9, f"к оплате в первой строке — {orders.loc[0, 'to_pay']}, а должно быть 6080.0"


def test_total():
    "total_to_pay — сумма к оплате за год"
    assert abs(total_to_pay - 3136349.0) < 1e-3, f"total_to_pay = {total_to_pay!r}, а сумма столбца to_pay — 3 136 349"
# ─── другое решение ───
orders = orders.assign(discount=orders["revenue"] * 0.05)
orders = orders.assign(to_pay=orders["revenue"] - orders["discount"])
total_to_pay = orders["revenue"].sum() * 0.95
# ─── ошибка ───
orders["discount"] = orders["revenue"] * 0.05
orders["to_pay"] = orders["discount"]
total_to_pay = orders["to_pay"].sum()
