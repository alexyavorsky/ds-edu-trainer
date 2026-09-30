# Урок pd-sort. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% sort
import pandas as pd

products = pd.read_csv("data/products.csv")
products.sort_values("price").head()

# %% desc
products.sort_values("price", ascending=False).head(4)

# %% kept
products.head(3)

# %% cheap [exercise]
by_cost = products.sort_values("cost")
cheapest = by_cost.iloc[0]["name"]
# ─── заготовка ───
by_cost = ...
cheapest = ...
# ─── проверка ───
def test_sorted():
    "by_cost — товары по возрастанию себестоимости"
    assert isinstance(by_cost, pd.DataFrame), f"by_cost — это {type(by_cost).__name__}, а нужна таблица: products.sort_values(...)"
    assert len(by_cost) == 20 and by_cost.shape[1] == 5, "в by_cost должны остаться все 20 строк и 5 столбцов"
    costs = by_cost["cost"].tolist()
    assert costs != sorted(costs, reverse=True), "сортировка по убыванию, а нужна по возрастанию: уберите ascending=False"
    assert costs == sorted(costs), "строки не отсортированы по cost: products.sort_values(\"cost\")"


def test_cheapest():
    "cheapest — название товара с наименьшей себестоимостью"
    assert isinstance(cheapest, str), f"cheapest — это {type(cheapest).__name__}, а нужно название товара: одно значение из столбца name"
    assert cheapest != "Эспрессо-смесь 1 кг", "это товар с меткой 0, а не первая строка: после сортировки первая строка — iloc[0], а не loc[0]"
    assert cheapest == "Печенье овсяное", f"cheapest = {cheapest!r}, а наименьшая себестоимость у другого товара"
# ─── другое решение ───
by_cost = products.sort_values(by="cost", ascending=True)
cheapest = by_cost["name"].iloc[0]
# ─── ошибка ───
by_cost = products.sort_values("cost")
cheapest = by_cost.loc[0, "name"]
# ─── ошибка ───
by_cost = products.sort_values("cost", ascending=False)
cheapest = by_cost.iloc[0]["name"]
# ─── ошибка ───
by_cost = products
cheapest = by_cost.iloc[0]["name"]

# %% two-keys
products.sort_values(["category", "price"]).head(7)

# %% two-orders
products.sort_values(["category", "price"], ascending=[True, False]).head(7)

# %% shelves [exercise]
shelves = products.sort_values(["category", "name"], ascending=[False, True])
# ─── заготовка ───
shelves = ...
# ─── проверка ───
def test_shelves():
    "shelves — категории от Я к А, внутри — названия от А к Я"
    assert isinstance(shelves, pd.DataFrame) and len(shelves) == 20, "shelves — все 20 товаров, отсортированные sort_values"
    cats = shelves["category"].tolist()
    assert cats[0] != "Аксессуары", "категории идут от А к Я, а нужно наоборот: для первого ключа ascending — False"
    assert cats == sorted(cats, reverse=True), "категории должны идти в обратном алфавитном порядке: первый ключ — category, для него ascending False"
    tea = shelves.loc[shelves["category"] == "Чай", "name"].tolist()
    assert tea != sorted(tea, reverse=True), "названия внутри категории идут от Я к А, а нужно от А к Я: ascending=[False, True]"
    assert tea == sorted(tea), "внутри категории товары должны идти по названию от А к Я: второй ключ — name"
    assert shelves.iloc[0]["name"] == "Зелёный чай 100 г", "первой строкой должен быть зелёный чай"
# ─── другое решение ───
shelves = products.sort_values("name").sort_values("category", ascending=False, kind="stable")
# ─── ошибка ───
shelves = products.sort_values(["category", "name"])
# ─── ошибка ───
shelves = products.sort_values(["category", "name"], ascending=False)
# ─── ошибка ───
shelves = products.sort_values(["name", "category"], ascending=[True, False])

# %% nlargest
products.nlargest(3, "price")

# %% nsmallest
products.nsmallest(3, "price")[["name", "price"]]

# %% sort-quiz [quiz]
t = pd.DataFrame({"x": [3, 1, 2]})
t.sort_values("x")
print(t["x"].tolist())

# %% top [exercise]
orders = pd.read_csv("data/shop_orders.csv")
orders["revenue"] = orders["price"] * orders["quantity"]
top5 = orders.nlargest(5, "revenue")[["date", "product", "quantity", "revenue"]]
# ─── заготовка ───
orders = pd.read_csv("data/shop_orders.csv")
orders["revenue"] = orders["price"] * orders["quantity"]
top5 = ...
# ─── проверка ───
def test_top():
    "top5 — пять строк с наибольшей выручкой"
    assert isinstance(top5, pd.DataFrame), f"top5 — это {type(top5).__name__}, а нужна таблица"
    assert list(top5.columns) == ["date", "product", "quantity", "revenue"], f"столбцы сейчас {list(top5.columns)}, а нужны date, product, quantity, revenue"
    assert len(top5) == 5, f"в top5 {len(top5)} строк, а нужно 5"
    assert top5["revenue"].tolist() != [150, 150, 150, 150, 150], "это пять самых маленьких значений: нужен nlargest, а не nsmallest"
    assert top5["revenue"].tolist() == [9030, 9030, 9030, 8700, 8700], f"выручка в top5 сейчас {top5['revenue'].tolist()}, а пять наибольших — 9030, 9030, 9030, 8700, 8700"
# ─── другое решение ───
orders = pd.read_csv("data/shop_orders.csv")
orders["revenue"] = orders["price"] * orders["quantity"]
top5 = orders.sort_values("revenue", ascending=False).head(5)[["date", "product", "quantity", "revenue"]]
# ─── ошибка ───
orders = pd.read_csv("data/shop_orders.csv")
orders["revenue"] = orders["price"] * orders["quantity"]
top5 = orders.nsmallest(5, "revenue")[["date", "product", "quantity", "revenue"]]
# ─── ошибка ───
orders = pd.read_csv("data/shop_orders.csv")
orders["revenue"] = orders["price"] * orders["quantity"]
top5 = orders.nlargest(5, "price")[["date", "product", "quantity", "revenue"]]

# %% series-sort
counts = orders["quantity"].value_counts()
counts.head(4)

# %% sort-index
counts.sort_index().head(4)

# %% series-values
orders["city"].value_counts().sort_values().head(3)

# %% alphabet [exercise]
city_counts = orders["city"].value_counts().sort_index()
first_city = city_counts.index[0]
# ─── заготовка ───
city_counts = ...
first_city = ...
# ─── проверка ───
def test_counts():
    "city_counts — строк по городам, города по алфавиту"
    assert isinstance(city_counts, pd.Series), f"city_counts — это {type(city_counts).__name__}, а нужен Series: value_counts() и сортировка по индексу"
    assert len(city_counts) == 5 and city_counts.sum() == 2448, "в city_counts должны быть все пять городов: orders[\"city\"].value_counts()"
    assert list(city_counts.index) != ["Москва", "Санкт-Петербург", "Казань", "Екатеринбург", "Новосибирск"], "города идут по убыванию числа строк, а нужны по алфавиту: добавьте sort_index()"
    assert list(city_counts.index) == ["Екатеринбург", "Казань", "Москва", "Новосибирск", "Санкт-Петербург"], f"порядок городов сейчас {list(city_counts.index)}, а нужен алфавитный"


def test_first():
    "first_city — первый город по алфавиту"
    assert first_city == "Екатеринбург", f"first_city = {first_city!r}, а первый по алфавиту — Екатеринбург: city_counts.index[0]"
# ─── другое решение ───
city_counts = orders.sort_values("city")["city"].value_counts(sort=False)
first_city = min(orders["city"])
# ─── ошибка ───
city_counts = orders["city"].value_counts()
first_city = city_counts.index[0]
# ─── ошибка ───
city_counts = orders["city"].value_counts().sort_values()
first_city = city_counts.index[0]
