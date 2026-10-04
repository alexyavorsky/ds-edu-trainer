# Урок pd-loc-iloc. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% row
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv")
orders.iloc[0]

# %% slice
orders.iloc[2:5]

# %% picks
orders.iloc[[0, 10, -1]]

# %% out [raises=IndexError]
orders.iloc[5000]

# %% rows [exercise]
row_100 = orders.iloc[99]
last_rows = orders.iloc[-4:]
# ─── заготовка ───
row_100 = ...
last_rows = ...
# ─── проверка ───
def test_row():
    "row_100 — сотая по счёту строка"
    assert not isinstance(row_100, pd.DataFrame), "row_100 — таблица, а нужна одна строка: iloc с одним числом, без среза"
    assert isinstance(row_100, pd.Series), f"row_100 — это {type(row_100).__name__}, а нужна строка таблицы"
    assert row_100["product"] != "Улун 100 г", "это строка с позицией 100 — сто первая по счёту: позиции считаются с нуля"
    assert row_100["order_id"] == 10061 and row_100["product"] == "Зефир", "это не сотая строка: позиции считаются с нуля"


def test_last():
    "last_rows — четыре последние строки"
    assert isinstance(last_rows, pd.DataFrame), f"last_rows — это {type(last_rows).__name__}, а нужна таблица"
    assert len(last_rows) == 4, f"в last_rows {len(last_rows)} строк, а нужно 4"
    assert last_rows["order_id"].tolist() == [11574, 11575, 11575, 11576], "это не последние строки таблицы"
# ─── другое решение ───
row_100 = orders.loc[99]
last_rows = orders.tail(4)
# ─── ошибка ───
row_100 = orders.iloc[100]
last_rows = orders.iloc[-4:]
# ─── ошибка ───
row_100 = orders.iloc[99:100]
last_rows = orders.iloc[-4:]
# ─── ошибка ───
row_100 = orders.iloc[99]
last_rows = orders.iloc[-4]

# %% cell
print(orders.iloc[0, 6])
print(orders.iloc[0, -1])

# %% block
orders.iloc[:3, 3:6]

# %% corner [exercise]
corner = orders.iloc[10:15, :3]
# ─── заготовка ───
corner = ...
# ─── проверка ───
def test_corner():
    "corner — 5 строк и 3 столбца"
    assert isinstance(corner, pd.DataFrame), f"corner — это {type(corner).__name__}, а нужна таблица"
    assert corner.shape[0] != 4, "в corner 4 строки: конец среза iloc не входит"
    assert corner.shape == (5, 3), f"у corner размер {corner.shape}, а нужно 5 строк и 3 столбца"
    assert list(corner.columns) == ["order_id", "date", "customer_id"], f"столбцы сейчас {list(corner.columns)}, а нужны первые три"
    assert corner["order_id"].tolist() == [10008, 10009, 10010, 10011, 10012], "строки не те: нужны позиции с 10 по 14"
# ─── другое решение ───
corner = orders.iloc[10:15][["order_id", "date", "customer_id"]]
# ─── ошибка ───
corner = orders.iloc[10:14, :3]
# ─── ошибка ───
corner = orders.iloc[10:15]
# ─── ошибка ───
corner = orders.iloc[:3, 10:15]

# %% stats
stats = orders.describe()
stats

# %% loc-row
stats.loc["mean"]

# %% loc-cell
print(stats.loc["mean", "price"])
print(stats.loc["max", "quantity"])

# %% loc-block
stats.loc["min":"50%", ["price", "quantity"]]

# %% summary [exercise]
median_price = stats.loc["50%", "price"]
quartiles = stats.loc["25%":"75%", "quantity"]
# ─── заготовка ───
median_price = ...
quartiles = ...
# ─── проверка ───
def test_median():
    "median_price — медиана цены из сводки"
    assert not isinstance(median_price, (pd.Series, pd.DataFrame)), "median_price — не одно число: в loc нужны и метка строки, и название столбца"
    assert median_price != 2, "2 — медиана количества; нужен столбец price"
    assert abs(median_price - 688.7214) > 1e-3, "это среднее (mean), а нужна медиана"
    assert median_price == 540, f"median_price = {median_price!r} — это не медиана цены"


def test_quartiles():
    "quartiles — три строки сводки по quantity"
    assert not isinstance(quartiles, pd.DataFrame), "quartiles — таблица, а нужен один столбец quantity: название без списка"
    assert isinstance(quartiles, pd.Series), f"quartiles — это {type(quartiles).__name__}, а нужен Series"
    assert list(quartiles.index) == ["25%", "50%", "75%"], f"метки сейчас {list(quartiles.index)}, а нужны 25%, 50%, 75% — срез loc включает оба конца"
    assert quartiles.tolist() == [1, 2, 3], f"значения сейчас {quartiles.tolist()} — это не строки сводки по quantity"
# ─── другое решение ───
median_price = stats["price"]["50%"]
quartiles = stats["quantity"].loc[["25%", "50%", "75%"]]
# ─── ошибка ───
median_price = stats.loc["mean", "price"]
quartiles = stats.loc["25%":"75%", "quantity"]
# ─── ошибка ───
median_price = stats.loc["50%", "price"]
quartiles = stats.loc["25%":"75%", "price"]

# %% loc-numbers
orders.loc[2:4, ["product", "price"]]

# %% loc-quiz [quiz]
print(len(orders.loc[3:6]))

# %% tail-labels
last = orders.tail(3)
last

# %% tail-iloc
print(last.iloc[0, 6])
print(last.loc[2445, "product"])

# %% tail-loc [raises=KeyError]
last.loc[0]

# %% piece [exercise]
piece = orders.loc[10:14, ["date", "product", "price"]]
first_product = piece.iloc[0, 1]
# ─── заготовка ───
piece = ...
first_product = ...
# ─── проверка ───
def test_piece():
    "piece — строки с метками 10–14, три столбца"
    assert isinstance(piece, pd.DataFrame), f"piece — это {type(piece).__name__}, а нужна таблица"
    assert list(piece.columns) == ["date", "product", "price"], f"столбцы сейчас {list(piece.columns)}, а нужны date, product, price"
    assert len(piece) != 4, "в piece 4 строки: похоже, строки выбраны по позициям — там конец среза не входит, а у loc последняя метка входит"
    assert list(piece.index) == [10, 11, 12, 13, 14], f"метки строк сейчас {list(piece.index)}, а нужны 10, 11, 12, 13, 14"


def test_first():
    "first_product — товар в первой строке piece"
    assert isinstance(first_product, str), f"first_product — это {type(first_product).__name__}, а нужно название товара: одна ячейка piece"
    assert first_product != "2025-01-03", "это дата: позиции столбцов считаются с нуля"
    assert first_product == "Миндаль в шоколаде", f"first_product = {first_product!r}, а в первой строке piece другой товар"
# ─── другое решение ───
piece = orders[["date", "product", "price"]].iloc[10:15]
first_product = piece.loc[10, "product"]
# ─── ошибка ───
piece = orders.iloc[10:14][["date", "product", "price"]]
first_product = piece.iloc[0, 1]
# ─── ошибка ───
piece = orders.loc[10:14, ["date", "product", "price"]]
first_product = piece.iloc[0, 0]
