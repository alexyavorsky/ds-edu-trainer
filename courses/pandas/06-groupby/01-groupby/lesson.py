# Урок pd-groupby. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% by-hand
import pandas as pd

sales = pd.DataFrame({
    "city": ["Омск", "Тула", "Омск", "Пермь", "Тула", "Омск"],
    "cups": [30, 12, 18, 25, 20, 12],
})
print(sales.loc[sales["city"] == "Омск", "cups"].sum())
print(sales.loc[sales["city"] == "Пермь", "cups"].sum())
print(sales.loc[sales["city"] == "Тула", "cups"].sum())

# %% first
sales.groupby("city")["cups"].sum()

# %% result-type
totals = sales.groupby("city")["cups"].sum()
print(type(totals).__name__)
print(totals.index.tolist())
print(totals["Тула"])

# %% real
orders = pd.read_csv("data/shop_orders.csv")
orders["revenue"] = orders["price"] * orders["quantity"]
orders.groupby("city")["revenue"].sum()

# %% check-total
by_city = orders.groupby("city")["revenue"].sum()
print(by_city.sum())
print(orders["revenue"].sum())

# %% category [exercise]
by_category = orders.groupby("category")["revenue"].sum()
top_category = by_category.idxmax()
# ─── заготовка ───
by_category = ...
top_category = ...
# ─── проверка ───
def test_by_category():
    "by_category — выручка по категориям"
    assert isinstance(by_category, pd.Series), f"by_category — это {type(by_category).__name__}, а нужен Series: orders.groupby(\"category\")[\"revenue\"].sum()"
    assert sorted(by_category.index) == ["Аксессуары", "Кофе", "Посуда", "Сладости", "Чай"], f"в индексе сейчас {list(by_category.index)}, а нужны пять категорий: groupby(\"category\")"
    assert by_category["Кофе"] != 975, "это число строк, а нужна сумма выручки: [\"revenue\"].sum()"
    assert by_category["Кофе"] != 2138, "это сумма количества, а нужна выручка: после groupby выберите столбец revenue"
    assert by_category["Кофе"] == 1914440 and by_category.sum() == 3301420, "суммы не те: orders.groupby(\"category\")[\"revenue\"].sum()"


def test_top():
    "top_category — категория с наибольшей выручкой"
    assert isinstance(top_category, str), f"top_category — это {type(top_category).__name__}, а нужно название категории: by_category.idxmax()"
    assert top_category == "Кофе", f"top_category = {top_category!r}, а больше всего выручки у другой категории"
# ─── другое решение ───
by_category = orders.groupby("category")["revenue"].sum().sort_values(ascending=False)
top_category = by_category.index[0]
# ─── ошибка ───
by_category = orders.groupby("category")["quantity"].sum()
top_category = by_category.idxmax()
# ─── ошибка ───
by_category = orders.groupby("category")["revenue"].sum()
top_category = by_category.max()

# %% other-aggs
print(orders.groupby("category")["price"].max())
print(orders.groupby("channel")["revenue"].mean().round(1))

# %% nunique
orders.groupby("channel")["order_id"].nunique()

# %% rows-quiz [quiz]
print(len(orders.groupby("channel")["price"].max()))

# %% channels [exercise]
channel_revenue = orders.groupby("channel")["revenue"].sum()
channel_orders = orders.groupby("channel")["order_id"].nunique()
channel_check = channel_revenue / channel_orders
# ─── заготовка ───
channel_revenue = ...
channel_orders = ...
channel_check = ...
# ─── проверка ───
def test_parts():
    "channel_revenue и channel_orders — выручка и число заказов по каналам"
    assert isinstance(channel_revenue, pd.Series) and sorted(channel_revenue.index) == ["маркетплейс", "приложение", "сайт"], "channel_revenue — Series с тремя каналами в индексе: orders.groupby(\"channel\")[\"revenue\"].sum()"
    assert channel_revenue["сайт"] == 1522920, "выручка не та: сумма столбца revenue по каналам"
    assert isinstance(channel_orders, pd.Series) and sorted(channel_orders.index) == ["маркетплейс", "приложение", "сайт"], "channel_orders — Series с тремя каналами в индексе"
    assert channel_orders["сайт"] != 1137, "1137 — число строк сайта, а заказ может занимать несколько строк: число разных order_id — nunique()"
    assert channel_orders["сайт"] == 715, "число заказов не то: orders.groupby(\"channel\")[\"order_id\"].nunique()"


def test_check():
    "channel_check — средний чек по каналам"
    assert isinstance(channel_check, pd.Series), f"channel_check — это {type(channel_check).__name__}, а нужен Series: выручка, делённая на число заказов"
    assert abs(channel_check["сайт"] - 1522920 / 1137) > 1e-6, "выручка разделена на число строк — это выручка на строку. Средний чек — на число заказов"
    assert abs(channel_check["сайт"] - 1522920 / 715) < 1e-6 and abs(channel_check["маркетплейс"] - 876070 / 407) < 1e-6, "средний чек — channel_revenue / channel_orders"
# ─── другое решение ───
groups = orders.groupby("channel")
channel_revenue = groups["revenue"].sum()
channel_orders = groups["order_id"].nunique()
channel_check = channel_revenue / channel_orders
# ─── ошибка ───
channel_revenue = orders.groupby("channel")["revenue"].sum()
channel_orders = orders.groupby("channel")["order_id"].count()
channel_check = channel_revenue / channel_orders
# ─── ошибка ───
channel_revenue = orders.groupby("channel")["revenue"].sum()
channel_orders = orders.groupby("channel")["order_id"].nunique()
channel_check = orders.groupby("channel")["revenue"].mean()

# %% two-columns
orders.groupby("city")[["revenue", "quantity"]].sum()

# %% no-column [raises=TypeError]
orders.groupby("city").mean()

# %% size-count
weather = pd.read_csv("data/weather.csv")
print(weather.groupby("city").size())
print(weather.groupby("city")["temp_max"].count())

# %% weather [exercise]
city_temp = weather.groupby("city")["temp_max"].mean()
warmest = city_temp.idxmax()
wind_gaps = weather.groupby("city").size() - weather.groupby("city")["wind_ms"].count()
# ─── заготовка ───
city_temp = ...
warmest = ...
wind_gaps = ...
# ─── проверка ───
def test_temp():
    "city_temp — средний дневной максимум по городам"
    assert isinstance(city_temp, pd.Series), f"city_temp — это {type(city_temp).__name__}, а нужен Series: weather.groupby(\"city\")[\"temp_max\"].mean()"
    assert len(city_temp) == 5 and "Сочи" in city_temp.index, "в индексе city_temp должны быть пять городов: groupby(\"city\")"
    assert abs(city_temp["Сочи"] - 31.9) > 1e-9, "в city_temp — наибольшая температура, а нужна средняя: mean()"
    assert abs(city_temp["Сочи"] - 17.724932) < 1e-5 and abs(city_temp["Казань"] - 8.295041) < 1e-5, "средние не те: столбец temp_max, метод mean()"
    assert warmest == "Сочи", f"warmest = {warmest!r}, а самый тёплый город — city_temp.idxmax()"


def test_gaps():
    "wind_gaps — сколько пропусков ветра в каждом городе"
    assert isinstance(wind_gaps, pd.Series), f"wind_gaps — это {type(wind_gaps).__name__}, а нужен Series: размер группы минус число непустых значений"
    assert len(wind_gaps) == 5, "в wind_gaps должны быть пять городов"
    assert wind_gaps.sum() != 0, "получились нули: из size() нужно вычесть count() столбца wind_ms — count считает только непустые значения"
    assert wind_gaps.sum() == 4 and wind_gaps["Москва"] == 0 and wind_gaps["Казань"] == 1, "числа не те: weather.groupby(\"city\").size() − weather.groupby(\"city\")[\"wind_ms\"].count()"
# ─── другое решение ───
city_temp = weather.groupby("city")["temp_max"].sum() / weather.groupby("city")["temp_max"].count()
warmest = city_temp.sort_values().index[-1]
wind_gaps = weather["wind_ms"].isna().groupby(weather["city"]).sum()
# ─── ошибка ───
city_temp = weather.groupby("city")["temp_max"].max()
warmest = city_temp.idxmax()
wind_gaps = weather.groupby("city").size() - weather.groupby("city")["wind_ms"].count()
# ─── ошибка ───
city_temp = weather.groupby("city")["temp_max"].mean()
warmest = city_temp.idxmax()
wind_gaps = weather.groupby("city").size() - weather.groupby("city")["wind_ms"].size()

# %% sorted
orders.groupby("product")["revenue"].sum().sort_values(ascending=False).head(5)

# %% leaders [exercise]
product_qty = orders.groupby("product")["quantity"].sum()
top3 = product_qty.nlargest(3)
customer_revenue = orders.groupby("customer_id")["revenue"].sum()
best_customer = customer_revenue.idxmax()
# ─── заготовка ───
product_qty = ...
top3 = ...
customer_revenue = ...
best_customer = ...
# ─── проверка ───
def test_products():
    "product_qty и top3 — продано штук по товарам и три лидера"
    assert isinstance(product_qty, pd.Series) and len(product_qty) == 20, "product_qty — Series с 20 товарами в индексе: orders.groupby(\"product\")[\"quantity\"].sum()"
    assert product_qty.sum() == 5210, "суммы не те: складывать нужно столбец quantity"
    assert isinstance(top3, pd.Series) and len(top3) == 3, "top3 — три наибольших значения product_qty: nlargest(3)"
    assert top3.tolist() == sorted(product_qty.tolist(), reverse=True)[:3], "top3 — три товара с наибольшим числом проданных штук, от большего к меньшему"


def test_customer():
    "customer_revenue и best_customer — выручка по покупателям и лучший покупатель"
    assert isinstance(customer_revenue, pd.Series) and len(customer_revenue) == 213, "customer_revenue — Series с 213 покупателями в индексе: orders.groupby(\"customer_id\")[\"revenue\"].sum()"
    assert customer_revenue.sum() == 3301420, "суммы не те: складывать нужно столбец revenue"
    assert best_customer == "C134", f"best_customer = {best_customer!r}, а больше всех потратил другой покупатель: customer_revenue.idxmax()"
# ─── другое решение ───
product_qty = orders.groupby("product")["quantity"].sum()
top3 = product_qty.sort_values(ascending=False).head(3)
customer_revenue = orders.groupby("customer_id")["revenue"].sum()
best_customer = customer_revenue.sort_values().index[-1]
# ─── ошибка ───
product_qty = orders.groupby("product")["quantity"].sum()
top3 = product_qty.head(3)
customer_revenue = orders.groupby("customer_id")["revenue"].sum()
best_customer = customer_revenue.idxmax()
# ─── ошибка ───
product_qty = orders.groupby("product")["quantity"].sum()
top3 = product_qty.nlargest(3)
customer_revenue = orders.groupby("customer_id")["revenue"].sum()
best_customer = orders["customer_id"].value_counts().idxmax()
