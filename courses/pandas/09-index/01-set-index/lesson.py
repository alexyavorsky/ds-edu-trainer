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
customers = pd.read_csv("data/customers.csv")
clients = customers.set_index("customer_id")
c012_city = clients.loc["C012", "city"]
picked = clients.loc[["C005", "C100", "C200"], ["name", "segment"]]
# ─── заготовка ───
customers = pd.read_csv("data/customers.csv")
clients = ...
c012_city = ...
picked = ...
# ─── проверка ───
def test_clients():
    "clients — справочник клиентов с customer_id в индексе"
    assert isinstance(clients, pd.DataFrame), f"clients — это {type(clients).__name__}, а нужна таблица"
    assert clients.index.name == "customer_id", "в индексе clients должны быть коды клиентов"
    assert list(clients.columns) == ["name", "city", "signup_date", "segment"], f"столбцы сейчас {list(clients.columns)}: customer_id должен уйти из столбцов в индекс"
    assert "customer_id" in customers.columns, "таблицу customers менять не нужно: результат set_index сохраните в clients"


def test_lookup():
    "c012_city — город клиента C012, picked — три клиента, два столбца"
    assert isinstance(c012_city, str), f"c012_city — это {type(c012_city).__name__}, а нужно одно значение — название города"
    assert c012_city == "Москва", f"c012_city = {c012_city!r} — это не город клиента C012"
    assert isinstance(picked, pd.DataFrame), f"picked — это {type(picked).__name__}, а нужна таблица"
    assert list(picked.index) == ["C005", "C100", "C200"], f"метки строк сейчас {list(picked.index)}, а нужны C005, C100, C200 — в этом порядке"
    assert list(picked.columns) == ["name", "segment"], f"столбцы сейчас {list(picked.columns)}, а нужны name и segment"
# ─── другое решение ───
customers = pd.read_csv("data/customers.csv")
clients = pd.read_csv("data/customers.csv", index_col="customer_id")
c012_city = clients["city"]["C012"]
picked = clients[["name", "segment"]].loc[["C005", "C100", "C200"]]
# ─── ошибка ───
customers = pd.read_csv("data/customers.csv")
clients = customers
c012_city = "Москва"
picked = customers[customers["customer_id"].isin(["C005", "C100", "C200"])][["name", "segment"]]
# ─── ошибка ───
customers = pd.read_csv("data/customers.csv")
clients = customers.set_index("customer_id")
c012_city = clients.loc["C012"]
picked = clients.loc[["C005", "C100", "C200"], ["name", "segment"]]

# %% missing-label [raises=KeyError]
catalog.loc["P99"]

# %% reset
catalog.reset_index().head(2)

# %% index-col
pd.read_csv("data/products.csv", index_col="product_id").head(2)

# %% by-name
named = products.set_index("name")
named.loc["Зефир", "price"]

# %% sorted-slice
named = named.sort_index()
named.loc["Т":"Ф", "price"]

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
    assert isinstance(by_name, pd.DataFrame) and by_name.index.name == "name", "by_name — справочник с названием товара в индексе"
    assert list(by_name.index) == sorted(by_name.index), "индекс должен идти по алфавиту"


def test_k():
    "k_products — товары на букву К, k_mean — их средняя цена"
    assert isinstance(k_products, pd.DataFrame), f"k_products — это {type(k_products).__name__}, а нужна таблица"
    assert list(k_products.index) == ["Колумбия 250 г", "Кофе без кофеина 250 г", "Кофемолка ручная", "Кружка 350 мл"], f"в k_products сейчас {list(k_products.index)}: нужны все товары на «К» — срез по меткам"
    assert abs(k_mean - 1300.0) < 1e-9, f"k_mean = {k_mean!r} — это не средняя цена товаров на «К»"
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
print(type(orders.loc[10001]))
print(type(orders.loc[11576]))

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
    assert isinstance(order_10140, pd.DataFrame), f"order_10140 — это {type(order_10140).__name__}, а нужна таблица"
    assert len(order_10140) == 3 and n_lines == 3, f"в order_10140 {len(order_10140)} строк, n_lines = {n_lines!r}: нужны все строки заказа 10140 и их число"
    assert order_sum == 3360, f"order_sum = {order_sum!r} — это не сумма заказа"


def test_flat():
    "flat — снова обычная таблица с order_id в столбце"
    assert isinstance(flat, pd.DataFrame), f"flat — это {type(flat).__name__}, а нужна таблица"
    assert "order_id" in flat.columns, "order_id должен вернуться в столбцы"
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
