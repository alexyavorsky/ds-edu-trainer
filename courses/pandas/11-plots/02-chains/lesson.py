# Урок pd-chains. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% steps
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv", parse_dates=["date"])
df = orders.copy()
df["revenue"] = df["price"] * df["quantity"]
df2 = df[df["category"] == "Кофе"]
df3 = df2.groupby("product")["revenue"].sum()
df4 = df3.sort_values(ascending=False)
df4.head(3)

# %% chain
top_coffee = (
    orders
    .assign(revenue=orders["price"] * orders["quantity"])
    .query("category == 'Кофе'")
    .groupby("product")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(3)
)
top_coffee

# %% cities [exercise]
top_cities = (
    orders
    .assign(revenue=orders["price"] * orders["quantity"])
    .groupby("city")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(3)
)
# ─── заготовка ───
top_cities = (
    orders
    # допишите шаги цепочки: каждый с новой строки, начиная с точки
)
# ─── проверка ───
def test_top():
    "top_cities — три города с наибольшей выручкой"
    assert top_cities is not ..., "top_cities пока равна ... — замените многоточие цепочкой методов"
    assert isinstance(top_cities, pd.Series), f"top_cities — это {type(top_cities).__name__}, а нужен Series: цепочка должна заканчиваться суммой по городам, сортировкой и head(3)"
    assert len(top_cities) == 3, f"в top_cities {len(top_cities)} значений, а нужно три: .head(3) в конце цепочки"
    assert list(top_cities.index) == ["Москва", "Санкт-Петербург", "Казань"], f"города сейчас {list(top_cities.index)}, а три лучших — Москва, Санкт-Петербург, Казань: сортировка по убыванию"
    assert top_cities.tolist() == [1310110, 803720, 440150], "значения не те: выручка — цена × количество, сумма по городу"
# ─── другое решение ───
top_cities = (
    orders
    .assign(revenue=lambda d: d["price"] * d["quantity"])
    .groupby("city")["revenue"]
    .sum()
    .nlargest(3)
)
# ─── ошибка ───
top_cities = (
    orders
    .assign(revenue=orders["price"] * orders["quantity"])
    .groupby("city")["revenue"]
    .sum()
    .sort_values()
    .head(3)
)
# ─── ошибка ───
top_cities = (
    orders
    .assign(revenue=orders["price"] * orders["quantity"])
    .groupby("city")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

# %% lambda-need [raises=KeyError]
(
    orders
    .query("category == 'Чай'")
    .assign(revenue=orders["price"] * orders["quantity"])
    .assign(share=orders["revenue"] / orders["revenue"].sum())
    .head(3)
)

# %% lambda
(
    orders
    .query("category == 'Чай'")
    .assign(revenue=lambda d: d["price"] * d["quantity"])
    .assign(share=lambda d: d["revenue"] / d["revenue"].sum())
    [["product", "revenue", "share"]]
    .head(3)
)

# %% lambda-quiz [quiz]
t = pd.DataFrame({"x": [1, 2, 3, 4]})
print(t.query("x > 2").assign(y=lambda d: d["x"] * 10)["y"].sum())

# %% app [exercise]
app_bulk = (
    orders
    .query("channel == 'приложение' and quantity >= 3")
    .assign(revenue=lambda d: d["price"] * d["quantity"])
    .groupby("category")["revenue"]
    .sum()
    .sort_values(ascending=False)
)
# ─── заготовка ───
app_bulk = (
    orders
    # допишите шаги цепочки: каждый с новой строки, начиная с точки
)
# ─── проверка ───
def test_app():
    "app_bulk — выручка по категориям для покупок в приложении от 3 штук"
    assert app_bulk is not ..., "app_bulk пока равна ... — замените многоточие цепочкой методов"
    assert isinstance(app_bulk, pd.Series), f"app_bulk — это {type(app_bulk).__name__}, а нужен Series: сумма revenue по категориям"
    assert len(app_bulk) == 5 and "Кофе" in app_bulk.index, "в app_bulk должны быть пять категорий: .groupby(\"category\")[\"revenue\"].sum()"
    assert app_bulk["Кофе"] != 540520, "посчитаны все покупки приложения, а нужны только строки, где количество не меньше 3: добавьте условие в query"
    assert app_bulk["Кофе"] != 1051870, "посчитаны все каналы, а нужно только приложение: условие channel == 'приложение' в query"
    assert app_bulk["Кофе"] == 279610 and app_bulk["Аксессуары"] == 1440, "значения не те: кофе — 279610, аксессуары — 1440"
    assert app_bulk.tolist() == sorted(app_bulk.tolist(), reverse=True), "отсортируйте по убыванию: .sort_values(ascending=False)"
# ─── другое решение ───
app_bulk = (
    orders[(orders["channel"] == "приложение") & (orders["quantity"] >= 3)]
    .assign(revenue=lambda d: d["price"] * d["quantity"])
    .groupby("category")["revenue"]
    .sum()
    .sort_values(ascending=False)
)
# ─── ошибка ───
app_bulk = (
    orders
    .query("channel == 'приложение'")
    .assign(revenue=lambda d: d["price"] * d["quantity"])
    .groupby("category")["revenue"]
    .sum()
    .sort_values(ascending=False)
)
# ─── ошибка ───
app_bulk = (
    orders
    .query("channel == 'приложение' and quantity >= 3")
    .assign(revenue=lambda d: d["price"] * d["quantity"])
    .groupby("category")["revenue"]
    .sum()
)

# %% pipe
def add_revenue(table):
    return table.assign(revenue=table["price"] * table["quantity"])


def top_rows(table, column, n):
    return table.nlargest(n, column)


(
    orders
    .pipe(add_revenue)
    .pipe(top_rows, "revenue", 3)
    [["date", "product", "revenue"]]
)

# %% months [exercise]
def add_month(table):
    return table.assign(month=table["date"].dt.month)


by_month = (
    orders
    .pipe(add_revenue)
    .pipe(add_month)
    .groupby("month")["revenue"]
    .sum()
)
# ─── заготовка ───
def add_month(table):
    return ...


by_month = (
    orders
    # допишите шаги цепочки: каждый с новой строки, начиная с точки
)
# ─── проверка ───
def test_function():
    "add_month(table) возвращает таблицу со столбцом month"
    result = add_month(orders)
    assert result is not ..., "функция add_month пока возвращает ... — верните таблицу с новым столбцом: table.assign(month=...)"
    assert isinstance(result, pd.DataFrame), f"add_month вернула {type(result).__name__}, а должна возвращать таблицу"
    assert "month" in result.columns, "в таблице, которую возвращает add_month, нет столбца month"
    assert result["month"].iloc[0] == 1 and result["month"].iloc[-1] == 12, "month — номер месяца из столбца date: table[\"date\"].dt.month"
    assert "month" not in orders.columns, "функция изменила исходную таблицу orders: возвращайте новую таблицу через assign, а не записывайте столбец в table"


def test_by_month():
    "by_month — выручка по месяцам"
    assert by_month is not ..., "by_month пока равна ... — замените многоточие цепочкой методов"
    assert isinstance(by_month, pd.Series) and len(by_month) == 12, "by_month — Series из 12 значений: .groupby(\"month\")[\"revenue\"].sum()"
    assert list(by_month.index) == list(range(1, 13)), "в индексе by_month должны быть номера месяцев 1–12"
    assert by_month.iloc[0] == 318940 and by_month.sum() == 3301420, "значения не те: январь — 318940, весь год — 3301420"
# ─── другое решение ───
def add_month(table):
    result = table.copy()
    result["month"] = result["date"].dt.month
    return result


by_month = orders.pipe(add_month).pipe(add_revenue).groupby("month")["revenue"].sum()
# ─── ошибка ───
def add_month(table):
    return table.assign(month=table["date"].dt.day)


by_month = (
    orders
    .pipe(add_revenue)
    .pipe(add_month)
    .groupby("month")["revenue"]
    .sum()
)

# %% loop
total = 0
for label, row in orders.head(3).iterrows():
    revenue = row["price"] * row["quantity"]
    print(label, row["product"], revenue)
    total = total + revenue
print(total)

# %% loop-full
total = 0
for label, row in orders.iterrows():
    revenue = row["price"] * row["quantity"]
    if row["quantity"] >= 3:
        revenue = revenue * 0.9
    total = total + revenue
print(round(total))

# %% vector [exercise]
import numpy as np

discounted = (
    orders
    .assign(revenue=lambda d: d["price"] * d["quantity"])
    .assign(to_pay=lambda d: np.where(d["quantity"] >= 3, d["revenue"] * 0.9, d["revenue"]))
)
total_fast = discounted["to_pay"].sum()
# ─── заготовка ───
import numpy as np

discounted = (
    orders
    # допишите шаги цепочки: каждый с новой строки, начиная с точки
)
total_fast = ...
# ─── проверка ───
def test_discounted():
    "discounted — таблица со столбцами revenue и to_pay"
    assert discounted is not ..., "discounted пока равна ... — замените многоточие цепочкой методов"
    assert isinstance(discounted, pd.DataFrame), f"discounted — это {type(discounted).__name__}, а нужна таблица"
    assert "revenue" in discounted.columns and "to_pay" in discounted.columns, "в discounted нужны столбцы revenue и to_pay: два assign"
    assert len(discounted) == 2448, "в discounted должны остаться все 2448 строк"
    assert abs(discounted.loc[0, "to_pay"] - 6400) < 1e-9, "в первой строке 2 штуки — скидки нет, to_pay равно revenue: 6400"
    assert abs(discounted.loc[9, "to_pay"] - discounted.loc[9, "revenue"] * (0.9 if discounted.loc[9, "quantity"] >= 3 else 1)) < 1e-9, "скидка 10 % — только там, где количество не меньше 3: np.where(условие, revenue * 0.9, revenue)"


def test_total():
    "total_fast — та же сумма, что у цикла"
    assert abs(total_fast - 3301420) > 1, "скидка не применена: сумма равна выручке без скидки"
    assert abs(total_fast - 3301420 * 0.9) > 1, "скидка применена ко всем строкам, а нужна только там, где количество не меньше 3"
    assert abs(total_fast - 3150009.0) < 1e-3, f"total_fast = {total_fast!r}, а цикл дал 3150009"
# ─── другое решение ───
import numpy as np

discounted = orders.assign(revenue=orders["price"] * orders["quantity"])
discounted["to_pay"] = discounted["revenue"]
discounted.loc[discounted["quantity"] >= 3, "to_pay"] = discounted["revenue"] * 0.9
total_fast = discounted["to_pay"].sum()
# ─── ошибка ───
import numpy as np

discounted = (
    orders
    .assign(revenue=lambda d: d["price"] * d["quantity"])
    .assign(to_pay=lambda d: d["revenue"] * 0.9)
)
total_fast = discounted["to_pay"].sum()
