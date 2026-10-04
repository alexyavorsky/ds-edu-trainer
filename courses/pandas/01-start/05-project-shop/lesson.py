# Урок pd-project-shop. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load [exercise]
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv")
n_lines = len(orders)
# ─── заготовка ───
import pandas as pd

orders = ...
n_lines = ...
# ─── проверка ───
def test_orders():
    "orders — таблица продаж"
    assert isinstance(orders, pd.DataFrame), f"orders — это {type(orders).__name__}, а нужна таблица"
    assert orders.shape == (2448, 9), f"у orders размер {orders.shape}, а в файле 2448 строк и 9 столбцов — читайте файл целиком"


def test_lines():
    "n_lines — число строк"
    assert not isinstance(n_lines, tuple), f"n_lines — кортеж {n_lines}, а нужно одно число"
    assert n_lines == 2448, f"n_lines = {n_lines!r} — это не число строк orders"
# ─── другое решение ───
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv")
n_lines = orders.shape[0]
# ─── ошибка ───
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv", nrows=100)
n_lines = len(orders)
# ─── ошибка ───
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv")
n_lines = orders.shape

# %% look
orders.tail(4)

# %% buyers [exercise]
n_orders = orders["order_id"].nunique()
n_customers = orders["customer_id"].nunique()
lines_per_order = n_lines / n_orders
orders_per_customer = n_orders / n_customers
# ─── заготовка ───
n_orders = ...
n_customers = ...
lines_per_order = ...
orders_per_customer = ...
# ─── проверка ───
def test_counts():
    "n_orders и n_customers — сколько заказов и покупателей"
    assert n_orders != 2448, "2448 — число строк, а заказ может занимать несколько строк: считайте разные номера заказов"
    assert n_orders == 1576, f"n_orders = {n_orders!r} — это не число разных заказов"
    assert n_customers != 2448, "2448 — число строк; покупателей считают по разным customer_id"
    assert n_customers == 213, f"n_customers = {n_customers!r} — это не число разных покупателей"


def test_ratios():
    "lines_per_order и orders_per_customer — средние"
    assert abs(lines_per_order - 1576 / 2448) > 1e-9, "дробь перевёрнута: строк на заказ — это строки, делённые на заказы"
    assert abs(lines_per_order - 2448 / 1576) < 1e-9, f"lines_per_order = {lines_per_order!r} — это не среднее число строк на заказ"
    assert abs(orders_per_customer - 1576 / 213) < 1e-9, f"orders_per_customer = {orders_per_customer!r} — это не среднее число заказов на покупателя"
# ─── другое решение ───
n_orders = len(orders["order_id"].unique())
n_customers = len(orders["customer_id"].unique())
lines_per_order = len(orders) / n_orders
orders_per_customer = n_orders / n_customers
# ─── ошибка ───
n_orders = len(orders["order_id"])
n_customers = len(orders["customer_id"])
lines_per_order = n_lines / n_orders
orders_per_customer = n_orders / n_customers
# ─── ошибка ───
n_orders = orders["order_id"].nunique()
n_customers = orders["customer_id"].nunique()
lines_per_order = n_orders / n_lines
orders_per_customer = n_orders / n_customers

# %% geo [exercise]
city_counts = orders["city"].value_counts()
n_cities = len(city_counts)
moscow_share = city_counts["Москва"] / n_lines
# ─── заготовка ───
city_counts = ...
n_cities = ...
moscow_share = ...
# ─── проверка ───
def test_counts():
    "city_counts — строк по городам, n_cities — сколько городов"
    assert isinstance(city_counts, pd.Series), f"city_counts — это {type(city_counts).__name__}, а нужен результат value_counts()"
    assert "Москва" in city_counts.index, "в индексе city_counts нет городов: value_counts нужно вызвать у столбца city"
    assert city_counts["Москва"] == 948, "числа не те: нужны подсчёты по столбцу city"
    assert n_cities == 5, f"n_cities = {n_cities!r} — это не число городов"


def test_share():
    "moscow_share — доля Москвы в строках"
    assert not isinstance(moscow_share, pd.Series), "moscow_share — Series, а нужно одно число"
    assert moscow_share != 948, "948 — число строк; доля — это число строк Москвы, делённое на число всех строк"
    assert abs(moscow_share - 38.7255) > 1e-3, "доля нужна числом от 0 до 1, а не в процентах: не умножайте на 100"
    assert abs(moscow_share - 948 / 2448) < 1e-9, f"moscow_share = {moscow_share!r} — это не доля строк Москвы"
# ─── другое решение ───
city_counts = orders["city"].value_counts()
n_cities = orders["city"].nunique()
moscow_share = (city_counts / len(orders))["Москва"]
# ─── ошибка ───
city_counts = orders["city"].value_counts()
n_cities = len(city_counts)
moscow_share = city_counts["Москва"]
# ─── ошибка ───
city_counts = orders["city"].value_counts()
n_cities = len(city_counts)
moscow_share = city_counts["Москва"] / n_lines * 100

# %% money [exercise]
revenue = orders["price"] * orders["quantity"]
total = revenue.sum()
avg_check = total / n_orders
# ─── заготовка ───
revenue = ...
total = ...
avg_check = ...
# ─── проверка ───
def test_revenue():
    "revenue — выручка каждой строки, total — за год"
    assert isinstance(revenue, pd.Series), f"revenue — это {type(revenue).__name__}, а нужен столбец: цена × количество"
    assert len(revenue) == 2448, f"в revenue {len(revenue)} значений, а строк 2448"
    assert revenue[0] == 6400, f"выручка первой строки — {revenue[0]}: выручка строки — цена × количество"
    assert total != 1685990, "это сумма цен без учёта количества"
    assert total == 3301420, f"total = {total!r} — это не сумма выручки всех строк"


def test_check():
    "avg_check — средний чек"
    assert abs(avg_check - 3301420 / 2448) > 1e-6, "это выручка на строку: чек — это заказ"
    assert abs(avg_check - 3301420 / 1576) < 1e-6, f"avg_check = {avg_check!r} — это не средний чек"
# ─── другое решение ───
revenue = orders["quantity"] * orders["price"]
total = sum(revenue)
avg_check = revenue.sum() / orders["order_id"].nunique()
# ─── ошибка ───
revenue = orders["price"] * orders["quantity"]
total = revenue.sum()
avg_check = revenue.mean()
# ─── ошибка ───
revenue = orders["price"] * orders["quantity"]
total = orders["price"].sum()
avg_check = total / n_orders

# %% mix [exercise]
category_share = orders["category"].value_counts() / n_lines
top_category = category_share.index[0]
top_share = category_share.max()
# ─── заготовка ───
category_share = ...
top_category = ...
top_share = ...
# ─── проверка ───
def test_share():
    "category_share — доля каждой категории в строках"
    assert isinstance(category_share, pd.Series), f"category_share — это {type(category_share).__name__}, а нужен Series"
    assert len(category_share) == 5 and "Чай" in category_share.index, "в category_share должны быть пять категорий: value_counts нужен у столбца category"
    assert category_share.max() <= 1, "в category_share числа строк, а нужны доли: разделите на число всех строк"
    assert abs(category_share.sum() - 1) < 1e-9, f"сумма долей — {category_share.sum()}, а должна быть 1: делите на число всех строк"
    assert abs(category_share["Чай"] - 682 / 2448) < 1e-9, "доли не те: нужны строки каждой категории, делённые на число всех строк"


def test_top():
    "top_category и top_share — самая частая категория"
    assert isinstance(top_category, str), f"top_category — это {type(top_category).__name__}, а нужно название: первая метка индекса"
    assert top_category == "Кофе", f"top_category = {top_category!r}: value_counts ставит самую частую категорию первой"
    assert abs(top_share - 975 / 2448) < 1e-9, f"top_share = {top_share!r} — это не доля самой частой категории"
# ─── другое решение ───
counts = orders["category"].value_counts()
category_share = counts / counts.sum()
top_category = list(category_share.index)[0]
top_share = category_share[top_category]
# ─── ошибка ───
category_share = orders["category"].value_counts()
top_category = category_share.index[0]
top_share = category_share.max()

# %% summary
print("строк:", n_lines, "· заказов:", n_orders, "· покупателей:", n_customers)
print("выручка:", total, "₽ · средний чек:", round(avg_check), "₽")
print("городов:", n_cities, "· доля Москвы:", round(moscow_share * 100, 1), "%")
print("главная категория:", top_category, "—", round(top_share * 100, 1), "% строк")
