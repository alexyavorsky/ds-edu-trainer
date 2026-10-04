# Урок pd-inspect. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% info [platform]
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv")
orders.info()

# %% describe
orders.describe()

# %% describe-one
orders["price"].describe()

# %% spread [exercise]
quantity_stats = orders["quantity"].describe()
typical = quantity_stats["50%"]
# ─── заготовка ───
quantity_stats = ...
typical = ...
# ─── проверка ───
def test_stats():
    "quantity_stats — сводка describe по столбцу quantity"
    assert not isinstance(quantity_stats, pd.DataFrame), "quantity_stats — таблица: describe вызван у всей таблицы, а нужен у столбца quantity"
    assert isinstance(quantity_stats, pd.Series), f"quantity_stats — это {type(quantity_stats).__name__}, а нужна сводка describe по столбцу quantity"
    assert "50%" in quantity_stats.index, "в quantity_stats нет строки 50% — это не сводка describe"
    assert quantity_stats["max"] != 3200, "это сводка по ценам, а нужна по столбцу quantity"
    assert quantity_stats["max"] == 10, "это сводка не по столбцу quantity"


def test_typical():
    "typical — медиана количества"
    assert not isinstance(typical, pd.Series), "typical — целая сводка, а нужно одно число из неё: строка с меткой \"50%\""
    assert abs(typical - 2.128268) > 1e-5, "это среднее (mean), а нужна медиана — строка \"50%\""
    assert typical == 2, f"typical = {typical} — это не медиана количества"
# ─── другое решение ───
quantity_stats = orders.describe()["quantity"]
typical = quantity_stats.loc["50%"]
# ─── ошибка ───
quantity_stats = orders["quantity"].describe()
typical = quantity_stats["mean"]
# ─── ошибка ───
quantity_stats = orders["price"].describe()
typical = quantity_stats["50%"]

# %% counts
orders["city"].value_counts()

# %% counts-label
city_counts = orders["city"].value_counts()
print(city_counts["Казань"])
print(city_counts.index)

# %% channels [exercise]
channel_counts = orders["channel"].value_counts()
app_rows = channel_counts["приложение"]
# ─── заготовка ───
channel_counts = ...
app_rows = ...
# ─── проверка ───
def test_counts():
    "channel_counts — сколько строк у каждого канала"
    assert isinstance(channel_counts, pd.Series), f"channel_counts — это {type(channel_counts).__name__}, а нужен результат value_counts()"
    assert "сайт" in channel_counts.index, "в индексе нет каналов: value_counts нужно вызвать у столбца channel"
    assert len(channel_counts) == 3, f"в channel_counts {len(channel_counts)} строк, а каналов три"
    assert channel_counts["сайт"] == 1137, "числа не те: нужны подсчёты по столбцу channel"


def test_app():
    "app_rows — строк из приложения"
    assert not isinstance(app_rows, pd.Series), "app_rows — Series, а нужно одно число: значение по метке канала"
    assert app_rows != 1137, "1137 — это сайт; по метке \"приложение\" лежит другое число"
    assert app_rows == 684, f"app_rows = {app_rows} — это не число строк из приложения"
# ─── другое решение ───
channel_counts = orders.value_counts("channel")
app_rows = channel_counts.loc["приложение"]
# ─── ошибка ───
channel_counts = orders["channel"].value_counts()
app_rows = channel_counts["сайт"]
# ─── ошибка ───
channel_counts = orders["city"].value_counts()
app_rows = 684

# %% nunique
print(orders["city"].nunique())
print(orders["product"].nunique())

# %% nunique-all
orders.nunique()

# %% unique [platform]
orders["channel"].unique()

# %% unique-list
list(orders["channel"].unique())

# %% rows-quiz [quiz]
print(orders["order_id"].nunique() == len(orders))

# %% catalog [exercise]
n_days = orders["date"].nunique()
categories = sorted(orders["category"].unique())
# ─── заготовка ───
n_days = ...
categories = ...
# ─── проверка ───
def test_days():
    "n_days — в скольких днях года были продажи"
    assert not isinstance(n_days, pd.Series), "n_days — Series, а нужно одно число"
    assert n_days != 2448, "2448 — это число строк; нужны разные даты"
    assert n_days == 358, f"n_days = {n_days} — это не число разных дат"


def test_categories():
    "categories — список категорий по алфавиту"
    assert isinstance(categories, list), f"categories — это {type(categories).__name__}, а нужен список"
    assert len(categories) == 5, f"в categories {len(categories)} значений, а категорий 5: нужны разные значения столбца category"
    assert sorted(categories) == ["Аксессуары", "Кофе", "Посуда", "Сладости", "Чай"], f"в categories сейчас {categories}"
    assert categories == ["Аксессуары", "Кофе", "Посуда", "Сладости", "Чай"], f"категории не по алфавиту: {categories} — отсортируйте функцией sorted"
# ─── другое решение ───
n_days = len(orders["date"].unique())
categories = sorted(set(orders["category"]))
# ─── ошибка ───
n_days = len(orders["date"])
categories = sorted(orders["category"].unique())
# ─── ошибка ───
n_days = orders["date"].nunique()
categories = list(orders["category"].unique())

# %% popular [exercise]
product_counts = orders["product"].value_counts()
best_seller = product_counts.index[0]
best_rows = product_counts.max()
# ─── заготовка ───
product_counts = ...
best_seller = ...
best_rows = ...
# ─── проверка ───
def test_counts():
    "product_counts — сколько строк у каждого товара"
    assert isinstance(product_counts, pd.Series), f"product_counts — это {type(product_counts).__name__}, а нужен результат value_counts()"
    assert len(product_counts) == 20, f"в product_counts {len(product_counts)} строк, а товаров 20: нужен столбец product"


def test_best():
    "best_seller и best_rows — самый частый товар"
    assert isinstance(best_seller, str), f"best_seller — это {type(best_seller).__name__}, а нужно название товара: метка из индекса product_counts"
    assert best_seller == "Колумбия 250 г", f"best_seller = {best_seller!r}: value_counts ставит самый частый товар первым"
    assert best_rows == 218, f"best_rows = {best_rows!r} — это не число строк самого частого товара"
# ─── другое решение ───
product_counts = orders["product"].value_counts()
best_seller = list(product_counts.index)[0]
best_rows = product_counts[best_seller]
# ─── ошибка ───
product_counts = orders["product"].value_counts()
best_seller = product_counts[0:1]
best_rows = product_counts.max()
