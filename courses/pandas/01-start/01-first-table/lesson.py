# Урок pd-first-table. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv")
orders

# %% load-error [raises=FileNotFoundError, platform]
pd.read_csv("shop_orders.csv")

# %% head
orders.head()

# %% tail
orders.tail(3)

# %% first-three [exercise]
top3 = orders.head(3)
# ─── заготовка ───
top3 = ...
# ─── проверка ───
def test_type():
    "top3 — таблица DataFrame"
    assert not callable(top3), "top3 — это сам метод head, а не таблица: вы забыли скобки — orders.head(3)"
    assert isinstance(top3, pd.DataFrame), f"top3 — это {type(top3).__name__}, а нужна таблица: вызовите метод head у orders"


def test_rows():
    "в top3 ровно три первые строки"
    assert isinstance(top3, pd.DataFrame), "top3 пока не таблица — сначала исправьте то, о чём говорит проверка выше"
    assert len(top3) == 3, f"в top3 {len(top3)} строк, а нужно 3 — передайте число строк в head"
    assert top3["order_id"].tolist() == [10001, 10001, 10002], "это не первые строки таблицы: первые показывает head, последние — tail"
# ─── другое решение ───
top3 = orders.head(n=3)
# ─── ошибка ───
top3 = orders.head
# ─── ошибка ───
top3 = orders.head()
# ─── ошибка ───
top3 = orders.tail(3)

# %% no-parens
orders.head

# %% shape
orders.shape

# %% len
print(orders.shape[0])
print(len(orders))

# %% size [exercise]
n_rows = orders.shape[0]
n_cols = orders.shape[1]
# ─── заготовка ───
n_rows = ...
n_cols = ...
# ─── проверка ───
def test_rows():
    "n_rows — число строк"
    assert not isinstance(n_rows, tuple), f"n_rows — это весь кортеж {n_rows}: возьмите из него первое число"
    assert n_rows != 9, "9 — это число столбцов; строки — первое число в orders.shape"
    assert n_rows == 2448, f"n_rows = {n_rows!r}, а строк в таблице 2448 — это первое число в orders.shape"


def test_cols():
    "n_cols — число столбцов"
    assert not isinstance(n_cols, tuple), f"n_cols — это весь кортеж {n_cols}: возьмите из него второе число"
    assert n_cols == 9, f"n_cols = {n_cols!r}, а столбцов 9 — это второе число в orders.shape"
# ─── другое решение ───
n_rows, n_cols = orders.shape
# ─── другое решение ───
n_rows = len(orders)
n_cols = len(orders.columns)
# ─── ошибка ───
n_rows = orders.shape[1]
n_cols = orders.shape[0]
# ─── ошибка ───
n_rows = orders.shape
n_cols = orders.shape

# %% columns
orders.columns

# %% names [exercise]
names = list(orders.columns)
# ─── заготовка ───
names = ...
# ─── проверка ───
def test_list():
    "names — список Python"
    assert isinstance(names, list), f"names — это {type(names).__name__}, а нужен обычный список: передайте orders.columns в list(...)"


def test_values():
    "в names все 9 названий по порядку"
    expected = ["order_id", "date", "customer_id", "city", "channel", "category", "product", "price", "quantity"]
    assert isinstance(names, list), "names пока не список — сначала исправьте то, о чём говорит проверка выше"
    assert names == expected, f"в names сейчас {names}"
# ─── другое решение ───
names = orders.columns.tolist()
# ─── другое решение ───
names = [name for name in orders.columns]
# ─── ошибка ───
names = orders.columns

# %% nrows
pd.read_csv("data/shop_orders.csv", nrows=4)

# %% sample [exercise]
sample = pd.read_csv("data/shop_orders.csv", nrows=100)
# ─── заготовка ───
sample = ...
# ─── проверка ───
def test_frame():
    "sample — таблица из 100 строк"
    assert isinstance(sample, pd.DataFrame), f"sample — это {type(sample).__name__}, а нужна таблица: pd.read_csv(...)"
    assert len(sample) == 100, f"в sample {len(sample)} строк, а нужно 100 — передайте read_csv параметр nrows"


def test_orders_kept():
    "таблица orders не изменилась"
    assert orders.shape == (2448, 9), (
        f"в orders теперь {len(orders)} строк: новую таблицу нужно сохранить в sample. Чтобы вернуть orders, выполните "
        "ячейку «Читаем CSV в таблицу» ещё раз или нажмите «Перезапустить»"
    )
# ─── другое решение ───
sample = orders.head(100)
# ─── ошибка ───
sample = pd.read_csv("data/shop_orders.csv")
