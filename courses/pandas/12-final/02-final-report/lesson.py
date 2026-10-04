# Урок pd-final-report. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% build
import pandas as pd

short = {"Спб": "Санкт-Петербург", "С.-Петербург": "Санкт-Петербург", "Екб": "Екатеринбург"}
customers = (
    pd.read_csv("data/customers_raw.csv")
    .assign(
        customer_id=lambda d: d["customer_id"].str.strip().str.upper(),
        city=lambda d: d["city"].str.strip().str.title().replace(short),
        segment=lambda d: d["segment"].str.strip().str.lower(),
    )
    [["customer_id", "city", "segment"]]
    .drop_duplicates()
)
returns = (
    pd.read_csv("data/returns_raw.csv")
    .drop_duplicates()
    .drop_duplicates(subset=["order_id", "product_id"])
    [["order_id", "product_id", "quantity"]]
    .rename(columns={"quantity": "returned"})
)
data = (
    pd.read_csv("data/orders.csv", parse_dates=["date"])
    .merge(pd.read_csv("data/products.csv"), on="product_id", validate="many_to_one")
    .merge(customers, on="customer_id", validate="many_to_one")
    .merge(returns, on=["order_id", "product_id"], how="left", validate="one_to_one")
    .assign(
        returned=lambda d: d["returned"].fillna(0).astype("int64"),
        revenue=lambda d: d["price"] * d["quantity"],
        net=lambda d: d["price"] * (d["quantity"] - d["returned"]),
        profit=lambda d: (d["price"] - d["cost"]) * (d["quantity"] - d["returned"]),
        month=lambda d: d["date"].dt.month,
    )
)
print(data.shape, data["net"].sum(), data["profit"].sum())

# %% months [exercise]
by_month = data.groupby("month").agg(net=("net", "sum"), profit=("profit", "sum"))
by_month["growth"] = by_month["net"].pct_change().round(3)
best_month = by_month["net"].idxmax()
worst_month = by_month["net"].idxmin()
# ─── заготовка ───
by_month = ...
# добавьте в by_month столбец growth
best_month = ...
worst_month = ...
# ─── проверка ───
def test_by_month():
    "by_month — чистая выручка, прибыль и рост по месяцам"
    assert isinstance(by_month, pd.DataFrame), f"by_month — это {type(by_month).__name__}, а нужна таблица"
    assert list(by_month.index) == list(range(1, 13)), "в индексе by_month должны быть номера месяцев 1–12: группируйте по столбцу month"
    assert list(by_month.columns) == ["net", "profit", "growth"], f"столбцы сейчас {list(by_month.columns)}, а нужны net, profit, growth"
    assert len(by_month) == 12 and by_month.loc[1, "net"] == 297120 and by_month.loc[1, "profit"] == 140940, "в by_month 12 месяцев, net и profit — суммы за месяц"
    assert by_month["growth"].isna().sum() == 1, "у января нет прошлого месяца — первое значение growth должно быть пропуском"
    assert abs(by_month.loc[2, "growth"] - (-0.179)) < 1e-9 and abs(by_month.loc[12, "growth"] - 0.296) < 1e-9, "growth не тот: нужен относительный рост net к прошлому месяцу, три знака"


def test_best():
    "best_month и worst_month — лучший и худший месяц по чистой выручке"
    assert best_month == 12, f"best_month = {best_month!r} — это не месяц с наибольшей чистой выручкой"
    assert worst_month == 7, f"worst_month = {worst_month!r} — это не месяц с наименьшей чистой выручкой"
# ─── другое решение ───
by_month = data.pivot_table(values=["net", "profit"], index="month", aggfunc="sum")[["net", "profit"]]
by_month["growth"] = (by_month["net"] / by_month["net"].shift(1) - 1).round(3)
best_month = by_month.sort_values("net").index[-1]
worst_month = by_month.sort_values("net").index[0]
# ─── ошибка ───
by_month = data.groupby("month").agg(net=("revenue", "sum"), profit=("profit", "sum"))
by_month["growth"] = by_month["net"].pct_change().round(3)
best_month = by_month["net"].idxmax()
worst_month = by_month["net"].idxmin()
# ─── ошибка ───
by_month = data.groupby("month").agg(net=("net", "sum"), profit=("profit", "sum"))
by_month["growth"] = by_month["net"].diff().round(3)
best_month = by_month["net"].idxmax()
worst_month = by_month["net"].idxmin()

# %% months-view
by_month

# %% categories [exercise]
by_category = data.groupby("category").agg(net=("net", "sum"), profit=("profit", "sum"), sold=("quantity", "sum"), returned=("returned", "sum"))
by_category["margin"] = (by_category["profit"] / by_category["net"]).round(3)
by_category["return_rate"] = (by_category["returned"] / by_category["sold"]).round(3)
by_category = by_category.sort_values("profit", ascending=False)
# ─── заготовка ───
by_category = ...
# ─── проверка ───
def test_by_category():
    "by_category — выручка, прибыль, штуки, маржа и доля возврата по категориям"
    assert isinstance(by_category, pd.DataFrame), f"by_category — это {type(by_category).__name__}, а нужна таблица"
    assert list(by_category.columns) == ["net", "profit", "sold", "returned", "margin", "return_rate"], f"столбцы сейчас {list(by_category.columns)}, а нужны net, profit, sold, returned, margin, return_rate"
    assert len(by_category) == 5 and by_category.loc["Кофе", "net"] == 1830330 and by_category.loc["Кофе", "sold"] == 2138, "в by_category пять категорий, net и sold — суммы по категории"
    assert abs(by_category.loc["Чай", "margin"] - 0.56) < 1e-9, "margin не тот: нужна доля прибыли в net, три знака"
    assert abs(by_category.loc["Кофе", "return_rate"] - 0.042) < 1e-9, "return_rate не тот: нужна доля возвращённых штук среди проданных, три знака"


def test_order():
    "категории — по убыванию прибыли"
    assert isinstance(by_category, pd.DataFrame) and "profit" in by_category.columns, "сначала исправьте то, о чём говорит проверка выше"
    assert by_category["profit"].tolist() == sorted(by_category["profit"].tolist(), reverse=True), "отсортируйте by_category по убыванию profit"
# ─── другое решение ───
g = data.groupby("category")
by_category = pd.DataFrame({"net": g["net"].sum(), "profit": g["profit"].sum(), "sold": g["quantity"].sum(), "returned": g["returned"].sum()})
by_category = by_category.assign(margin=lambda d: (d["profit"] / d["net"]).round(3), return_rate=lambda d: (d["returned"] / d["sold"]).round(3))
by_category = by_category.sort_values("profit", ascending=False)
# ─── ошибка ───
by_category = data.groupby("category").agg(net=("net", "sum"), profit=("profit", "sum"), sold=("quantity", "sum"), returned=("returned", "sum"))
by_category["margin"] = (by_category["profit"] / by_category["net"]).round(3)
by_category["return_rate"] = (by_category["returned"] / by_category["sold"]).round(3)
# ─── ошибка ───
by_category = data.groupby("category").agg(net=("net", "sum"), profit=("profit", "sum"), sold=("quantity", "sum"), returned=("returned", "sum"))
by_category["margin"] = (by_category["net"] / by_category["profit"]).round(3)
by_category["return_rate"] = (by_category["returned"] / by_category["sold"]).round(3)
by_category = by_category.sort_values("profit", ascending=False)

# %% categories-view
by_category

# %% cities [exercise]
by_city = data.groupby("city").agg(net=("net", "sum"), orders=("order_id", "nunique"), buyers=("customer_id", "nunique"))
by_city["check"] = (by_city["net"] / by_city["orders"]).round()
by_city["share"] = (by_city["net"] / by_city["net"].sum()).round(3)
top_check_city = by_city["check"].idxmax()
# ─── заготовка ───
by_city = ...
top_check_city = ...
# ─── проверка ───
def test_by_city():
    "by_city — выручка, заказы, покупатели, средний чек и доля по городам"
    assert isinstance(by_city, pd.DataFrame), f"by_city — это {type(by_city).__name__}, а нужна таблица"
    assert list(by_city.columns) == ["net", "orders", "buyers", "check", "share"], f"столбцы сейчас {list(by_city.columns)}, а нужны net, orders, buyers, check, share"
    assert by_city.loc["Москва", "net"] == 1245060, "net не тот: нужна сумма net по городу"
    assert by_city.loc["Москва", "orders"] != 948, "orders — число разных заказов, а не строк"
    assert by_city.loc["Москва", "orders"] == 627 and by_city.loc["Москва", "buyers"] == 79, "orders или buyers не те: нужно число разных заказов и покупателей"
    assert by_city.loc["Москва", "check"] == 1986, "check не тот: нужна net на один заказ, до рублей"
    assert abs(by_city.loc["Москва", "share"] - 0.394) < 1e-9 and abs(by_city["share"].sum() - 1) < 0.01, "share не тот: нужна доля города в общей net, три знака"


def test_top():
    "top_check_city — город с наибольшим средним чеком"
    assert top_check_city == "Санкт-Петербург", f"top_check_city = {top_check_city!r}, а самый высокий средний чек в другом городе"
# ─── другое решение ───
g = data.groupby("city")
by_city = pd.DataFrame({"net": g["net"].sum(), "orders": g["order_id"].nunique(), "buyers": g["customer_id"].nunique()})
by_city["check"] = round(by_city["net"] / by_city["orders"])
by_city["share"] = round(by_city["net"] / data["net"].sum(), 3)
top_check_city = by_city.sort_values("check").index[-1]
# ─── ошибка ───
by_city = data.groupby("city").agg(net=("net", "sum"), orders=("order_id", "count"), buyers=("customer_id", "nunique"))
by_city["check"] = (by_city["net"] / by_city["orders"]).round()
by_city["share"] = (by_city["net"] / by_city["net"].sum()).round(3)
top_check_city = by_city["check"].idxmax()

# %% pivot [exercise]
cross = data.pivot_table(values="net", index="category", columns="city", aggfunc="sum", margins=True, margins_name="Всего")
moscow_coffee_share = cross.loc["Кофе", "Москва"] / cross.loc["Всего", "Всего"]
# ─── заготовка ───
cross = ...
moscow_coffee_share = ...
# ─── проверка ───
def test_cross():
    "cross — чистая выручка: категории × города, с итогами «Всего»"
    assert isinstance(cross, pd.DataFrame), f"cross — это {type(cross).__name__}, а нужна таблица"
    assert "Всего" in cross.index and "Всего" in cross.columns, "в cross нет итогов: вспомните параметры margins и margins_name"
    assert cross.shape == (6, 6), f"у cross размер {cross.shape}, а нужно 6 × 6: пять категорий и пять городов с итогами"
    assert "Кофе" in cross.index and "Москва" in cross.columns, "в строках — категории, в столбцах — города"
    assert cross.loc["Кофе", "Москва"] == 735480 and cross.loc["Всего", "Всего"] == 3159140, "в ячейках должна быть сумма net"


def test_share():
    "moscow_coffee_share — доля московского кофе во всей чистой выручке"
    assert abs(moscow_coffee_share - 735480 / 3159140) < 1e-9, f"moscow_coffee_share = {moscow_coffee_share!r} — это не доля московского кофе во всей чистой выручке"
# ─── другое решение ───
cross = data.pivot_table(values="net", index="category", columns="city", aggfunc="sum", margins=True, margins_name="Всего")
moscow_coffee_share = data.loc[(data["category"] == "Кофе") & (data["city"] == "Москва"), "net"].sum() / data["net"].sum()
# ─── ошибка ───
cross = data.pivot_table(values="net", index="category", columns="city", margins=True, margins_name="Всего")
moscow_coffee_share = cross.loc["Кофе", "Москва"] / cross.loc["Всего", "Всего"]
# ─── ошибка ───
cross = data.pivot_table(values="net", index="category", columns="city", aggfunc="sum")
moscow_coffee_share = 0.233

# %% pivot-view
cross

# %% segments [exercise]
by_segment = data.groupby("segment").agg(net=("net", "sum"), buyers=("customer_id", "nunique"))
by_segment["per_buyer"] = (by_segment["net"] / by_segment["buyers"]).round()
vip = data.groupby(["customer_id", "city", "segment"], as_index=False)["net"].sum().nlargest(5, "net").reset_index(drop=True)
# ─── заготовка ───
by_segment = ...
vip = ...
# ─── проверка ───
def test_segment():
    "by_segment — выручка, покупатели и выручка на покупателя по сегментам"
    assert isinstance(by_segment, pd.DataFrame), f"by_segment — это {type(by_segment).__name__}, а нужна таблица"
    assert list(by_segment.columns) == ["net", "buyers", "per_buyer"], f"столбцы сейчас {list(by_segment.columns)}, а нужны net, buyers, per_buyer"
    assert by_segment.loc["оптовый", "net"] == 737000 and by_segment.loc["оптовый", "buyers"] == 25, "значения не те: net — сумма по сегменту, buyers — число разных покупателей"
    assert by_segment.loc["оптовый", "per_buyer"] == 29480, "per_buyer не тот: нужна net на одного покупателя, до рублей"


def test_vip():
    "vip — пять покупателей с наибольшей чистой выручкой"
    assert isinstance(vip, pd.DataFrame), f"vip — это {type(vip).__name__}, а нужна таблица"
    assert list(vip.columns) == ["customer_id", "city", "segment", "net"], f"столбцы сейчас {list(vip.columns)}, а нужны customer_id, city, segment, net"
    assert len(vip) == 5, f"в vip {len(vip)} строк, а нужно пять"
    assert vip["customer_id"].tolist() == ["C134", "C137", "C118", "C151", "C216"], f"покупатели сейчас {vip['customer_id'].tolist()}: нужны пять покупателей с наибольшей net"
    assert list(vip.index) == [0, 1, 2, 3, 4], "индекс vip должен идти с нуля"
# ─── другое решение ───
g = data.groupby("segment")
by_segment = pd.DataFrame({"net": g["net"].sum(), "buyers": g["customer_id"].nunique()})
by_segment["per_buyer"] = round(by_segment["net"] / by_segment["buyers"])
vip = data.groupby(["customer_id", "city", "segment"])["net"].sum().reset_index().sort_values("net", ascending=False).head(5).reset_index(drop=True)
# ─── ошибка ───
by_segment = data.groupby("segment").agg(net=("net", "sum"), buyers=("customer_id", "nunique"))
by_segment["per_buyer"] = (by_segment["net"] / by_segment["buyers"]).round()
vip = data.groupby(["customer_id", "city", "segment"], as_index=False)["net"].sum().nsmallest(5, "net").reset_index(drop=True)
# ─── ошибка ───
by_segment = data.groupby("segment").agg(net=("net", "sum"), buyers=("customer_id", "count"))
by_segment["per_buyer"] = (by_segment["net"] / by_segment["buyers"]).round()
vip = data.groupby(["customer_id", "city", "segment"], as_index=False)["net"].sum().nlargest(5, "net").reset_index(drop=True)

# %% chart [exercise]
ax = by_month[["net", "profit"]].plot(title="Чистая выручка и прибыль по месяцам, 2025")
ax.set_xlabel("месяц")
ax.set_ylabel("₽")
# ─── заготовка ───
ax = ...
# подпишите оси
# ─── проверка ───
def test_chart():
    "ax — две линии: чистая выручка и прибыль по месяцам"
    assert hasattr(ax, "lines") and hasattr(ax, "get_title"), f"ax — это {type(ax).__name__}, а нужен график"
    assert len(ax.lines) != 3, "на графике три линии: столбец growth рисовать не нужно — выберите net и profit"
    assert len(ax.lines) == 2, f"линий на графике: {len(ax.lines)}, а нужны две — net и profit"
    assert [line.get_label() for line in ax.lines] == ["net", "profit"], "линии должны быть net и profit — в этом порядке"
    assert list(ax.lines[0].get_ydata())[0] == 297120 and len(ax.lines[0].get_ydata()) == 12, "на графике должны быть 12 месяцев из by_month"


def test_labels():
    "заголовок и подписи осей"
    assert hasattr(ax, "get_title"), "сначала постройте график и сохраните его в ax"
    assert ax.get_title() == "Чистая выручка и прибыль по месяцам, 2025", f"заголовок сейчас {ax.get_title()!r}"
    assert ax.get_xlabel() == "месяц" and ax.get_ylabel() == "₽", f"подписи осей сейчас {ax.get_xlabel()!r} и {ax.get_ylabel()!r}, а нужны «месяц» и «₽»"
# ─── другое решение ───
ax = by_month["net"].plot(label="net")
by_month["profit"].plot(ax=ax, label="profit")
ax.set_title("Чистая выручка и прибыль по месяцам, 2025")
ax.set_xlabel("месяц")
ax.set_ylabel("₽")
# ─── ошибка ───
ax = by_month.plot(title="Чистая выручка и прибыль по месяцам, 2025")
ax.set_xlabel("месяц")
ax.set_ylabel("₽")
# ─── ошибка ───
ax = by_month[["net", "profit"]].plot()

# %% category-chart
by_category["profit"].sort_values().plot(kind="barh", title="Прибыль по категориям, ₽")

# %% summary
total_net = data["net"].sum()
total_profit = data["profit"].sum()
print("Выручка:", data["revenue"].sum(), "₽ · после возвратов:", total_net, "₽")
print("Прибыль:", total_profit, "₽ · маржа:", round(total_profit / total_net * 100, 1), "%")
print("Заказов:", data["order_id"].nunique(), "· покупателей:", data["customer_id"].nunique())
print("Лучший месяц:", best_month, "· худший:", worst_month)
print("Самый высокий средний чек:", top_check_city)
print(by_segment)
