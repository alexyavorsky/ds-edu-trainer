# Урок pd-set-index. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% default
import pandas as pd

products = pd.read_csv("data/products.csv")
products.head(3)

# %% search
products[products["product_id"] == "P05"]

# %% set
catalog = products.set_index("product_id")
catalog.head(3)

# %% loc
print(catalog.loc["P05", "price"])
catalog.loc["P05"]

# %% shape-quiz [quiz]
print(products.shape[1] - catalog.shape[1])

# %% gone [raises=KeyError]
catalog["product_id"]

# %% index-attr
print(catalog.index.name)
print(list(catalog.index[:4]))
print("P05" in catalog.index, "P99" in catalog.index)

# %% lookup [exercise]
catalog = products.set_index("product_id")
p12_name = catalog.loc["P12", "name"]
picked = catalog.loc[["P03", "P11", "P18"], ["name", "price"]]
# ─── заготовка ───
catalog = ...
p12_name = ...
picked = ...
# ─── проверка ───
def test_catalog():
    "catalog — справочник с product_id в индексе"
    assert isinstance(catalog, pd.DataFrame), f"catalog — это {type(catalog).__name__}, а нужна таблица: products.set_index(\"product_id\")"
    assert catalog.index.name == "product_id", "в индексе catalog должны быть коды товаров: products.set_index(\"product_id\")"
    assert list(catalog.columns) == ["name", "category", "price", "cost"], f"столбцы сейчас {list(catalog.columns)}: product_id должен уйти из столбцов в индекс"


def test_lookup():
    "p12_name — название товара P12, picked — три товара, два столбца"
    assert isinstance(p12_name, str), f"p12_name — это {type(p12_name).__name__}, а нужно одно значение — название: catalog.loc[\"P12\", \"name\"]"
    assert p12_name == "Миндаль в шоколаде", f"p12_name = {p12_name!r}, а товар P12 — «Миндаль в шоколаде»: catalog.loc[\"P12\", \"name\"]"
    assert isinstance(picked, pd.DataFrame), f"picked — это {type(picked).__name__}, а нужна таблица: catalog.loc[список меток, список столбцов]"
    assert list(picked.index) == ["P03", "P11", "P18"], f"метки строк сейчас {list(picked.index)}, а нужны P03, P11, P18 — в этом порядке"
    assert list(picked.columns) == ["name", "price"], f"столбцы сейчас {list(picked.columns)}, а нужны name и price"
# ─── другое решение ───
catalog = pd.read_csv("data/products.csv", index_col="product_id")
p12_name = catalog["name"]["P12"]
picked = catalog[["name", "price"]].loc[["P03", "P11", "P18"]]
# ─── ошибка ───
catalog = products
p12_name = "Миндаль в шоколаде"
picked = products[products["product_id"].isin(["P03", "P11", "P18"])][["name", "price"]]
# ─── ошибка ───
catalog = products.set_index("product_id")
p12_name = catalog.loc["P12"]
picked = catalog.loc[["P03", "P11", "P18"], ["name", "price"]]

# %% missing-label [raises=KeyError]
catalog.loc["P99"]

# %% reset
catalog.reset_index().head(2)

# %% index-col
pd.read_csv("data/products.csv", index_col="product_id").head(2)

# %% by-name
by_name = products.set_index("name")
by_name.loc["Зефир", "price"]

# %% sorted-slice
by_name = by_name.sort_index()
by_name.loc["Т":"Ф", "price"]

# %% alphabet [exercise]
by_name = products.set_index("name").sort_index()
k_products = by_name.loc["К":"Л"]
k_mean = k_products["price"].mean()
# ─── заготовка ───
by_name = ...
k_products = ...
k_mean = ...
# ─── проверка ───
def test_by_name():
    "by_name — товары с названием в индексе, по алфавиту"
    assert isinstance(by_name, pd.DataFrame) and by_name.index.name == "name", "by_name — справочник с названием товара в индексе: products.set_index(\"name\")"
    assert list(by_name.index) == sorted(by_name.index), "индекс должен идти по алфавиту: добавьте sort_index()"


def test_k():
    "k_products — товары на букву К, k_mean — их средняя цена"
    assert isinstance(k_products, pd.DataFrame), f"k_products — это {type(k_products).__name__}, а нужна таблица: by_name.loc[\"К\":\"Л\"]"
    assert list(k_products.index) == ["Колумбия 250 г", "Кофе без кофеина 250 г", "Кофемолка ручная", "Кружка 350 мл"], f"в k_products сейчас {list(k_products.index)}, а товаров на «К» четыре: срез меток от \"К\" до \"Л\""
    assert abs(k_mean - 1300.0) < 1e-9, f"k_mean = {k_mean!r}, а средняя цена товаров на «К» — 1300.0"
# ─── другое решение ───
by_name = products.sort_values("name").set_index("name")
k_products = by_name[by_name.index.str.startswith("К")]
k_mean = k_products["price"].sum() / len(k_products)
# ─── ошибка ───
by_name = products.set_index("name")
k_products = by_name[by_name.index.str.startswith("К")]
k_mean = k_products["price"].mean()
# ─── ошибка ───
by_name = products.set_index("name").sort_index()
k_products = by_name.loc["К":"П"]
k_mean = k_products["price"].mean()

# %% dup-index
orders = pd.read_csv("data/shop_orders.csv").set_index("order_id")
print(orders.index.is_unique)
orders.loc[10001]

# %% dup-one
print(type(orders.loc[10001]).__name__)
print(type(orders.loc[11576]).__name__)

# %% order [exercise]
order_10140 = orders.loc[10140]
n_lines = len(order_10140)
order_sum = (order_10140["price"] * order_10140["quantity"]).sum()
flat = orders.reset_index()
# ─── заготовка ───
order_10140 = ...
n_lines = ...
order_sum = ...
flat = ...
# ─── проверка ───
def test_order():
    "order_10140 — строки заказа 10140, n_lines — их число, order_sum — сумма заказа"
    assert isinstance(order_10140, pd.DataFrame), f"order_10140 — это {type(order_10140).__name__}, а нужна таблица: orders.loc[10140]"
    assert len(order_10140) == 3 and n_lines == 3, f"в заказе 10140 три строки, а n_lines = {n_lines!r}"
    assert order_sum == 3360, f"order_sum = {order_sum!r}, а сумма заказа — 3360: цена × количество по строкам заказа, затем sum()"


def test_flat():
    "flat — снова обычная таблица с order_id в столбце"
    assert isinstance(flat, pd.DataFrame), f"flat — это {type(flat).__name__}, а нужна таблица: orders.reset_index()"
    assert "order_id" in flat.columns, "order_id должен вернуться в столбцы: reset_index() без drop=True"
    assert flat.shape == (2448, 9) and list(flat.index[:3]) == [0, 1, 2], "в flat 2448 строк и 9 столбцов, индекс — номера строк"
# ─── другое решение ───
order_10140 = orders[orders.index == 10140]
n_lines = order_10140.shape[0]
order_sum = sum(order_10140["price"] * order_10140["quantity"])
flat = orders.reset_index()
# ─── ошибка ───
order_10140 = orders.loc[10140]
n_lines = len(order_10140)
order_sum = (order_10140["price"] * order_10140["quantity"]).sum()
flat = orders.reset_index(drop=True)
