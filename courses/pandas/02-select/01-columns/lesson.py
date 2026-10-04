# Урок pd-columns. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% several
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv")
orders[["product", "price"]]

# %% no-list [raises=KeyError]
orders["product", "price"]

# %% goods [exercise]
goods = orders[["product", "price", "quantity"]]
# ─── заготовка ───
goods = ...
# ─── проверка ───
def test_goods():
    "goods — таблица из трёх столбцов"
    assert not isinstance(goods, pd.Series), "goods — один столбец Series, а нужна таблица из трёх столбцов: список названий в двойных скобках"
    assert isinstance(goods, pd.DataFrame), f"goods — это {type(goods).__name__}, а нужна таблица"
    assert goods.shape[1] != 9, "в goods все 9 столбцов, а нужны только три"
    assert sorted(goods.columns) == ["price", "product", "quantity"], f"столбцы сейчас {list(goods.columns)}, а нужны product, price, quantity"
    assert list(goods.columns) == ["product", "price", "quantity"], f"порядок столбцов сейчас {list(goods.columns)}, а нужен product, price, quantity"
    assert len(goods) == 2448, f"в goods {len(goods)} строк, а нужны все 2448"
# ─── другое решение ───
names = ["product", "price", "quantity"]
goods = orders[names]
# ─── ошибка ───
goods = orders["product"]
# ─── ошибка ───
goods = orders[["price", "product", "quantity"]]
# ─── ошибка ───
goods = orders

# %% order
who_where = ["city", "customer_id", "date"]
orders[who_where].head(3)

# %% one-two
print(type(orders["price"]))
print(type(orders[["price"]]))

# %% one-frame
orders[["price"]].head(3)

# %% brackets-quiz [quiz]
print(type(orders[["city"]]).__name__)

# %% single [exercise]
price_column = orders["price"]
price_table = orders[["price"]]
# ─── заготовка ───
price_column = ...
price_table = ...
# ─── проверка ───
def test_column():
    "price_column — столбец Series"
    assert not isinstance(price_column, pd.DataFrame), "price_column — таблица, а нужен Series: одни квадратные скобки"
    assert isinstance(price_column, pd.Series), f"price_column — это {type(price_column).__name__}, а нужен Series"
    assert price_column.name == "price", f"это столбец {price_column.name!r}, а нужен price"


def test_table():
    "price_table — таблица из одного столбца"
    assert not isinstance(price_table, pd.Series), "price_table — Series, а нужна таблица из одного столбца: двойные скобки"
    assert isinstance(price_table, pd.DataFrame), f"price_table — это {type(price_table).__name__}, а нужна таблица"
    assert list(price_table.columns) == ["price"], f"столбцы сейчас {list(price_table.columns)}, а нужен один — price"
# ─── другое решение ───
price_table = orders[["price"]]
price_column = price_table["price"]
# ─── ошибка ───
price_column = orders[["price"]]
price_table = orders["price"]
# ─── ошибка ───
price_column = orders["price"]
price_table = orders["price"]

# %% frame-mean
orders[["price", "quantity"]].mean()

# %% averages [exercise]
maxima = orders[["price", "quantity"]].max()
top_quantity = maxima["quantity"]
# ─── заготовка ───
maxima = ...
top_quantity = ...
# ─── проверка ───
def test_maxima():
    "maxima — наибольшие цена и количество"
    assert not isinstance(maxima, pd.DataFrame), "maxima — таблица: вы выбрали столбцы, но не вызвали max()"
    assert isinstance(maxima, pd.Series), f"maxima — это {type(maxima).__name__}, а нужен Series"
    assert sorted(maxima.index) == ["price", "quantity"], f"метки сейчас {list(maxima.index)}, а нужны price и quantity: сначала выберите два столбца, потом max()"
    assert maxima["price"] == 3200, "числа не те: нужен max(), а не другой метод"


def test_top():
    "top_quantity — наибольшее количество"
    assert not isinstance(top_quantity, pd.Series), "top_quantity — Series, а нужно одно число"
    assert top_quantity != 3200, "3200 — наибольшая цена, а нужно значение по метке \"quantity\""
    assert top_quantity == 10, f"top_quantity = {top_quantity!r} — это не наибольшее количество"
# ─── другое решение ───
maxima = pd.Series({"price": orders["price"].max(), "quantity": orders["quantity"].max()})
top_quantity = maxima["quantity"]
# ─── ошибка ───
maxima = orders[["price", "quantity"]]
top_quantity = 10
# ─── ошибка ───
maxima = orders[["price", "quantity"]].max()
top_quantity = maxima["price"]

# %% dot
orders.price.head(3)

# %% dot-trap
cups = pd.DataFrame({"name": ["S", "M", "L"], "size": [0.25, 0.35, 0.45]})
print(cups.size)
print(cups["size"].tolist())

# %% receipt [exercise]
receipt = orders[["order_id", "product", "quantity", "price"]].head(10)
n_receipt_cols = receipt.shape[1]
# ─── заготовка ───
receipt = ...
n_receipt_cols = ...
# ─── проверка ───
def test_receipt():
    "receipt — 10 строк и 4 столбца"
    assert isinstance(receipt, pd.DataFrame), f"receipt — это {type(receipt).__name__}, а нужна таблица"
    assert list(receipt.columns) == ["order_id", "product", "quantity", "price"], f"столбцы сейчас {list(receipt.columns)}, а нужны order_id, product, quantity, price — в этом порядке"
    assert len(receipt) != 2448, "в receipt все строки, а нужны первые 10"
    assert len(receipt) == 10, f"в receipt {len(receipt)} строк, а нужно 10"
    assert receipt["order_id"].tolist()[:2] == [10001, 10001], "это не первые строки таблицы orders"


def test_cols():
    "n_receipt_cols — число столбцов"
    assert n_receipt_cols == 4, f"n_receipt_cols = {n_receipt_cols!r}: число столбцов — второе число в shape"
# ─── другое решение ───
receipt = orders.head(10)[["order_id", "product", "quantity", "price"]]
n_receipt_cols = len(receipt.columns)
# ─── ошибка ───
receipt = orders[["order_id", "product", "quantity", "price"]]
n_receipt_cols = receipt.shape[1]
# ─── ошибка ───
receipt = orders[["order_id", "product", "price", "quantity"]].head(10)
n_receipt_cols = receipt.shape[1]
