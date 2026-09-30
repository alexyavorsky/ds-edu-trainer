# Урок pd-project-report. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% raw
import pandas as pd

raw = pd.read_csv("data/shop_orders.csv", parse_dates=["date"])
raw.head(3)

# %% prepare [exercise]
def prepare(table):
    return table.assign(
        revenue=lambda d: d["price"] * d["quantity"],
        month=lambda d: d["date"].dt.month,
    )


orders = raw.pipe(prepare)
# ─── заготовка ───
def prepare(table):
    return ...


orders = ...
# ─── проверка ───
def test_prepare():
    "prepare(table) возвращает таблицу со столбцами revenue и month"
    result = prepare(raw)
    assert result is not ..., "функция prepare пока возвращает ... — верните table.assign(...)"
    assert isinstance(result, pd.DataFrame), f"prepare вернула {type(result).__name__}, а должна возвращать таблицу"
    assert "revenue" in result.columns and "month" in result.columns, "в таблице, которую возвращает prepare, нужны столбцы revenue и month"
    assert result["revenue"].sum() == 3301420, "revenue — цена × количество"
    assert result["month"].iloc[0] == 1 and result["month"].iloc[-1] == 12, "month — номер месяца из столбца date: d[\"date\"].dt.month"
    assert "revenue" not in raw.columns, "функция изменила исходную таблицу raw: возвращайте новую таблицу через assign. Исправив функцию, выполните первую ячейку урока заново — она вернёт raw в исходный вид"


def test_orders():
    "orders — подготовленная таблица"
    assert isinstance(orders, pd.DataFrame), f"orders — это {type(orders).__name__}, а нужна таблица: raw.pipe(prepare)"
    assert orders.shape == (2448, 11), f"у orders размер {orders.shape}, а должно быть 2448 строк и 11 столбцов: девять исходных, revenue и month"
# ─── другое решение ───
def prepare(table):
    result = table.copy()
    result["revenue"] = result["price"] * result["quantity"]
    result["month"] = result["date"].dt.month
    return result


orders = prepare(raw)
# ─── ошибка ───
def prepare(table):
    return table.assign(revenue=lambda d: d["price"] * d["quantity"])


orders = raw.pipe(prepare)

# %% monthly [exercise]
monthly = (
    raw
    .pipe(prepare)
    .groupby("month")["revenue"]
    .sum()
)
best_month = monthly.idxmax()
# ─── заготовка ───
monthly = (
    raw
    # допишите шаги цепочки
)
best_month = ...
# ─── проверка ───
def test_monthly():
    "monthly — выручка по месяцам"
    assert isinstance(monthly, pd.Series), f"monthly — это {type(monthly).__name__}, а нужен Series: .pipe(prepare), затем группировка по month и сумма revenue"
    assert len(monthly) == 12 and list(monthly.index) == list(range(1, 13)), "в monthly 12 значений с номерами месяцев в индексе"
    assert monthly.iloc[0] == 318940 and monthly.sum() == 3301420, "значения не те: январь — 318940, весь год — 3301420"


def test_best():
    "best_month — номер лучшего месяца"
    assert best_month == 12, f"best_month = {best_month!r}, а лучший месяц — декабрь (12): monthly.idxmax()"
# ─── другое решение ───
monthly = raw.pipe(prepare).pivot_table(values="revenue", index="month", aggfunc="sum")["revenue"]
best_month = monthly.sort_values().index[-1]
# ─── ошибка ───
monthly = (
    raw
    .pipe(prepare)
    .groupby("month")["revenue"]
    .mean()
)
best_month = monthly.idxmax()

# %% channels [exercise]
channels = (
    raw
    .pipe(prepare)
    .pivot_table(values="revenue", index="month", columns="channel", aggfunc="sum")
    .assign(total=lambda d: d["сайт"] + d["приложение"] + d["маркетплейс"])
    .assign(site_share=lambda d: (d["сайт"] / d["total"]).round(3))
)
# ─── заготовка ───
channels = (
    raw
    # допишите шаги цепочки
)
# ─── проверка ───
def test_channels():
    "channels — выручка по месяцам и каналам, итог и доля сайта"
    assert isinstance(channels, pd.DataFrame), f"channels — это {type(channels).__name__}, а нужна таблица"
    assert len(channels) == 12, f"в channels {len(channels)} строк, а месяцев 12: index=\"month\" в pivot_table"
    assert list(channels.columns) == ["маркетплейс", "приложение", "сайт", "total", "site_share"], f"столбцы сейчас {list(channels.columns)}, а нужны маркетплейс, приложение, сайт, total, site_share"
    assert channels.loc[1, "сайт"] == 130860, "в ячейках — сумма revenue: aggfunc=\"sum\""
    assert channels.loc[1, "total"] == 318940, "total — сумма трёх каналов: январь — 318940"
    assert abs(channels.loc[1, "site_share"] - 0.41) < 1e-9, "site_share — сайт, делённый на total, с округлением до трёх знаков: январь — 0.41"
# ─── другое решение ───
channels = (
    raw
    .pipe(prepare)
    .groupby(["month", "channel"])["revenue"]
    .sum()
    .unstack()
    .assign(total=lambda d: d.sum(axis=1))
    .assign(site_share=lambda d: (d["сайт"] / d["total"]).round(3))
)
# ─── ошибка ───
channels = (
    raw
    .pipe(prepare)
    .pivot_table(values="revenue", index="month", columns="channel", aggfunc="sum")
    .assign(total=lambda d: d["сайт"] + d["приложение"] + d["маркетплейс"])
    .assign(site_share=lambda d: (d["total"] / d["сайт"]).round(3))
)
# ─── ошибка ───
channels = (
    raw
    .pipe(prepare)
    .pivot_table(values="revenue", index="channel", columns="month", aggfunc="sum")
)

# %% channels-view
channels.head(4)

# %% top [exercise]
def top_products(table, category, n):
    return (
        table
        .query("category == @category")
        .groupby("product", as_index=False)["revenue"]
        .sum()
        .nlargest(n, "revenue")
        .reset_index(drop=True)
    )


top_tea = raw.pipe(prepare).pipe(top_products, "Чай", 2)
# ─── заготовка ───
def top_products(table, category, n):
    return (
        table
        # допишите шаги: отбор категории, сумма revenue по товарам, n лучших, индекс с нуля
    )


top_tea = ...
# ─── проверка ───
def test_function():
    "top_products(table, category, n) — n товаров категории с наибольшей выручкой"
    result = top_products(prepare(raw), "Кофе", 3)
    assert isinstance(result, pd.DataFrame), f"top_products вернула {type(result).__name__}, а должна возвращать таблицу"
    assert list(result.columns) == ["product", "revenue"], f"столбцы результата сейчас {list(result.columns)}, а нужны product и revenue: groupby(\"product\", as_index=False)[\"revenue\"].sum()"
    assert len(result) == 3, f"для n = 3 функция вернула {len(result)} строк: .nlargest(n, \"revenue\")"
    assert result["product"].tolist() == ["Эфиопия 250 г", "Бразилия 1 кг", "Эспрессо-смесь 1 кг"], "для кофе три лучших товара — Эфиопия, Бразилия, Эспрессо-смесь: отбор по параметру category — query(\"category == @category\")"
    assert list(result.index) == [0, 1, 2], "индекс результата должен идти с нуля: .reset_index(drop=True)"


def test_tea():
    "top_tea — два лучших чая"
    assert isinstance(top_tea, pd.DataFrame) and len(top_tea) == 2, "top_tea — таблица из двух строк: raw.pipe(prepare).pipe(top_products, \"Чай\", 2)"
    assert top_tea["product"].tolist() == ["Улун 100 г", "Зелёный чай 100 г"], f"в top_tea сейчас {top_tea['product'].tolist()}"
# ─── другое решение ───
def top_products(table, category, n):
    part = table[table["category"] == category]
    return part.groupby("product")["revenue"].sum().sort_values(ascending=False).head(n).reset_index()


top_tea = top_products(prepare(raw), "Чай", 2)
# ─── ошибка ───
def top_products(table, category, n):
    return (
        table
        .groupby("product", as_index=False)["revenue"]
        .sum()
        .nlargest(n, "revenue")
        .reset_index(drop=True)
    )


top_tea = raw.pipe(prepare).pipe(top_products, "Чай", 2)

# %% chart [exercise]
ax = (
    raw
    .pipe(prepare)
    .pivot_table(values="revenue", index="month", columns="channel", aggfunc="sum")
    .plot(title="Выручка по каналам, 2025")
)
ax.set_xlabel("месяц")
ax.set_ylabel("₽")
# ─── заготовка ───
ax = (
    raw
    # допишите шаги цепочки; последний — .plot(...)
)
# подпишите оси
# ─── проверка ───
def test_chart():
    "ax — три линии: выручка каналов по месяцам"
    assert hasattr(ax, "lines") and hasattr(ax, "get_title"), f"ax — это {type(ax).__name__}, а нужен график: последний шаг цепочки — .plot(...)"
    assert len(ax.lines) == 3, f"линий на графике: {len(ax.lines)}, а каналов три: перед .plot нужна сводная таблица месяцы × каналы"
    labels = sorted(line.get_label() for line in ax.lines)
    assert labels == ["маркетплейс", "приложение", "сайт"], f"линии сейчас {labels}, а нужны три канала: columns=\"channel\""
    site = [line for line in ax.lines if line.get_label() == "сайт"][0]
    assert list(site.get_ydata())[0] == 130860 and len(site.get_ydata()) == 12, "на графике должна быть сумма выручки по 12 месяцам: aggfunc=\"sum\", index=\"month\""


def test_labels():
    "заголовок и подписи осей"
    assert hasattr(ax, "get_title"), "сначала постройте график и сохраните его в ax"
    assert ax.get_title() == "Выручка по каналам, 2025", f"заголовок сейчас {ax.get_title()!r}, а нужен «Выручка по каналам, 2025»"
    assert ax.get_xlabel() == "месяц", f"подпись оси X сейчас {ax.get_xlabel()!r}, а нужна «месяц»: ax.set_xlabel(\"месяц\")"
    assert ax.get_ylabel() == "₽", f"подпись оси Y сейчас {ax.get_ylabel()!r}, а нужна «₽»: ax.set_ylabel(\"₽\")"
# ─── другое решение ───
ax = channels[["маркетплейс", "приложение", "сайт"]].plot()
ax.set_title("Выручка по каналам, 2025")
ax.set_xlabel("месяц")
ax.set_ylabel("₽")
# ─── ошибка ───
ax = (
    raw
    .pipe(prepare)
    .groupby("month")["revenue"]
    .sum()
    .plot(title="Выручка по каналам, 2025")
)
ax.set_xlabel("месяц")
ax.set_ylabel("₽")
# ─── ошибка ───
ax = (
    raw
    .pipe(prepare)
    .pivot_table(values="revenue", index="month", columns="channel", aggfunc="sum")
    .plot(title="Выручка по каналам, 2025")
)

# %% share-chart
channels["site_share"].plot(kind="bar", title="Доля сайта в выручке по месяцам", rot=0)

# %% whole
(
    pd.read_csv("data/shop_orders.csv", parse_dates=["date"])
    .pipe(prepare)
    .query("category == 'Кофе'")
    .set_index("date")["revenue"]
    .resample("W")
    .sum()
    .iloc[1:-1]
    .rolling(4)
    .mean()
    .plot(title="Кофе: выручка за неделю, среднее за 4 недели")
)
